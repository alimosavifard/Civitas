from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn

app = FastAPI()

# Example rules and node map (internal cache)
rules = {
    "rule_1": "No unauthorized node connections",
    "rule_2": "Update every 10 minutes"
}

node_map = {
    "node_1": {"status": "active", "last_update": "2025-08-10T20:00:00"},
    "node_2": {"status": "inactive", "last_update": "2025-08-10T19:30:00"}
}

class NodeStatus(BaseModel):
    node_id: str
    status: str
    last_update: str

@app.get("/rules")
def get_rules():
    return rules

@app.get("/node_map")
def get_node_map():
    return node_map

@app.post("/node_status")
def update_node_status(status: NodeStatus):
    node_map[status.node_id] = {
        "status": status.status,
        "last_update": status.last_update
    }
    return {"message": "Status updated"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
