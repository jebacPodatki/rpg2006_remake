from misc.decorators import *

@fromJson()
@deserialize()
class Config:
    def __init__(self):
        self.window_size = [0, 0]
        self.fps_limit = 0
        self.system_update_delay = 0