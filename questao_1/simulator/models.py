from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Processe:
    """
    Representa um processo na simulação.
    """
    pid: str
    arrival_time: int
    burst_time: int
    remaining_time: int = field(init=False)
    start_time: Optional[int] = None
    finish_time: Optional[int] = None
    waiting_time: int = 0
    turnaround_time: int = 0

    def __post_init__(self):
        self.remaining_time = self.burst_time