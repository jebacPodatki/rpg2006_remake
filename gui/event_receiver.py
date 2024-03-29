from system.event.fight_event_receiver import *
from system.core.character import *
from gui.widgets.console import *

class SystemEventReceiver(FightEventReceiverInterface):
    def __init__(self, console : Console):
        self.console = console

    def on_start(self):
        self.console.print_nl("FIGHT BEGINS")

    def on_end(self, winner_faction : int):
        self.console.print_nl("THE FIGHT IS OVER")
        if winner_faction == Character.BLUE_FACTION:
            self.console.print_nl("YOU WON!");
        else:
            self.console.print_nl("YOU LOOSE!");

    def on_attack(self, attacker : Character, targets):
        self.console.print_nl(attacker.sheet.name + ' attacks ' + targets[0].sheet.name + '. ')

    def on_damage(self, character : Character, damage : int, armor_reduction : int, critical : bool):
        if critical:
            self.console.print('CRITICAL HIT! ')
        if armor_reduction > 0:
            self.console.print(character.sheet.name + ' taken ' + str(damage) + ' damage (' + str(armor_reduction) + ' reduced).')
        else:
            self.console.print(character.sheet.name + ' taken ' + str(damage) + ' damage.')

    def on_block(self, character : Character):
        self.console.print(character.sheet.name + ' blocked attack.')

    def on_cast_spell(self, attacker : Character, targets, spell_name : str):
        if len(targets) == 1:
            self.console.print_nl(attacker.sheet.name + ' casts ' + spell_name + ' on ' + targets[0].sheet.name + ' ')
        else:
            self.console.print_nl(attacker.sheet.name + ' casts ' + spell_name + ' ')

    def on_spell_effect(self, targets, effect : str):
        if effect == 'summon_undeads':
            if len(targets) > 1:
                self.console.print('and creates ' + str(len(targets)) + ' ' + targets[0].sheet.name + 's.')
            elif len(targets) == 1:
                self.console.print('and creates ' + targets[0].sheet.name + '.')
        elif effect == 'heal':
            self.console.print('and heals ' + targets[0].sheet.name)

    def on_magic_block(self, character : Character):
        self.console.print(character.sheet.name + ' effectively resists magic.')

    def on_wait(self, character : Character):
        self.console.print_nl(character.sheet.name + ' is waiting.')

    def on_death(self, character : Character):
        self.console.print_nl(character.sheet.name + ' died.')

    def on_new_turn(self, current_character : Character, characters):
        pass

    def on_move(self, character : Character):
        if character.line == Character.FRONT_LINE:
            line = 'front line'
        else:
            line = "back line"
        self.console.print_nl(character.sheet.name + ' moved to ' + line +'.')