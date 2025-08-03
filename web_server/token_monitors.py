











"""
Token Monitors for AI Backlog Assistant
"""

from .token_billing_manager import TokenBasedBillingManager

class InputTokenMonitor:
    """
    Monitor for input tokens.
    """

    def __init__(self, organization_id: str, user_id: str):
        self.organization_id = organization_id
        self.user_id = user_id

    def monitor(self, tokens: int):
        """
        Monitor input tokens and charge for usage.
        """
        TokenBasedBillingManager.charge_tokens(
            self.organization_id,
            input_tokens=tokens,
            llm_tokens=0,
            output_tokens=0,
            user_id=self.user_id
        )

class LLMTokenMonitor:
    """
    Monitor for LLM tokens.
    """

    def __init__(self, organization_id: str, user_id: str):
        self.organization_id = organization_id
        self.user_id = user_id

    def monitor(self, tokens: int):
        """
        Monitor LLM tokens and charge for usage.
        """
        TokenBasedBillingManager.charge_tokens(
            self.organization_id,
            input_tokens=0,
            llm_tokens=tokens,
            output_tokens=0,
            user_id=self.user_id
        )

class OutputTokenMonitor:
    """
    Monitor for output tokens.
    """

    def __init__(self, organization_id: str, user_id: str):
        self.organization_id = organization_id
        self.user_id = user_id

    def monitor(self, tokens: int):
        """
        Monitor output tokens and charge for usage.
        """
        TokenBasedBillingManager.charge_tokens(
            self.organization_id,
            input_tokens=0,
            llm_tokens=0,
            output_tokens=tokens,
            user_id=self.user_id
        )

class CombinedTokenMonitor:
    """
    Monitor for all token types combined.
    """

    def __init__(self, organization_id: str, user_id: str):
        self.organization_id = organization_id
        self.user_id = user_id

    def monitor(self, input_tokens: int, llm_tokens: int, output_tokens: int):
        """
        Monitor all token types and charge for usage.
        """
        TokenBasedBillingManager.charge_tokens(
            self.organization_id,
            input_tokens=input_tokens,
            llm_tokens=llm_tokens,
            output_tokens=output_tokens,
            user_id=self.user_id
        )


