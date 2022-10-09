from system.core.action.target import *
from misc.decorators import *

@deserialize()
class Spell:
    def __init__(self):
        self.name = 'Magic bolt'
        self.impact = [70, 120]
        self.dmg = [60, 90]
        self.effect = ''
        self.mp_cost = 50
        self.target = ActionTarget.TARGET_SINGLE_ENEMY_BOTHLINE