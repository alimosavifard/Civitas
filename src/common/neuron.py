class Signal:
    def __init__(self, signal_id: str, category: str, payload: any, metadata: dict = None):
        self.signal_id = signal_id
        self.category = category
        self.payload = payload
        self.metadata = metadata or {}

class Neuron:
    def __init__(self, neuron_id: str):
        self.neuron_id = neuron_id
        self.state = {}
        self.connections = []

    def receive_signal(self, signal: Signal):
        print(f"Neuron {self.neuron_id} received signal: {signal.category} with payload: {signal.payload}")

    def send_signal(self):
        # Example of sending output signal
        return []
