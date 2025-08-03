










"""
Token-Based Billing Manager for AI Backlog Assistant
"""

import uuid
from datetime import datetime
from .app import db
from .billing_models import OrganizationBalance, UsageLog, TariffPlan
from .billing_manager import BillingException

class TokenBasedBillingManager:
    """
    Manager for token-based billing, including input, LLM, and output tokens.
    """

    @staticmethod
    def calculate_token_cost(input_tokens: int, llm_tokens: int, output_tokens: int) -> float:
        """
        Calculate the cost based on token usage.
        """
        # Example pricing - adjust as needed
        INPUT_TOKEN_PRICE = 0.0001  # 0.0001 RUB per input token
        LLM_TOKEN_PRICE = 0.0005    # 0.0005 RUB per LLM token
        OUTPUT_TOKEN_PRICE = 0.0001 # 0.0001 RUB per output token

        total_cost = (input_tokens * INPUT_TOKEN_PRICE +
                      llm_tokens * LLM_TOKEN_PRICE +
                      output_tokens * OUTPUT_TOKEN_PRICE)

        return total_cost

    @staticmethod
    def charge_tokens(organization_id: str, input_tokens: int, llm_tokens: int, output_tokens: int, user_id: str) -> float:
        """
        Charge for token usage, checking balance and limits.
        """
        # Calculate total cost
        total_cost = TokenBasedBillingManager.calculate_token_cost(input_tokens, llm_tokens, output_tokens)

        # Check balance
        org_balance = OrganizationBalance.query.get(organization_id)
        if not org_balance:
            raise BillingException("Organization not found")

        if org_balance.balance_rub < total_cost:
            raise BillingException("Insufficient balance")

        # Deduct from balance
        org_balance.balance_rub -= total_cost
        org_balance.last_updated = datetime.utcnow()

        # Log usage
        usage_log = UsageLog(
            id=str(uuid.uuid4()),
            organization_id=organization_id,
            user_id=user_id,
            feature="token_usage",
            units_used=1,  # Count as one usage event
            tokens_used=input_tokens + llm_tokens + output_tokens,
            price_charged=total_cost,
            timestamp=datetime.utcnow(),
            additional_data={
                "input_tokens": input_tokens,
                "llm_tokens": llm_tokens,
                "output_tokens": output_tokens
            }
        )

        db.session.add(usage_log)
        db.session.commit()

        return total_cost

    @staticmethod
    def log_token_usage(organization_id: str, input_tokens: int, llm_tokens: int, output_tokens: int, user_id: str):
        """
        Log token usage without charging (for informational purposes).
        """
        usage_log = UsageLog(
            id=str(uuid.uuid4()),
            organization_id=organization_id,
            user_id=user_id,
            feature="token_usage",
            units_used=1,
            tokens_used=input_tokens + llm_tokens + output_tokens,
            price_charged=0.0,  # No charge
            timestamp=datetime.utcnow(),
            additional_data={
                "input_tokens": input_tokens,
                "llm_tokens": llm_tokens,
                "output_tokens": output_tokens
            }
        )

        db.session.add(usage_log)
        db.session.commit()

