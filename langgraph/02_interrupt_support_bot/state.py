from typing import TypedDict

class SupportState(TypedDict):
    """
    The shared state for the support ticket.
    """
    user_query: str
    refund_amount: float
    status: str
