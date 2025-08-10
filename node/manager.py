# node/manager.py
import asyncio
from node.neuron import Neuron
from common.signal import Signal

class NeuronManager:
    def __init__(self):
        self.neurons = {}
        self.queues = {}

    async def spawn_neuron(self, neuron_id, role="generic", threshold=1.0):
        q = asyncio.Queue()
        neuron = Neuron(neuron_id, role, q, threshold)
        task = asyncio.create_task(neuron.run())
        self.neurons[neuron_id] = task
        self.queues[neuron_id] = q
        print(f"Spawned neuron {neuron_id} ({role})")

    async def send_signal(self, target_id, strength=0.5):
        if target_id in self.queues:
            await self.queues[target_id].put(Signal(strength))

    async def autoscale(self):
        while True:
            for nid, q in self.queues.items():
                if q.qsize() > 10:
                    await self.spawn_neuron(f"{nid}_extra")
            await asyncio.sleep(5)
