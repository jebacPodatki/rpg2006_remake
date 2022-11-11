from misc.decorators import *

@fromJson()
@deserialize()
class SceneProperties:
    def __init__(self):
        self.sprite_pos = [0, 0]
        self.sprite_image = ''