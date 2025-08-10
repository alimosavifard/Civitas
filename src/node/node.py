# src/node/node.py

import time
from common.signal import Signal
from common.neuron import Neuron

class NodeApp:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.neurons = []
        self.setup_neurons()

    def setup_neurons(self):
        # ایجاد سه نورون نمونه و اتصال آنها
        neuron1 = Neuron("N1")
        neuron2 = Neuron("N2")
        neuron3 = Neuron("N3")

        neuron1.connect(neuron2)
        neuron2.connect(neuron3)

        self.neurons = [neuron1, neuron2, neuron3]

    def run(self):
        print(f"Node {self.node_id} running with {len(self.neurons)} neurons.")
        try:
            while True:
                # تولید سیگنال اولیه توسط نورون اول
                signal = Signal(signal_id="sig1", category="test", payload="Hello")
                print(f"Node {self.node_id} sending signal: {signal}")

                # نورون اول سیگنال را پردازش می‌کند و سیگنال پاسخ تولید می‌کند
                response_signal = self.neurons[0].receive_signal(signal)

                # ارسال سیگنال پاسخ به نورون‌های متصل
                for connected_neuron in self.neurons[0].connections:
                    print(f"Sending signal to {connected_neuron.neuron_id}")
                    resp = connected_neuron.receive_signal(response_signal)
                    print(f"Response from {connected_neuron.neuron_id}: {resp}")

                time.sleep(5)  # تاخیر برای حلقه بعدی

        except KeyboardInterrupt:
            print("Node shutting down.")

if __name__ == "__main__":
    node = NodeApp("node_1")
    node.run()
