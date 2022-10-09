from misc.decorators import *

@fromJson()
@deserialize()
class Config:
    def __init__(self):
        self.window_size = [0, 0]
        self.print_font = ''
        self.print_font_size = 0