# src/common/mqtt_client.py
import uuid
from paho.mqtt import client as mqtt_client

def create_mqtt_client(broker: str='localhost', port: int=1883, client_prefix: str='civitas'):
    client_id = f"{client_prefix}-{uuid.uuid4()}"
    client = mqtt_client.Client(client_id)
    client.connect(broker, port)
    return client
