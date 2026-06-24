"""
Access decision utilities.

This module converts recognition results into access-control
decisions that can later be used by the UI, logger, and hardware layer.
"""

from dataclasses import dataclass


@dataclass
class AccessDecision:
    """
    Final access-control decision.
    """

    user_name: str
    access_granted: bool
    reason: str


class AccessDecisionManager:
    """
    Decide whether access should be granted or denied.
    """

    def decide(
        self,
        user_name: str | None,
        access_granted: bool,
    ) -> AccessDecision:
        """
        Convert raw recognition output into a clean access decision.
        """

        if access_granted and user_name:
            return AccessDecision(
                user_name=user_name,
                access_granted=True,
                reason="recognized_authorized_user",
            )

        return AccessDecision(
            user_name="Unknown",
            access_granted=False,
            reason="unknown_or_below_threshold",
        )