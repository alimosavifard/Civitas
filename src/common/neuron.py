# src/common/neuron.py

from signal import Signal

class Neuron:
    def __init__(self, neuron_id: str, filters=None):
        self.neuron_id = neuron_id
        self.state = {}
        self.connections = []  # نورون‌های متصل
        self.filters = filters if filters else []

    def receive_signal(self, signal: Signal):
        print(f"Neuron {self.neuron_id} received: {signal}")

        # بررسی فیلترها: اگر یکی از فیلترها سیگنال را رد کرد، سیگنال پردازش نشود
        for f in self.filters:
            if not f(signal):
                print(f"Signal {signal.signal_id} rejected by filter in {self.neuron_id}")
                return None

        # منطق پردازش (مثلاً تغییر payload)
        processed_payload = f"Processed by {self.neuron_id}: {signal.payload}"
        response_signal = Signal(
            signal_id=f"{signal.signal_id}_resp_from_{self.neuron_id}",
            category=signal.category,
            payload=processed_payload,
            metadata={"processed_by": self.neuron_id}
        )
        return response_signal

    def connect(self, neuron):
        self.connections.append(neuron)
