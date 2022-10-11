import random
from system.core.spell import *
from system.core.character import *
from system.core.library import Library
from system.core.action.action import *
from system.core.action.helper import *
from system.core.action.selector import *
from system.event.event_receiver import EventReceiverInterface

class Fight:
    def __init__(self, characters, library : Library, selectorA : ActionSelectorInterface,
                 selectorB : ActionSelectorInterface, logger):
        self.characters = characters
        self.library = library
        self.selector = [selectorA, selectorB]
        self.current = 0
        self.logger = logger
        self.characters.sort(key=lambda x: x.sheet.initiative, reverse=True)
        self.helper = ActionHelper(self.library, self.characters)

    def __attack_target(self, attacker, target):
        atk_factor = attacker.sheet.attack / target.sheet.defence
        atk = atk_factor * random.randint(attacker.sheet.breakage[0], attacker.sheet.breakage[1])
        target.stats.dp -= atk
        if target.stats.dp <= 0:
            dmg_factor = attacker.sheet.strength / target.sheet.endurance
            dmg = dmg_factor * random.randint(attacker.sheet.dmg[0], attacker.sheet.dmg[1])
            target.stats.hp -= dmg
            self.logger.on_damage(target, dmg)
            if target.stats.hp < 0:
                self.logger.on_death(target)
            else:
                target.stats.dp = target.sheet.dp
        else:
            self.logger.on_block(target)

    def __attack(self, attacker, targets):
        if len(targets) == 0:
            return
        for i in range(attacker.sheet.attack_number):
            self.logger.on_attack(attacker, targets)
            for target in targets:
                self.__attack_target(attacker, target)

    def __magic_on_target(self, attacker, target, spell):
        if spell.effect == 'raise':
            sheet = self.library.sheets['Skeleton']
            number = int(attacker.sheet.power / 5)
            if number > 0:
                skeletons = [Character(sheet, False, attacker.faction) for i in range(number)]
                for skeleton in skeletons:
                    self.characters.append(skeleton)
                self.logger.on_spell_effect(skeletons, spell.effect)
            return
        atk_factor = attacker.sheet.power / target.sheet.will
        atk = atk_factor * random.randint(spell.impact[0], spell.impact[1])
        target.stats.rp -= atk
        if target.stats.rp <= 0:
            dmg_factor = attacker.sheet.power / target.sheet.will
            dmg = dmg_factor * random.randint(spell.dmg[0], spell.dmg[1])
            target.stats.hp -= dmg
            self.logger.on_damage(target, dmg)
            if target.stats.hp < 0:
                self.logger.on_death(target)
            else:
                target.stats.rp = target.sheet.rp
        else:
            self.logger.on_magic_block(target)

    def __magic(self, attacker, targets, spell_name):
        if spell_name in self.library.spells:
            spell = self.library.spells[spell_name]
        else:
            return
        if attacker.stats.mp < spell.mp_cost:
            return
        attacker.stats.mp -= spell.mp_cost
        self.logger.on_cast_spell(attacker, targets, spell.name)
        if len(targets) > 0:
            for target in targets:
                self.__magic_on_target(attacker, target, spell)
        else:
            self.__magic_on_target(attacker, [], spell)

    def __move(self, actor : Character):
        if actor.line == Character.FRONT_LINE:
            actor.line = Character.BACK_LINE
        else:
            actor.line = Character.FRONT_LINE
        self.logger.on_move(actor)

    def __move_all_to_frontline(self, faction : int):
        for chr in self.characters:
            if chr.faction == faction:
                chr.line = Character.FRONT_LINE

    def __processAction(self, action : Action):
        if action.type == Action.ACTION_WAIT:
            self.logger.on_wait(action.actor)
            action.actor.stats.action_number = 0
        elif action.type == Action.ACTION_ATTACK:
            self.__attack(action.actor, action.targets)
            action.actor.stats.action_number -= 1
        elif action.type == Action.ACTION_MAGIC:
            self.__magic(action.actor, action.targets, action.spell_name)
            action.actor.stats.action_number = 0
        elif action.type == Action.ACTION_MOVE:
            self.__move(action.actor)
            action.actor.stats.action_number = 0
        else:
            pass

    def __new_turn(self):
        self.current += 1
        if self.current >= len(self.characters):
            self.current = 0
        current_character = self.characters[self.current]
        if current_character.is_alive():
            current_character.stats.action_number = current_character.sheet.action_number
            self.logger.on_new_turn(current_character, self.characters)

    def process(self):
        if self.current == -1 or self.characters[self.current].stats.action_number == 0:
            self.__new_turn()
        current_character = self.characters[self.current]
        if current_character.is_alive():
            if current_character.controlled == True:
                selector = self.selector[0]
            else:
                selector = self.selector[1]
            action = selector.select(current_character, self.characters, self.helper)
            if action.type == Action.ACTION_NONE:
                return
            self.__processAction(action)
            if self.helper.is_frontline_empty(Character.BLUE_FACTION):
                self.__move_all_to_frontline(Character.BLUE_FACTION)
            if self.helper.is_frontline_empty(Character.RED_FACTION):
                self.__move_all_to_frontline(Character.RED_FACTION)

    def ended(self):
        alive = [0, 0]
        for chr in self.characters:
            if chr.is_alive():
                if chr.faction == Character.BLUE_FACTION:
                    alive[0] += 1
                else:
                    alive[1] += 1
        if alive[0] == 0 or alive[1] == 0:
            return True
        return False