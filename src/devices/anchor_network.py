from .anchor import Anchor

class AnchorNetwork:
    def __init__(self):
        self.anchors = {}

    def add_anchor(self, id, x, y, z):
        anchor = Anchor(id, x, y, z)
        self.anchors[id] = anchor

    def get_anchor_pos(self, id):
        return self.anchors[id].get_pos()
        
    def get_anchor_ids(self):
        return list(self.anchors.keys())
    