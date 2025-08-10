# src/node/manager.py
import asyncio
from typing import Dict, Callable
from src.node.neuron import Neuron
from src.common.signal import Signal

class NeuronManager:
    def __init__(self, node_id: str, mqtt_publish_func: Callable[[Signal], None]):
        self.node_id = node_id
        self.neurons: Dict[str, Neuron] = {}         # key: neuron_id (like "N1")
        self.tasks: Dict[str, asyncio.Task] = {}
        self.mqtt_publish = mqtt_publish_func        # async callable to publish Signal
        self.lock = asyncio.Lock()

    async def spawn_neuron(self, neuron_id: str, threshold: float = 1.0):
        full_id = f"{self.node_id}:{neuron_id}"
        n = Neuron(full_id, threshold=threshold)
        self.neurons[neuron_id] = n
        # pass a coroutine to publish (wrap to send as JSON on topic)
        async def publish_wrapper(signal: Signal):
            # delegate to provided mqtt_publish (should accept Signal)
            await self.mqtt_publish(signal)
        task = asyncio.create_task(n.run(publish_wrapper))
        self.tasks[neuron_id] = task

    async def route_signal(self, signal: Signal):
        """
        route incoming signal to local neuron queue or publish to another node if not local
        signal.receiver: "nodeX:N3"
        """
        # parse receiver
        try:
            node, neuron = signal.receiver.split(":", 1)
        except ValueError:
            return
        if node == self.node_id:
            # local delivery
            n = self.neurons.get(neuron)
            if n:
                await n.in_queue.put(signal)
        else:
            # not local — publish as-is (this manager's mqtt_publish should handle)
            await self.mqtt_publish(signal)

    async def autoscale_loop(self):
        # very simple autoscale: if any queue > threshold, spawn one more neuron of same type
        while True:
            async with self.lock:
                for nid, n in list(self.neurons.items()):
                    qsize = n.in_queue.qsize()
                    if qsize > 20:  # threshold — tune in real use
                        # spawn extra neuron with suffix
                        new_id = f"{nid}_s{int(time.time())%10000}"
                        await self.spawn_neuron(new_id, threshold=n.threshold)
            await asyncio.sleep(5)
