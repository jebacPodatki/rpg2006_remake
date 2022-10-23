from system.core.spell import *
from system.core.library import Library
from system.core.action.target import *
from system.core.character import *

class ActionHelper:
    MAX_IN_LINE = 6

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

    def can_summon(self, character : Character):
        if self.is_frontline_full(character.faction, False):
            return False
        return True

    def can_move(self, character : Character):
        if character.line == Character.FRONT_LINE:
            if self.is_backline_empty(character.faction) or self.is_backline_full(character.faction, True):
                return False
            possible = True
            character.line = Character.BACK_LINE
            if self.is_frontline_empty(character.faction):
                possible = False
            character.line = Character.FRONT_LINE
            return possible
        elif character.line == Character.BACK_LINE:
            if self.is_frontline_empty(character.faction) or self.is_frontline_full(character.faction, True):
                return False
            if not self.is_frontline_full(character.faction, False):
                return True
        return True

    def is_single_target(self, spell_name):
        if spell_name in self.library.spells:
            spell = self.library.spells[spell_name]
            return spell.target == ActionTarget.TARGET_SINGLE_ENEMY_FRONTLINE \
                or spell.target == ActionTarget.TARGET_SINGLE_ENEMY_BOTHLINE \
                or spell.target == ActionTarget.TARGET_SINGLE_ALLY
        else:
            return False

    def is_frontline_empty(self, faction, alives = True):
        for chr in self.characters:
            if (chr.is_alive() or not alives) and chr.faction == faction and chr.line == Character.FRONT_LINE:
                return False
        return True

    def is_backline_empty(self, faction, alives = True):
        for chr in self.characters:
            if (chr.is_alive() or not alives) and chr.faction == faction and chr.line == Character.BACK_LINE:
                return False
        return True

    def is_frontline_full(self, faction, alives = True):
        n = 0
        for chr in self.characters:
            if (chr.is_alive() or not alives) and chr.faction == faction and chr.line == Character.FRONT_LINE:
                n += 1
        if n >= ActionHelper.MAX_IN_LINE:
            return True
        return False

    def is_backline_full(self, faction, alives = True):
        n = 0
        for chr in self.characters:
            if (chr.is_alive() or not alives) and chr.faction == faction and chr.line == Character.BACK_LINE:
                n += 1
        if n >= ActionHelper.MAX_IN_LINE:
            return True
        return False

    def __get_possible_targets(self, character : Character, target_type, with_spell : bool):
        if target_type == ActionTarget.TARGET_NONE:
            return []
        elif target_type == ActionTarget.TARGET_ALL_ALLIES or target_type == ActionTarget.TARGET_ALL_ENEMIES:
            all = []
            if target_type == ActionTarget.TARGET_ALL_ALLIES:
                target_faction = character.faction
            else:
                target_faction = -character.faction
            for chr in self.characters:
                if chr.faction == target_faction and chr.is_alive():
                    all.append(chr)
            return [all]
        elif target_type == ActionTarget.TARGET_SINGLE_ALLY or target_type == ActionTarget.TARGET_SINGLE_ENEMY_BOTHLINE:
            targets = []
            if target_type == ActionTarget.TARGET_SINGLE_ALLY:
                target_faction = character.faction
            else:
                target_faction = -character.faction
            for chr in self.characters:
                if chr.faction == target_faction and chr.is_alive():
                    targets.append([chr])
            return targets
        elif target_type == ActionTarget.TARGET_ALL_ENEMIES_FRONTLINE:
            if self.is_frontline_empty(-character.faction):
                return self.get_possible_targets(character, ActionTarget.TARGET_ALL_ENEMIES)
            if character.line == Character.BACK_LINE and not character.sheet.distant and with_spell == False:
                return []
            all = []
            for chr in self.characters:
                if chr.faction == -character.faction and chr.is_alive() and chr.line == Character.FRONT_LINE:
                    all.append(chr)
            return [all]
        elif target_type == ActionTarget.TARGET_SINGLE_ENEMY_FRONTLINE:
            if self.is_frontline_empty(-character.faction):
                return self.get_possible_targets(character, ActionTarget.TARGET_SINGLE_ENEMY_BOTHLINE)
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