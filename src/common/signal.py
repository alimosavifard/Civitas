# src/common/signal.py

class Signal:
    def __init__(self, signal_id: str, category: str, payload: any, metadata: dict = None):
       
		signal_id: Unique identifier for the signal
		category: Type of signal (e.g. 'emotion', 'request', 'vision', ...)
		payload: The main data of the signal, can be of any type
		metadata: Additional information such as time, intensity, source, etc....
        
        self.signal_id = signal_id
        self.category = category
        self.payload = payload
        self.metadata = metadata or {}

    def __repr__(self):
        return f"<Signal id={self.signal_id} category={self.category} payload={self.payload}>"
