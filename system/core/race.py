from misc.decorators import *

@deserialize()
class Race:
    def __init__(self):
        self.name = ''
        self.portrait = ''
        self.classes = []