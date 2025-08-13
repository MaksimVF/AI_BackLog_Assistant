
"""
Storage Management Module for AI Backlog Assistant

Handles storage policy enforcement including:
- Storage cleanup based on retention policies
- Expiration handling
- Background job processing
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from flask import current_app as app
from .extensions import db
from .billing_models import StoragePricing, TariffPlan
from .models import User, Document
from sqlalchemy.exc import SQLAlchemyError

class StorageException(Exception):
    """Custom exception for storage errors."""
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code

class StorageManager:
    """Central storage manager for handling storage policy enforcement."""

    @staticmethod
    def cleanup_expired_storage() -> Dict[str, Any]:
        """
        Clean up expired storage based on retention policies and expiration dates.

        Returns:
            Dict: Cleanup report including number of items cleaned up
        """
        try:
            # Get current time
            now = datetime.utcnow()

            # Clean up expired user storage quotas
            expired_users = User.query.filter(
                User.storage_expiration != None,
                User.storage_expiration < now
            ).all()

            cleanup_count = 0

            for user in expired_users:
                # Reset storage quota to default/free tier
                user.storage_quota_mb = 100  # Default free tier
                user.storage_retention_days = 30  # Default retention
                user.storage_tier = 'free'
                user.storage_expiration = None
                db.session.add(user)
                cleanup_count += 1

            # Clean up documents based on retention policies
            # For each organization, get their tariff plan to determine retention
            from .models import Organization

            organizations = Organization.query.all()
            doc_cleanup_count = 0

            for org in organizations:
                # Get tariff plan for retention policy
                org_balance = org.balance
                retention_days = 180  # Default retention

                if org_balance and org_balance.tariff_plan_id:
                    tariff_plan = TariffPlan.query.get(org_balance.tariff_plan_id)
                    if tariff_plan:
                        retention_days = tariff_plan.storage_retention_days

                # Calculate expiration date based on retention
                expiration_date = now - timedelta(days=retention_days)

                # Find and soft-delete expired documents
                expired_docs = Document.query.filter(
                    Document.organization_id == org.id,
                    Document.created_at < expiration_date,
                    Document.is_deleted == False
                ).all()

                for doc in expired_docs:
                    # Soft delete the document
                    doc.is_deleted = True
                    doc.deleted_at = now
                    db.session.add(doc)
                    doc_cleanup_count += 1

            db.session.commit()

            return {
                'status': 'success',
                'user_quotas_cleaned': cleanup_count,
                'documents_cleaned': doc_cleanup_count,
                'timestamp': now.isoformat()
            }

        except SQLAlchemyError as e:
            db.session.rollback()
            raise StorageException(f"Database error: {str(e)}", 500)
        except Exception as e:
            db.session.rollback()
            raise StorageException(f"Storage cleanup error: {str(e)}", 500)

    @staticmethod
    def enforce_storage_quotas(organization_id: str) -> Dict[str, Any]:
        """
        Enforce storage quotas for an organization.

        Args:
            organization_id: The organization ID

        Returns:
            Dict: Enforcement report
        """
        try:
            # Get organization's tariff plan to determine storage limits
            from .billing_models import OrganizationBalance

            org_balance = OrganizationBalance.query.filter_by(organization_id=organization_id).first()
            if not org_balance:
                raise StorageException("Organization balance not found", 404)

            # Calculate total storage usage
            total_storage_mb = 0
            users = User.query.filter_by(organization_id=organization_id).all()

            for user in users:
                total_storage_mb += user.storage_quota_mb or 0

            # Get storage limits from tariff plan
            storage_limit_mb = 1024  # Default 1GB in MB
            if org_balance.tariff_plan_id:
                tariff_plan = TariffPlan.query.get(org_balance.tariff_plan_id)
                if tariff_plan:
                    # Convert GB to MB
                    storage_limit_mb = tariff_plan.included_storage_gb * 1024

            # Check if organization is over quota
            is_over_quota = total_storage_mb > storage_limit_mb
            excess_storage_mb = max(0, total_storage_mb - storage_limit_mb)

            return {
                'status': 'success',
                'organization_id': organization_id,
                'total_storage_mb': total_storage_mb,
                'storage_limit_mb': storage_limit_mb,
                'is_over_quota': is_over_quota,
                'excess_storage_mb': excess_storage_mb
            }

        except SQLAlchemyError as e:
            db.session.rollback()
            raise StorageException(f"Database error: {str(e)}", 500)
        except Exception as e:
            db.session.rollback()
            raise StorageException(f"Storage enforcement error: {str(e)}", 500)

    @staticmethod
    def get_storage_usage(organization_id: str) -> Dict[str, Any]:
        """
        Get storage usage statistics for an organization.

        Args:
            organization_id: The organization ID

        Returns:
            Dict: Storage usage statistics
        """
        try:
            # Calculate total storage usage by users
            users = User.query.filter_by(organization_id=organization_id).all()

            total_storage_mb = 0
            storage_by_tier = {}

            for user in users:
                user_storage_mb = user.storage_quota_mb or 0
                total_storage_mb += user_storage_mb

                # Track by storage tier
                if user.storage_tier not in storage_by_tier:
                    storage_by_tier[user.storage_tier] = 0
                storage_by_tier[user.storage_tier] += user_storage_mb

            # Calculate total storage usage by documents
            # In a real implementation, this would sum up actual document sizes
            # For now, we'll use a placeholder
            documents = Document.query.filter_by(organization_id=organization_id).all()
            document_storage_mb = len(documents) * 0.5  # Average 0.5MB per document (placeholder)

            total_storage_mb += document_storage_mb
            storage_by_tier['documents'] = document_storage_mb

            return {
                'status': 'success',
                'organization_id': organization_id,
                'total_storage_mb': total_storage_mb,
                'total_storage_gb': total_storage_mb / 1024,
                'storage_by_tier': storage_by_tier,
                'user_count': len(users),
                'document_count': len(documents)
            }

        except SQLAlchemyError as e:
            db.session.rollback()
            raise StorageException(f"Database error: {str(e)}", 500)
        except Exception as e:
            db.session.rollback()
            raise StorageException(f"Storage usage calculation error: {str(e)}", 500)

    @staticmethod
    def apply_retention_policy(organization_id: str, retention_days: int) -> Dict[str, Any]:
        """
        Apply retention policy to an organization's documents.

        Args:
            organization_id: The organization ID
            retention_days: Number of days to retain documents

        Returns:
            Dict: Retention policy application report
        """
        try:
            # Get current time
            now = datetime.utcnow()
            expiration_date = now - timedelta(days=retention_days)

            # Find and soft-delete expired documents
            expired_docs = Document.query.filter(
                Document.organization_id == organization_id,
                Document.created_at < expiration_date,
                Document.is_deleted == False
            ).all()

            cleanup_count = 0
            for doc in expired_docs:
                # Soft delete the document
                doc.is_deleted = True
                doc.deleted_at = now
                db.session.add(doc)
                cleanup_count += 1

            db.session.commit()

            return {
                'status': 'success',
                'organization_id': organization_id,
                'retention_days': retention_days,
                'documents_cleaned': cleanup_count,
                'timestamp': now.isoformat()
            }

        except SQLAlchemyError as e:
            db.session.rollback()
            raise StorageException(f"Database error: {str(e)}", 500)
        except Exception as e:
            db.session.rollback()
            raise StorageException(f"Retention policy error: {str(e)}", 500)

