from system.core.action.action import *
from system.core.action.selector import *
from system.core.action.helper import *
from system.core.character import *

class ConsoleSelector(ActionSelector):
    def select(self, character : Character, characterList, helper):
        print('\033[94m')
        print('Current character: ' + character.sheet.name)
        print('Action: 1 - Attack, 2 - Magic, 3 - Wait, 4 - Move.: ', end = ' ')
        action = int(input())
        if action == 3:
            return Action(Action.ACTION_WAIT, character, [], '')
        if action == 4:
            if helper.can_move(character):
                return Action(Action.ACTION_MOVE, character, [], '')
            else:
                return Action(Action.ACTION_WAIT, character, [], '')
        selected_spell = ''
        if action == 2:
            msg = 'Choose spell: '
            i = 1
            for spell in character.sheet.spells:
                if helper.can_use(character, spell):
                    msg += str(i) + ' - ' + spell + ', '
                    i += 1
            if i > 1:                
                print(msg + ': ', end = " ")
                selected_spell = character.sheet.spells[int(input()) - 1]
            else:
                print("No spells", end = " ")
                action = 1
        target_groups = helper.get_possible_targets(character, selected_spell)
        if len(target_groups) == 0:
            selected_targets = []
        elif len(target_groups) == 1:
            if len(target_groups[0]) >= 1:
                selected_targets = target_groups[0]
            else:
                selected_targets = []
        else:
            msg = 'Choose target: '
            i = 1
            for target_group in target_groups:
                if len(target_group) == 1:
                    msg += str(i) + ' - ' + target_group[0].sheet.name + ', '
                else:
                    msg += str(i) + ' - ('
                    for target in target_group:
                        msg += target.sheet.name + ', '
                    msg += '),'
                i += 1
            print(msg + ': ', end = " ")
            selected_targets = [target_groups[int(input()) - 1][0]]
        if action == 1:
            return Action(Action.ACTION_ATTACK, character, selected_targets, '')
        else:
            return Action(Action.ACTION_MAGIC, character, selected_targets, selected_spell) 