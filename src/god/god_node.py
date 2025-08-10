# src/god/god_node.py
import json
import time
import asyncio
from fastapi import FastAPI
import uvicorn
from paho.mqtt import client as mqtt_client
from src.common.mqtt_client import create_mqtt_client

BROKER='localhost'
PORT=1883
PUB_RULES_TOPIC = "civitas/rules"
NODE_STATUS_TOPIC = "civitas/node/+/status"

app = FastAPI()
rules = {"global_threshold": 1.0, "announce_interval": 30}
node_map = {}

# MQTT client for publish/subscribe
mqttc = create_mqtt_client(BROKER, PORT, client_prefix="god")

def on_connect(client, userdata, flags, rc):
    print("[god] mqtt connected")
    client.subscribe(NODE_STATUS_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)
        # topic like civitas/node/{node_id}/status
        topic_parts = msg.topic.split('/')
        node_id = topic_parts[2] if len(topic_parts) >= 3 else "unknown"
        node_map[node_id] = data
        print(f"[god] status update from {node_id}: {data}")
    except Exception as e:
        print("god on_message error:", e)

mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.loop_start()

# publish rules periodically
async def announce_rules_loop():
    while True:
        mqttc.publish(PUB_RULES_TOPIC, json.dumps(rules))
        await asyncio.sleep(rules.get("announce_interval", 30))

@app.get("/rules")
def get_rules():
    return rules

@app.post("/rules")
def set_rules(new: dict):
    rules.update(new)
    # publish updated rules immediately
    mqttc.publish(PUB_RULES_TOPIC, json.dumps(rules))
    return {"status":"ok","rules":rules}

@app.get("/nodes")
def get_nodes():
    return node_map

if __name__ == "__main__":
    mqttc.connect(BROKER, PORT)
    loop = asyncio.get_event_loop()
    loop.create_task(announce_rules_loop())
    uvicorn.run(app, host="0.0.0.0", port=8000)
