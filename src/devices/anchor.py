class Anchor:
    def __init__(self, id, x, y ,z):
        self.id = id
        self.x, self.y, self.z = x, y, z

    def get_position(self):
        return (self.x, self.y, self.z)
    