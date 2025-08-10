import argparse
from node.node import NodeApp
from client.client import ClientApp

def main():
    parser = argparse.ArgumentParser(description="Civitas Neural Network Node/Client")
    parser.add_argument("--mode", choices=["node", "client"], required=True)
    parser.add_argument("--id", default="node_1")
    parser.add_argument("--neurons", type=int, default=5, help="Number of neurons in this node")
    args = parser.parse_args()

    if args.mode == "node":
        node = NodeApp(node_id=args.id, neuron_count=args.neurons)
        node.connect_to_god()
        node.run()
    elif args.mode == "client":
        client = ClientApp(client_id=args.id)
        client.run()
