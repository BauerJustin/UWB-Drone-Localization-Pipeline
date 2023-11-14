import json

class Capture:
    def __init__(self, file_name):
        self.file_name = file_name

    def write_stream(self, stream):
        print(f"Saving capture to {self.file_name}")
        with open(self.file_name, "w") as file:
            json.dump(stream, file)
        print("Capture saved")