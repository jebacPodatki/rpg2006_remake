from misc.decorators import *

@deserialize()
class Race:
    def __init__(self):
        self.name = ''
        self.classes = []