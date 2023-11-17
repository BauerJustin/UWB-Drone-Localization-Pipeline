import json

class StreamCapture:
    def __init__(self, file_name, replay=False):
        self.file_name = file_name
        self.replay = replay

    def write_stream(self, stream):
        with open(f'./captures/{self.file_name}', "w") as file:
            json.dump(stream, file)

    def read_stream(self):
        try:
            with open(f'./captures/{self.file_name}', "r") as file:
                stream = json.load(file)
                return stream
        except FileNotFoundError:
            print(f"File '{f'./captures/{self.file_name}'}' not found.")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
