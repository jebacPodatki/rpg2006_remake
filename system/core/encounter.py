from misc.decorators import *

@deserialize()
class Encounter:
    def __init__(self):
        self.name = ''
        self.front_line = []
        self.back_line = []