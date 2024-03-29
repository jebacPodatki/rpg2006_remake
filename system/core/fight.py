import random
from system.core.spell import *
from system.core.character import *
from system.core.library import Library
from system.core.action.action import *
from system.core.action.helper import *
from system.core.action.action_selector import *
from system.core.spellbook import *
from system.event.fight_event_receiver import FightEventReceiverInterface

class Fight:
    def __init__(self, characters, library : Library, selectorA : ActionSelectorInterface,
                 selectorB : ActionSelectorInterface, logger):
        self.characters = characters
        self.library = library
        self.selector = [selectorA, selectorB]
        self.current = -1
        self.logger = logger
        self.characters.sort(key=lambda x: x.sheet.initiative, reverse=True)
        self.helper = ActionHelper(self.library, self.characters)
        self.spellbook = Spellbook(characters, library, self.helper)
        self.round_number = 0
        self.winner_faction = 0

    def get_current_character(self):
        return self.characters[self.current]

    def __check_critical_hit(self, attacker):
        if random.randint(1, 100) <= attacker.sheet.critical_hit_chance:
            return True
        return False

    def __attack_target(self, attacker, target):
        atk_factor = attacker.sheet.attack / target.sheet.defence
        atk = atk_factor * random.randint(attacker.sheet.breakage[0], attacker.sheet.breakage[1])
        target.stats.dp -= atk
        if target.stats.dp <= 0:
            dmg_factor = attacker.sheet.strength / target.sheet.endurance
            dmg = int(dmg_factor * random.randint(attacker.sheet.dmg[0], attacker.sheet.dmg[1]))
            critical_hit = self.__check_critical_hit(attacker)
            if critical_hit:
                dmg *= attacker.sheet.critical_hit_dmg_factor
            dmg_reduced = dmg - target.sheet.armor
            if dmg_reduced < 0:
                dmg_reduced = 0
            target.stats.hp -= dmg_reduced
            self.logger.on_damage(target, dmg_reduced, dmg - dmg_reduced, critical_hit)
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
        if spell.effect != '':
            actors = self.spellbook.invoke_spell_effect(spell, spell.effect, attacker, target)
            self.logger.on_spell_effect(actors, spell.effect)
            return
        atk_factor = attacker.sheet.power / target.sheet.will
        atk = atk_factor * random.randint(spell.impact[0], spell.impact[1])
        target.stats.rp -= atk
        if target.stats.rp <= 0:
            dmg_factor = attacker.sheet.power / target.sheet.will
            dmg = int(dmg_factor * random.randint(spell.dmg[0], spell.dmg[1]))
            dmg_reduced = dmg - target.sheet.armor
            if dmg_reduced < 0:
                dmg_reduced = 0
            target.stats.hp -= dmg_reduced
            self.logger.on_damage(target, dmg_reduced, dmg - dmg_reduced, False)
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

    def __move_first_dead_character_to_backline(self, faction):
        for chr in self.characters:
            if not chr.is_alive() and chr.faction == faction and chr.line == Character.FRONT_LINE:
                chr.line = Character.BACK_LINE

    def __move(self, actor : Character):
        if actor.line == Character.FRONT_LINE:
            actor.line = Character.BACK_LINE
        else:
            if self.helper.is_frontline_full(actor.faction, False):
                self.__move_first_dead_character_to_backline(actor.faction)
            actor.line = Character.FRONT_LINE
        self.logger.on_move(actor)

    def __move_all_alive_to_frontline(self, faction : int):
        for chr in self.characters:
            if chr.faction == faction:
                if chr.is_alive():
                    chr.line = Character.FRONT_LINE
                else:
                    chr.line = Character.BACK_LINE

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
        if self.ended():
            return
        if self.round_number == 0:
            self.logger.on_start()
            self.round_number += 1
        while True:
            self.current += 1
            if self.current >= len(self.characters):
                self.current = 0
                self.round_number += 1
            current_character = self.characters[self.current]
            if current_character.is_alive():
                current_character.stats.action_number = current_character.sheet.action_number
                self.logger.on_new_turn(current_character, self.characters)
                return

    def process(self):
        if self.current == -1 or self.characters[self.current].stats.action_number == 0:
            self.__new_turn()
        current_character = self.characters[self.current]
        if current_character.is_alive():
            if current_character.controlled == True:
                selector = self.selector[0]
            else:
                selector = self.selector[1]
            action = selector.select(current_character, self.helper)
            if action.type == Action.ACTION_NONE:
                return
            self.__processAction(action)
            if self.helper.is_frontline_empty(Character.BLUE_FACTION):
                self.__move_all_alive_to_frontline(Character.BLUE_FACTION)
            if self.helper.is_frontline_empty(Character.RED_FACTION):
                self.__move_all_alive_to_frontline(Character.RED_FACTION)
        if self.ended() and self.round_number > 0:
            self.logger.on_end(self.winner_faction)
            self.round_number = 0

    def ended(self):
        alive = [0, 0]
        for chr in self.characters:
            if chr.is_alive():
                if chr.faction == Character.BLUE_FACTION:
                    alive[0] += 1
                else:
                    alive[1] += 1
        if alive[0] == 0 or alive[1] == 0:
            if alive[0] > 0:
                self.winner_faction = Character.BLUE_FACTION
            else:
                self.winner_faction = Character.RED_FACTION
            return True
        return False