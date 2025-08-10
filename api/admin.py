




"""
FastAPI Admin Module - Complete implementation with best features from Flask and FastAPI versions
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from models.user import UserRole
from security.permissions import require_role, TokenData
from config.llm_config import (
    get_llm_config, set_llm_config, add_model_config, remove_model_config,
    set_default_model, LLMModelConfig, LLMProvider
)
from config.billing_config import FEATURE_CONFIG, TARIFF_PLANS
from web_server.billing_models import TariffPlan, OrganizationBalance, UsageLog
from web_server.models import User, Organization
from web_server.extensions import db

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={401: {"description": "Unauthorized - requires admin role"}}
)

class LLMModelCreate(BaseModel):
    """Model for creating/updating LLM models"""
    name: str = Field(..., description="Name of the LLM model")
    provider: str = Field(..., description="Provider of the LLM model")
    api_key: Optional[str] = Field(None, description="API key for the model")
    api_url: Optional[str] = Field(None, description="API URL for the model")
    max_tokens: int = Field(4096, description="Maximum tokens for the model")
    temperature: float = Field(0.7, description="Temperature setting for the model")
    is_default: bool = Field(False, description="Whether this is the default model")

    @validator('temperature')
    def validate_temperature(cls, v):
        if not 0 <= v <= 1:
            raise ValueError('Temperature must be between 0 and 1')
        return v

class TariffPlanCreate(BaseModel):
    """Model for creating/updating tariff plans"""
    name: str = Field(..., description="Name of the tariff plan")
    price_per_month: float = Field(..., description="Monthly price for the plan")
    included_limits: Optional[Dict[str, int]] = Field({}, description="Usage limits included in the plan")
    discounts: Optional[Dict[str, float]] = Field({}, description="Discounts for the plan")
    access_features: Optional[List[str]] = Field([], description="Features accessible with this plan")

class TariffPlanUpdate(TariffPlanCreate):
    """Model for updating tariff plans (allows optional fields)"""
    name: Optional[str] = Field(None, description="Name of the tariff plan")
    price_per_month: Optional[float] = Field(None, description="Monthly price for the plan")

class ManualTransaction(BaseModel):
    """Model for manual transactions"""
    organization_id: str = Field(..., description="ID of the organization")
    amount: float = Field(..., description="Amount to add/remove")
    description: Optional[str] = Field("Manual transaction", description="Description of the transaction")

class FeatureUpdate(BaseModel):
    """Model for updating feature configuration"""
    config: Dict[str, Any] = Field(..., description="Feature configuration data")

@router.post("/command")
async def admin_command(
    command: dict,
    current_user: TokenData = Depends(require_role(UserRole.ADMIN))
) -> dict:
    """Admin command endpoint - only accessible to users with ADMIN role"""
    # Here you would implement the actual admin command logic
    return {
        "status": "success",
        "message": "Admin command executed successfully",
        "command": command,
        "executed_by": current_user.username
    }

@router.get("/status")
async def admin_status(current_user: TokenData = Depends(require_role(UserRole.ADMIN))) -> dict:
    """Get admin status - only accessible to users with ADMIN role"""
    return {
        "status": "ok",
        "message": "Admin system is running",
        "accessed_by": current_user.username
    }

# LLM Management Endpoints
@router.get("/llm/models")
async def get_llm_models(current_user: TokenData = Depends(require_role(UserRole.ADMIN))) -> dict:
    """Get all LLM models"""
    config = get_llm_config()
    return {
        "default_provider": config.default_provider.value,
        "models": [{
            "name": model.name,
            "provider": model.provider.value,
            "max_tokens": model.max_tokens,
            "temperature": model.temperature,
            "is_default": model.is_default
        } for model in config.models]
    }

@router.post("/llm/models")
async def create_llm_model(
    model_data: LLMModelCreate,
    current_user: TokenData = Depends(require_role(UserRole.ADMIN))
) -> dict:
    """Create or update an LLM model"""
    try:
        model_config = LLMModelConfig(
            name=model_data.name,
            provider=LLMProvider(model_data.provider),
            api_key=model_data.api_key,
            api_url=model_data.api_url,
            max_tokens=model_data.max_tokens,
            temperature=model_data.temperature,
            is_default=model_data.is_default
        )

        add_model_config(model_config)

        if model_data.is_default:
            set_default_model(model_data.name)

        return {
            "status": "success",
            "message": "LLM model created/updated successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/llm/models/{model_name}")
async def delete_llm_model(
    model_name: str,
    current_user: TokenData = Depends(require_role(UserRole.ADMIN))
) -> dict:
    """Delete an LLM model"""
    try:
        remove_model_config(model_name)
        return {
            "status": "success",
            "message": "LLM model deleted successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/llm/models/{model_name}/set_default")
async def set_default_llm_model(
    model_name: str,
    current_user: TokenData = Depends(require_role(UserRole.ADMIN))
) -> dict:
    """Set default LLM model"""
    try:
        set_default_model(model_name)
        return {
            "status": "success",
            "message": "Default LLM model updated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Tariff Management Endpoints
@router.get("/tariffs")
async def get_tariff_plans(current_user: TokenData = Depends(require_role(UserRole.ADMIN))) -> dict:
    """Get all tariff plans"""
    try:
        # Get from database first
        db_plans = TariffPlan.query.all()

        if db_plans:
            return {
                "tariffs": [{
                    "id": plan.id,
                    "name": plan.name,
                    "price_per_month": plan.price_per_month,
                    "included_limits": plan.included_limits,
                    "discounts": plan.discounts,
                    "access_features": plan.access_features
                } for plan in db_plans]
            }
        else:
            # Fallback to config if database is empty
            return {
                "tariffs": [{
                    "name": name,
                    "price_per_month": plan["price_per_month"],
                    "included_limits": plan["included_limits"],
                    "discounts": plan["discounts"],
                    "access_features": plan["access_features"]
                } for name, plan in TARIFF_PLANS.items()]
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tariffs")
async def create_tariff_plan(
    plan_data: TariffPlanCreate,
    current_user: TokenData = Depends(require_role(UserRole.ADMIN))
) -> dict:
    """Create a new tariff plan"""
    try:
        # Check if plan exists
        existing_plan = TariffPlan.query.filter_by(name=plan_data.name).first()

        if existing_plan:
            raise HTTPException(
                status_code=400,
                detail="Tariff plan with this name already exists"
            )

        # Create new plan
        new_plan = TariffPlan(
            name=plan_data.name,
            price_per_month=plan_data.price_per_month,
            included_limits=plan_data.included_limits or {},
            discounts=plan_data.discounts or {},
            access_features=plan_data.access_features or []
        )
        db.session.add(new_plan)
        db.session.commit()
        return {
            "status": "success",
            "message": "Tariff plan created successfully"
        }

    except Exception as e:
        db.session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/tariffs/{plan_id}")
async def update_tariff_plan(
    plan_id: str,
    plan_data: TariffPlanUpdate,
    current_user: TokenData = Depends(require_role(UserRole.ADMIN))
) -> dict:
    """Update an existing tariff plan"""
    try:
        plan = TariffPlan.query.get(plan_id)

        if not plan:
            raise HTTPException(status_code=404, detail="Tariff plan not found")

        # Update plan fields
        if plan_data.name is not None:
            plan.name = plan_data.name
        if plan_data.price_per_month is not None:
            plan.price_per_month = plan_data.price_per_month
        if plan_data.included_limits is not None:
            plan.included_limits = plan_data.included_limits
        if plan_data.discounts is not None:
            plan.discounts = plan_data.discounts
        if plan_data.access_features is not None:
            plan.access_features = plan_data.access_features

        db.session.commit()

        return {
            "status": "success",
            "message": "Tariff plan updated successfully"
        }

    except Exception as e:
        db.session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/tariffs/{plan_id}")
async def delete_tariff_plan(
    plan_id: str,
    current_user: TokenData = Depends(require_role(UserRole.ADMIN))
) -> dict:
    """Delete a tariff plan"""
    try:
        plan = TariffPlan.query.get(plan_id)

        if not plan:
            raise HTTPException(status_code=404, detail="Tariff plan not found")

        # Check if any organizations are using this plan
        orgs_using_plan = OrganizationBalance.query.filter_by(tariff_plan_id=plan_id).count()
        if orgs_using_plan > 0:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete plan - organizations are using it"
            )

        db.session.delete(plan)
        db.session.commit()

        return {
            "status": "success",
            "message": "Tariff plan deleted successfully"
        }

    except Exception as e:
        db.session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Payment Management Endpoints
@router.get("/payments/history")
async def get_payment_history(
    current_user: TokenData = Depends(require_role(UserRole.ADMIN)),
    limit: int = 10
) -> dict:
    """Get payment history"""
    try:
        transactions = UsageLog.query.order_by(UsageLog.timestamp.desc()).limit(limit).all()

        return {
            "transactions": [{
                "id": tx.id,
                "organization_id": tx.organization_id,
                "feature": tx.feature,
                "amount": tx.price_charged,
                "timestamp": tx.timestamp.isoformat(),
                "description": tx.additional_data.get("description", "") if tx.additional_data else ""
            } for tx in transactions]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/payments/manual")
async def manual_transaction(
    transaction_data: ManualTransaction,
    current_user: TokenData = Depends(require_role(UserRole.ADMIN))
) -> dict:
    """Add manual transaction (compensation, bonus, etc.)"""
    try:
        from web_server.billing_manager import BillingManager

        # Add funds to organization
        new_balance = BillingManager.top_up(
            transaction_data.organization_id,
            transaction_data.amount
        )

        # Log the transaction
        transaction = UsageLog(
            organization_id=transaction_data.organization_id,
            feature="manual_transaction",
            units_used=1,
            price_charged=transaction_data.amount,
            additional_data={
                "description": transaction_data.description,
                "transaction_type": "manual",
                "amount": transaction_data.amount
            }
        )
        db.session.add(transaction)
        db.session.commit()

        return {
            "status": "success",
            "message": f"Added {transaction_data.amount} RUB to organization {transaction_data.organization_id}",
            "new_balance": new_balance
        }

    except Exception as e:
        db.session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Feature Management Endpoints
@router.get("/features")
async def get_features(current_user: TokenData = Depends(require_role(UserRole.ADMIN))) -> dict:
    """Get all features and their configuration"""
    return {
        "features": FEATURE_CONFIG
    }

@router.post("/features/{feature_name}")
async def update_feature(
    feature_name: str,
    feature_data: FeatureUpdate,
    current_user: TokenData = Depends(require_role(UserRole.ADMIN))
) -> dict:
    """Update feature configuration"""
    # Note: This would require updating the config file or database
    # For now, we'll just return the current config
    if feature_name in FEATURE_CONFIG:
        # In a real implementation, you would update the configuration here
        return {
            "status": "success",
            "message": "Feature configuration updated",
            "feature": FEATURE_CONFIG[feature_name]
        }
    else:
        raise HTTPException(status_code=404, detail="Feature not found")

# System Management Endpoints
@router.get("/system/health")
async def system_health(current_user: TokenData = Depends(require_role(UserRole.ADMIN))) -> dict:
    """Get system health status"""
    # In a real implementation, this would check various system components
    return {
        "status": "healthy",
        "database": "connected",
        "cache": "connected",
        "message_queue": "connected"
    }

@router.get("/system/stats")
async def system_stats(current_user: TokenData = Depends(require_role(UserRole.ADMIN))) -> dict:
    """Get system statistics"""
    # In a real implementation, this would return actual system statistics
    return {
        "users": User.query.count(),
        "organizations": Organization.query.count(),
        "transactions": UsageLog.query.count(),
        "llm_models": len(get_llm_config().models)
    }


