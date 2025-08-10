# node/neuron.py
import asyncio
import random
from common.signal import Signal

class Neuron:
    def __init__(self, neuron_id, role, queue, threshold=1.0):
        self.id = neuron_id
        self.role = role
        self.queue = queue
        self.potential = 0
        self.threshold = threshold

    async def run(self):
        while True:
            signal = await self.queue.get()
            self.potential += signal.strength
            if self.potential >= self.threshold:
                await self.fire()
                self.potential = 0

    async def fire(self):
        print(f"[{self.id}] firing signal!")
        # اینجا میشه سیگنال رو به نورون بعدی یا GodNode فرستاد
        await asyncio.sleep(random.uniform(0.1, 0.5))
