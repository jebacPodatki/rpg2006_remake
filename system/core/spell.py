from system.core.action.target import *
from misc.decorators import *

@deserialize()
class Spell:
    def __init__(self):
        self.name = ''
        self.impact = [0, 0]
        self.dmg = [0, 0]
        self.effect = ''
        self.mp_cost = 0
        self.target = ActionTarget.TARGET_NONE