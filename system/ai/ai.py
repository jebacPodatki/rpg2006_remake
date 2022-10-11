import random
from system.core.action.action import *
from system.core.action.selector import *
from system.core.action.helper import *
from system.core.character import *

class AIActionSelector(ActionSelectorInterface):
    def select(self, character : Character, character_list, helper):
        selected_spell_name = ''
        for i in range(0, len(character.sheet.spells)):
            if helper.can_use(character, character.sheet.spells[i]) and \
                random.randint(1, 100) < character.sheet.spells_ai_chance[i]:
                selected_spell_name = character.sheet.spells[i]
        target_groups = helper.get_possible_targets(character, selected_spell_name)
        if len(target_groups) == 0:
            selected_targets = []
        elif len(target_groups) == 1:
            if len(target_groups[0]) >= 1:
                selected_targets = target_groups[0]
            else:
                selected_targets = []
        else:
            index = random.randint(0, len(target_groups) - 1)
            selected_targets = target_groups[index]
        if selected_spell_name == '':
            if len(selected_targets) == 0:
                return Action(Action.ACTION_WAIT, character, [], '')
            else:
                return Action(Action.ACTION_ATTACK, character, selected_targets, '')
        else:
            return Action(Action.ACTION_MAGIC, character, selected_targets, selected_spell_name)