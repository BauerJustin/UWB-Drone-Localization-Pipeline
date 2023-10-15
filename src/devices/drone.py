class Drone:
    def __init__(self, id):
        self.id = id
        self.x = None
        self.y = None
        self.z = None

    def update_pos(self, tofs):
        print(f"[Drone-{self.id}] Update pos: {tofs}")
