import argparse
from src.god.god_node import GodNode
from src.node.node import NodeApp
from src.client.client import ClientApp

def main():
    parser = argparse.ArgumentParser(description="Civitas AI Framework")
    parser.add_argument('--mode', choices=['god', 'node', 'client'], required=True,
                        help="Run as god, node, or client")
    args = parser.parse_args()

    if args.mode == 'god':
        app = GodNode()
    elif args.mode == 'node':
        app = NodeApp()
    else:
        app = ClientApp()

    app.run()

if __name__ == '__main__':
    main()
