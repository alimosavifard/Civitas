# src/common/neuron.py
from signal import Signal

class Neuron:
    def __init__(self, neuron_id: str):
        self.neuron_id = neuron_id
        self.state = {}
        self.connections = []  # List of connected nodesل

    def receive_signal(self, signal: Signal):
        print(f"Neuron {self.neuron_id} received: {signal}")
        # Do the signal processing here

    def send_signal(self) -> list[Signal]:
        # Send output signals (if needed)
        return []

    def connect(self, neuron):
        self.connections.append(neuron)
