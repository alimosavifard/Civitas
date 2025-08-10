# src/node/node.py

class NodeApp:
    def __init__(self):
        print("NodeApp initialized - processing signals")

    def run(self):
        print("NodeApp running - waiting for signals")
        while True:
            cmd = input("NodeApp> ")
            if cmd in ['exit', 'quit']:
                print("Stopping NodeApp.")
                break
            print(f"Received command: {cmd}")
