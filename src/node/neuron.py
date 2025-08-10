# src/node/neuron.py
import asyncio
import time
import random
from typing import Dict, List
from src.common.signal import Signal

class Neuron:
    def __init__(self, full_id: str, threshold: float = 1.0):
        """
        full_id: "node_id:neuron_id"
        """
        self.id = full_id
        self.threshold = threshold
        self.potential = 0.0
        self.in_queue: asyncio.Queue = asyncio.Queue()
        # synapses: receiver_full_id -> weight, delay in seconds optional in metadata
        self.synapses: Dict[str, float] = {}

    def connect(self, target_full_id: str, weight: float = 1.0):
        self.synapses[target_full_id] = weight

    async def run(self, publish_callable):
        """ main loop: read signals, accumulate potential, fire when threshold reached.
            publish_callable(signal_json) -> publishes signal via MQTT (or routes locally)
        """
        while True:
            sig: Signal = await self.in_queue.get()
            # accumulate potential proportional to signal.weight
            self.potential += float(sig.weight)
            # optional: time-decay could be applied here
            if self.potential >= self.threshold:
                # create output signals for each synapse
                ts = time.time()
                for target, w in self.synapses.items():
                    out = Signal(
                        signal_id=f"{self.id}_to_{target}_{int(ts*1000)}",
                        sender=self.id,
                        receiver=target,
                        weight=w,
                        payload=f"fired_by:{self.id}",
                        timestamp=ts,
                        metadata={"origin": self.id}
                    )
                    # publish (async-safe wrapper expected)
                    await publish_callable(out)
                # reset potential (leaky reset could be used)
                self.potential = 0.0
            # small sleep to yield
            await asyncio.sleep(0)
