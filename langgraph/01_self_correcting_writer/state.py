from typing import TypedDict, Optional

class WriterState(TypedDict):
    """
    The shared state passed between the nodes in the graph.
    """
    topic: str
    draft: Optional[str]
    critique: Optional[str]
    iteration_count: int
