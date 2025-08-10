# src/node/node.py
import asyncio
import json
import time
from paho.mqtt import client as mqtt_client
from src.common.signal import Signal
from src.common.mqtt_client import create_mqtt_client
from src.node.manager import NeuronManager

BROKER = 'localhost'
PORT = 1883
TOPIC_SIGNAL = "civitas/signals/#"        # wildcard to receive signals; we'll filter by receiver
TOPIC_NODE_STATUS = "civitas/node/{node_id}/status"
TOPIC_PUBLISH_SIGNAL = "civitas/signals/{receiver}"  # receiver is full id like node:neuron

class NodeApp:
    def __init__(self, node_id: str, broker: str = BROKER, port: int = PORT):
        self.node_id = node_id
        self.client = create_mqtt_client(broker, port, client_prefix=f"node-{node_id}")
        self.loop = asyncio.get_event_loop()
        # async publish uses loop.run_in_executor to call paho publish
        async def mqtt_publish(signal: Signal):
            topic = TOPIC_PUBLISH_SIGNAL.format(receiver=signal.receiver)
            self.client.publish(topic, signal.to_json())
        self.manager = NeuronManager(node_id, mqtt_publish)
        self._setup_handlers()

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("[node] connected to broker")
            # subscribe to all signals targeted to this node
            topic = f"civitas/signals/{self.node_id}/#"
            client.subscribe(topic)
            # also subscribe to direct signals that use "node:neuron" topic form
            client.subscribe("civitas/signals/+/+")
        else:
            print("[node] bad connection, rc:", rc)

    def _on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode()
            sig = Signal.from_json(payload)
        except Exception as e:
            print("failed parse signal:", e)
            return
        # We don't block in MQTT callback — route to asyncio loop
        asyncio.run_coroutine_threadsafe(self.manager.route_signal(sig), self.loop)

    def _setup_handlers(self):
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def start_mqtt(self):
        # start network loop in background thread
        self.client.loop_start()

    async def register_and_run(self):
        # register with GodNode by publishing status (simple)
        status_topic = TOPIC_NODE_STATUS.format(node_id=self.node_id)
        self.client.publish(status_topic, json.dumps({"node_id": self.node_id, "status": "online", "timestamp": time.time()}))

        # spawn some default neurons from config (simple demo)
        await self.manager.spawn_neuron("N1", threshold=1.0)
        await self.manager.spawn_neuron("N2", threshold=1.5)
        await self.manager.spawn_neuron("N3", threshold=1.0)

        # connect some synapses (local or cross-node via full ids)
        # format full ids: node:neuron
        self.manager.neurons["N1"].connect(f"{self.node_id}:N2", weight=1.0)
        self.manager.neurons["N2"].connect(f"{self.node_id}:N3", weight=1.0)
        # example cross-node synapse (comment/uncomment if another node exists)
        # self.manager.neurons["N3"].connect("node_other:N1", weight=0.8)

        # start autoscale loop
        asyncio.create_task(self.manager.autoscale_loop())

        # keep the event loop alive (neurons run as tasks)
        while True:
            await asyncio.sleep(1)

    def run(self):
        self.start_mqtt()
        # run asyncio main in current thread
        try:
            self.loop.run_until_complete(self.register_and_run())
        except KeyboardInterrupt:
            print("shutting down node")
            self.client.loop_stop()
            for t in self.manager.tasks.values():
                t.cancel()
