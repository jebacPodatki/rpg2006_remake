from system.core.spell import Spell
from system.core.library import Library
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

class ActionHelper:
    def __init__(self, library : Library, characters):
        self.library = library
        self.characters = characters
    def can_use(self, character : Character, spell_name):
        if spell_name in self.library.spells:
            spell = self.library.spells[spell_name]
            if character.stats.mp >= spell.mp_cost:
                return True
            else:
                return False
        else:
            return False
    def can_move(self, character : Character):
        if character.line == Character.FRONT_LINE:
            if self.is_backline_empty(character.faction):
                return False
            possible = True
            character.line = Character.BACK_LINE
            if self.is_frontline_empty(character.faction):
                possible = False
            character.line = Character.FRONT_LINE
            return possible
        return True
    def is_single_target(self, spell_name):
        if spell_name in self.library.spells:
            spell = self.library.spells[spell_name]
            return spell.target == Spell.TARGET_SINGLE_ENEMY_FRONTLINE \
                or spell.target == Spell.TARGET_SINGLE_ENEMY_BOTHLINE \
                or spell.target == Spell.TARGET_SINGLE_ALLY
        else:
            return False
        
    def is_frontline_empty(self, faction):
        for chr in self.characters:
            if chr.is_alive() and chr.faction == faction and chr.line == Character.FRONT_LINE:
                return False
        return True

    def is_backline_empty(self, faction):
        for chr in self.characters:
            if chr.is_alive() and chr.faction == faction and chr.line == Character.BACK_LINE:
                return False
        return True

    def __get_possible_targets(self, character : Character, target_type, with_spell : bool):
        if target_type == Spell.TARGET_NONE:
            return []
        elif target_type == Spell.TARGET_ALL_ALLIES or target_type == Spell.TARGET_ALL_ENEMIES:
            all = []
            if target_type == Spell.TARGET_ALL_ALLIES:
                target_faction = character.faction
            else:
                target_faction = -character.faction
            for chr in self.characters:
                if chr.faction == target_faction and chr.is_alive():
                    all.append(chr)
            return [all]
        elif target_type == Spell.TARGET_SINGLE_ALLY or target_type == Spell.TARGET_SINGLE_ENEMY_BOTHLINE:
            targets = []
            if target_type == Spell.TARGET_SINGLE_ALLY:
                target_faction = character.faction
            else:
                target_faction = -character.faction
            for chr in self.characters:
                if chr.faction == target_faction and chr.is_alive():
                    targets.append([chr])
            return targets
        elif target_type == Spell.TARGET_ALL_ENEMIES_FRONTLINE:
            if self.is_frontline_empty(-character.faction):
                return self.get_possible_targets(character, Spell.TARGET_ALL_ENEMIES)
            if character.line == Character.BACK_LINE and not character.sheet.distant and with_spell == False:
                return []
            all = []
            for chr in self.characters:
                if chr.faction == -character.faction and chr.is_alive() and chr.line == Character.FRONT_LINE:
                    all.append(chr)
            return [all]
        elif target_type == Spell.TARGET_SINGLE_ENEMY_FRONTLINE:
            if self.is_frontline_empty(-character.faction):
                return self.get_possible_targets(character, Spell.TARGET_SINGLE_ENEMY_BOTHLINE)
            if character.line == Character.BACK_LINE and not character.sheet.distant and with_spell == False:
                return []
            targets = []
            for chr in self.characters:
                if chr.faction == -character.faction and chr.is_alive() and chr.line == Character.FRONT_LINE:
                    targets.append([chr])
            return targets

    def get_possible_targets(self, character : Character, spell_name = ''):
        uses_spell = False
        if spell_name == '':
            target_type = character.sheet.attack_area
        else:
            if spell_name in self.library.spells:
                spell = self.library.spells[spell_name]
            else:
                return []
            target_type = spell.target
            uses_spell = True
        return self.__get_possible_targets(character, target_type, uses_spell)

class ActionSelector:
    def select(self, character : Character, characterList, helper : ActionHelper):
        return Action(Action.ACTION_NONE, None, [], '')