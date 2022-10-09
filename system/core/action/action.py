from system.core.character import Character

class Action:
    ACTION_NONE = 0
    ACTION_ATTACK = 1
    ACTION_MAGIC = 2
    ACTION_WAIT = 3
    ACTION_MOVE = 4
    def __init__(self, type, actor : Character, targets, spell_name):
        self.type = type
        self.actor = actor
        self.targets = targets
        self.spell_name = spell_name