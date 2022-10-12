from system.core.character import *
from system.core.action.action import *
from system.core.action.helper import *

class ActionSelectorInterface:
    def select(self, character : Character, helper : ActionHelper):
        return Action(Action.ACTION_NONE, None, [], '')