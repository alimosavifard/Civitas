# src/common/signal.py
from dataclasses import dataclass, asdict, field
from typing import Any, Dict
import time
import json

@dataclass
class Signal:
    signal_id: str
    sender: str                # e.g. "node1:N1" or "external"
    receiver: str              # e.g. "node2:N3"
    weight: float
    payload: Any = None
    timestamp: float = field(default_factory=lambda: time.time())
    metadata: Dict = field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @staticmethod
    def from_json(s: str) -> "Signal":
        data = json.loads(s)
        return Signal(**data)
