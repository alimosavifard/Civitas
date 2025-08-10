# src/god/god_node.py

class GodNode:
    def __init__(self):
        print("GodNode initialized - central controller")

    def run(self):
        print("GodNode running - managing rules and node map")
        # In the future, API and rules management will be implemented here
        while True:
            cmd = input("GodNode> ")
            if cmd in ['exit', 'quit']:
                print("Stopping GodNode.")
                break
            print(f"Received command: {cmd}")
