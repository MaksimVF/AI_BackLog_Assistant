











"""
Team Billing Manager for AI Backlog Assistant
"""

from datetime import datetime
from .extensions import db
from .billing_models import OrganizationBalance, TariffPlan
from .billing_manager import BillingException

class TeamBillingManager:
    """
    Manager for team-based billing, including adding team members and managing limits.
    """

    @staticmethod
    def add_team_member(organization_id: str) -> None:
        """
        Add a new team member to an organization, checking limits and charging if necessary.
        """
        # Get organization balance and tariff
        org_balance = OrganizationBalance.query.get(organization_id)
        if not org_balance:
            raise BillingException("Organization not found")

        tariff = TariffPlan.query.get(org_balance.tariff_plan_id)
        if not tariff:
            raise BillingException("Tariff plan not found")

        # Check team member limit
        if org_balance.team_members >= tariff.max_team_members:
            raise BillingException("Team member limit reached")

        # Calculate cost for additional member
        cost = tariff.member_price

        # Check balance
        if org_balance.balance_rub < cost:
            raise BillingException("Insufficient balance for adding team member")

        # Deduct cost
        org_balance.balance_rub -= cost
        org_balance.team_members += 1
        org_balance.last_updated = datetime.utcnow()

        db.session.commit()

    @staticmethod
    def remove_team_member(organization_id: str) -> None:
        """
        Remove a team member from an organization.
        """
        org_balance = OrganizationBalance.query.get(organization_id)
        if not org_balance:
            raise BillingException("Organization not found")

        if org_balance.team_members <= 1:
            raise BillingException("Cannot remove the last team member")

        org_balance.team_members -= 1
        org_balance.last_updated = datetime.utcnow()

        db.session.commit()

    @staticmethod
    def get_team_info(organization_id: str) -> dict:
        """
        Get information about the team, including members and limits.
        """
        org_balance = OrganizationBalance.query.get(organization_id)
        if not org_balance:
            raise BillingException("Organization not found")

        tariff = TariffPlan.query.get(org_balance.tariff_plan_id)

        return {
            "team_members": org_balance.team_members,
            "max_team_members": tariff.max_team_members if tariff else None,
            "member_price": tariff.member_price if tariff else None,
            "balance": org_balance.balance_rub
        }

    @staticmethod
    def upgrade_team_tariff(organization_id: str, new_tariff_id: str) -> None:
        """
        Upgrade an organization to a new team tariff.
        """
        org_balance = OrganizationBalance.query.get(organization_id)
        if not org_balance:
            raise BillingException("Organization not found")

        new_tariff = TariffPlan.query.get(new_tariff_id)
        if not new_tariff:
            raise BillingException("New tariff not found")

        # Check if upgrade is needed
        if org_balance.tariff_plan_id == new_tariff_id:
            raise BillingException("Organization already on this tariff")

        # Check balance for upgrade cost
        upgrade_cost = new_tariff.price_per_month - (org_balance.tariff_plan.price_per_month if org_balance.tariff_plan else 0)
        if org_balance.balance_rub < upgrade_cost:
            raise BillingException("Insufficient balance for tariff upgrade")

        # Apply upgrade
        org_balance.balance_rub -= upgrade_cost
        org_balance.tariff_plan_id = new_tariff_id
        org_balance.last_updated = datetime.utcnow()

        db.session.commit()





