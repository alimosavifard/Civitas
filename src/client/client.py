# src/client/client.py

class ClientApp:
    def __init__(self):
        print("ClientApp initialized - sending requests")

    def run(self):
        print("ClientApp running - enter requests")
        while True:
            cmd = input("ClientApp> ")
            if cmd in ['exit', 'quit']:
                print("Stopping ClientApp.")
                break
            print(f"Sent request: {cmd}")
