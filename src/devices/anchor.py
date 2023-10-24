from src.utils import Position

class Anchor:
    def __init__(self, id, x, y ,z):
        self.id = id
        self.pos = Position(x, y, z)

    def get_pos(self):
        return self.pos
    