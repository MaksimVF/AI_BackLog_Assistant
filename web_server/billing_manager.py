

"""
Billing Manager for AI Backlog Assistant

Centralized service for handling all billing operations including:
- Access control
- Limit checking
- Charging (PAYG and subscription)
- Usage logging
"""

import uuid
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from flask import current_app as app
from .app import db
from .billing_models import TariffPlan, OrganizationBalance, UsageLog, FeatureConfig
from sqlalchemy.exc import SQLAlchemyError

class BillingException(Exception):
    """Custom exception for billing errors."""
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code

class BillingManager:
    """Central billing manager for handling all billing operations."""

    @staticmethod
    def check_access(organization_id: str, feature_name: str) -> bool:
        """
        Check if an organization has access to a specific feature.

        Args:
            organization_id: The organization ID
            feature_name: The feature to check access for

        Returns:
            bool: True if access is granted, False otherwise

        Raises:
            BillingException: If access is denied
        """
        # Get organization's tariff plan
        org_balance = OrganizationBalance.query.filter_by(organization_id=organization_id).first()
        if not org_balance:
            raise BillingException("Organization balance not found", 404)

        # Get feature configuration
        feature_config = FeatureConfig.query.filter_by(feature_name=feature_name).first()
        if not feature_config:
            raise BillingException("Feature not configured", 404)

        # Check if feature is exclusive and requires specific tariff
        if feature_config.feature_type == 'exclusive':
            if feature_config.access_tariffs and org_balance.tariff_plan_id:
                tariff_plan = TariffPlan.query.get(org_balance.tariff_plan_id)
                if tariff_plan and tariff_plan.name not in feature_config.access_tariffs:
                    raise BillingException(f"Feature '{feature_name}' requires a different tariff plan", 403)

        return True

    @staticmethod
    def get_price(organization_id: str, feature_name: str) -> float:
        """
        Get the price for using a feature, considering tariff discounts.

        Args:
            organization_id: The organization ID
            feature_name: The feature name

        Returns:
            float: The price per unit for the feature

        Raises:
            BillingException: If feature is not configured or other errors occur
        """
        # Get feature configuration
        feature_config = FeatureConfig.query.filter_by(feature_name=feature_name).first()
        if not feature_config:
            raise BillingException("Feature not configured", 404)

        price = feature_config.price_per_unit

        # Check for tariff discounts
        org_balance = OrganizationBalance.query.filter_by(organization_id=organization_id).first()
        if org_balance and org_balance.tariff_plan_id:
            tariff_plan = TariffPlan.query.get(org_balance.tariff_plan_id)
            if tariff_plan and 'PAYG' in tariff_plan.discounts:
                discount = tariff_plan.discounts['PAYG']
                price = price * (1 - discount)

        return price

    @staticmethod
    def check_limit(organization_id: str, feature_name: str) -> Tuple[int, int]:
        """
        Check remaining limit for a feature.

        Args:
            organization_id: The organization ID
            feature_name: The feature name

        Returns:
            Tuple[int, int]: (remaining_limit, total_limit)

        Raises:
            BillingException: If organization or feature not found
        """
        # Get organization balance and tariff
        org_balance = OrganizationBalance.query.filter_by(organization_id=organization_id).first()
        if not org_balance:
            raise BillingException("Organization balance not found", 404)

        if not org_balance.tariff_plan_id:
            return (0, 0)  # No tariff plan, no limits

        tariff_plan = TariffPlan.query.get(org_balance.tariff_plan_id)
        if not tariff_plan:
            return (0, 0)

        # Get limit from tariff plan
        included_limits = tariff_plan.included_limits or {}
        total_limit = included_limits.get(feature_name, 0)

        # Calculate usage for current billing period
        # For simplicity, we'll use all-time usage in this basic implementation
        # In production, this should be filtered by billing period
        usage = UsageLog.query.filter_by(
            organization_id=organization_id,
            feature=feature_name
        ).with_entities(db.func.sum(UsageLog.units_used)).scalar() or 0

        remaining = total_limit - usage
        return (max(remaining, 0), total_limit)

    @staticmethod
    def charge(organization_id: str, feature_name: str, units: int = 1, user_id: str = None) -> float:
        """
        Charge for feature usage, either from limits or balance.

        Args:
            organization_id: The organization ID
            feature_name: The feature name
            units: Number of units to charge
            user_id: Optional user ID for logging

        Returns:
            float: Amount charged from balance (0 if charged from limits)

        Raises:
            BillingException: For various billing errors
        """
        try:
            # Check access first
            BillingManager.check_access(organization_id, feature_name)

            # Check remaining limits
            remaining_limit, total_limit = BillingManager.check_limit(organization_id, feature_name)

            amount_charged = 0.0

            if remaining_limit >= units:
                # Charge from limits
                units_from_limit = units
                units_from_balance = 0
            else:
                # Charge remaining from limits, rest from balance
                units_from_limit = remaining_limit
                units_from_balance = units - remaining_limit

                if units_from_balance > 0:
                    # Get price and charge from balance
                    price_per_unit = BillingManager.get_price(organization_id, feature_name)
                    amount_charged = units_from_balance * price_per_unit

                    # Check balance
                    org_balance = OrganizationBalance.query.filter_by(organization_id=organization_id).first()
                    if not org_balance:
                        raise BillingException("Organization balance not found", 404)

                    if org_balance.balance_rub < amount_charged:
                        raise BillingException("Insufficient balance", 402)

                    # Deduct from balance
                    org_balance.balance_rub -= amount_charged
                    db.session.add(org_balance)

            # Log usage
            usage_log = BillingManager.log_usage(
                organization_id=organization_id,
                user_id=user_id,
                feature=feature_name,
                units_used=units,
                price_charged=amount_charged
            )

            db.session.commit()
            return amount_charged

        except SQLAlchemyError as e:
            db.session.rollback()
            raise BillingException(f"Database error: {str(e)}", 500)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def log_usage(organization_id: str, user_id: str, feature: str, units_used: int,
                 price_charged: float, additional_data: Optional[Dict] = None) -> UsageLog:
        """
        Log feature usage.

        Args:
            organization_id: The organization ID
            user_id: The user ID
            feature: The feature name
            units_used: Number of units used
            price_charged: Amount charged
            additional_data: Additional metadata

        Returns:
            UsageLog: The created usage log entry
        """
        usage_log = UsageLog(
            id=str(uuid.uuid4()),
            organization_id=organization_id,
            user_id=user_id,
            feature=feature,
            units_used=units_used,
            price_charged=price_charged,
            additional_data=additional_data
        )

        db.session.add(usage_log)
        db.session.commit()

        return usage_log

    @staticmethod
    def get_balance(organization_id: str) -> float:
        """
        Get current balance for an organization.

        Args:
            organization_id: The organization ID

        Returns:
            float: Current balance

        Raises:
            BillingException: If organization balance not found
        """
        org_balance = OrganizationBalance.query.filter_by(organization_id=organization_id).first()
        if not org_balance:
            raise BillingException("Organization balance not found", 404)

        return org_balance.balance_rub

    @staticmethod
    def top_up(organization_id: str, amount: float) -> float:
        """
        Add funds to an organization's balance.

        Args:
            organization_id: The organization ID
            amount: Amount to add

        Returns:
            float: New balance

        Raises:
            BillingException: If organization balance not found
        """
        org_balance = OrganizationBalance.query.filter_by(organization_id=organization_id).first()
        if not org_balance:
            raise BillingException("Organization balance not found", 404)

        org_balance.balance_rub += amount
        org_balance.last_updated = datetime.utcnow()

        db.session.add(org_balance)
        db.session.commit()

        return org_balance.balance_rub

    @staticmethod
    def get_usage_history(organization_id: str, feature_name: Optional[str] = None,
                         start_date: Optional[datetime] = None,
                         end_date: Optional[datetime] = None) -> list:
        """
        Get usage history for an organization.

        Args:
            organization_id: The organization ID
            feature_name: Optional feature name to filter by
            start_date: Optional start date
            end_date: Optional end date

        Returns:
            list: List of UsageLog entries
        """
        query = UsageLog.query.filter_by(organization_id=organization_id)

        if feature_name:
            query = query.filter_by(feature=feature_name)

        if start_date:
            query = query.filter(UsageLog.timestamp >= start_date)

        if end_date:
            query = query.filter(UsageLog.timestamp <= end_date)

        return query.order_by(UsageLog.timestamp.desc()).all()

    @staticmethod
    def initialize_organization_balance(organization_id: str, tariff_plan_id: Optional[str] = None,
                                      initial_balance: float = 0.0) -> OrganizationBalance:
        """
        Initialize balance for a new organization.

        Args:
            organization_id: The organization ID
            tariff_plan_id: Optional tariff plan ID
            initial_balance: Initial balance amount

        Returns:
            OrganizationBalance: The created balance entry
        """
        org_balance = OrganizationBalance(
            organization_id=organization_id,
            balance_rub=initial_balance,
            tariff_plan_id=tariff_plan_id
        )

        db.session.add(org_balance)
        db.session.commit()

        return org_balance

    @staticmethod
    def get_tariff_features(tariff_plan_id: str) -> list:
        """
        Get features available for a tariff plan.

        Args:
            tariff_plan_id: The tariff plan ID

        Returns:
            list: List of feature names
        """
        tariff_plan = TariffPlan.query.get(tariff_plan_id)
        if not tariff_plan:
            raise BillingException("Tariff plan not found", 404)

        return tariff_plan.access_features or []

