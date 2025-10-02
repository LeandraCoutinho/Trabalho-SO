from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Process:
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
    turnaround_time_process: int = 0

    def __post_init__(self):
        self.remaining_time = self.burst_time

    @property
    def turnaround_time(self) -> Optional[int]:
        """Calcula o tempo de retorno (Turnaround Time)."""
        if self.finish_time is not None:
            return self.finish_time - self.arrival_time
        return None

    @property
    def response_time(self) -> Optional[int]:
        """Calcula o tempo de resposta (Response Time)."""
        if self.start_time is not None:
            return self.start_time - self.arrival_time
        return None