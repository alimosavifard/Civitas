# src/node/mqtt_node.py

import time
import json
import threading
import uuid
from paho.mqtt import client as mqtt_client
from common.signal import Signal

BROKER = 'localhost'
PORT = 1883
CLIENT_ID = f'node-{uuid.uuid4()}'
TOPIC_PREFIX = 'civitas/signals/'

class Neuron:
    def __init__(self, neuron_id, mqtt_client):
        self.neuron_id = neuron_id
        self.mqtt_client = mqtt_client

    def process_signal(self, signal: Signal):
        print(f"Neuron {self.neuron_id} processing signal: {signal}")
        # ساخت سیگنال پاسخ
        response = Signal(
            signal_id=f"{signal.signal_id}_resp_{self.neuron_id}",
            category=signal.category,
            payload=f"Processed by {self.neuron_id}: {signal.payload}",
            metadata={"processed_by": self.neuron_id}
        )
        # انتشار سیگنال پاسخ روی کانال مخصوص نورون
        topic = TOPIC_PREFIX + self.neuron_id
        self.mqtt_client.publish(topic, json.dumps(response.__dict__))
        print(f"Neuron {self.neuron_id} published response to {topic}")

class NodeApp:
    def __init__(self, node_id):
        self.node_id = node_id
        self.client = mqtt_client.Client(CLIENT_ID)
        self.neurons = [Neuron(f'N{i+1}', self.client) for i in range(3)]
        self.setup_mqtt()

    def setup_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
                # سابسکرایب به تاپیک دریافت سیگنال نود
                client.subscribe(TOPIC_PREFIX + self.node_id)
            else:
                print("Failed to connect, return code %d\n", rc)

        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            data = json.loads(msg.payload.decode())
            signal = Signal(**data)
            # ارسال سیگنال به تمام نورون‌ها برای پردازش
            for neuron in self.neurons:
                neuron.process_signal(signal)

        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.connect(BROKER, PORT)

    def run(self):
        # اجرای loop MQTT در thread جدا
        thread = threading.Thread(target=self.client.loop_forever)
        thread.start()

        # ارسال سیگنال اولیه هر ۱۰ ثانیه
        counter = 0
        try:
            while True:
                sig = Signal(
                    signal_id=f"sig_{counter}",
                    category="test",
                    payload=f"Hello from {self.node_id} #{counter}"
                )
                topic = TOPIC_PREFIX + self.node_id
                self.client.publish(topic, json.dumps(sig.__dict__))
                print(f"Published signal {sig.signal_id} to topic {topic}")
                counter += 1
                time.sleep(10)
        except KeyboardInterrupt:
            print("Node shutting down...")
            self.client.disconnect()
            thread.join()

if __name__ == "__main__":
    node = NodeApp("node_1")
    node.run()
