from system.event.event_receiver import *
from system.core.character import *

class ConsoleEventReceiver(EventReceiverInterface):
    COLOR = '\033[0m'
    COLOR2 = '\033[92m'
    def on_attack(self, attacker : Character, targets):
        print(ConsoleEventReceiver.COLOR, end = ' ')
        print(attacker.sheet.name + ' attacks ' + targets[0].sheet.name, end = ' ')

    def on_damage(self, character : Character, damage):
        print('and deals ' + str(damage) + ' damage. ' + character.sheet.name + ' has ' + str(character.stats.hp) + ' HP now.')

    def on_block(self, character : Character):
        print('who blocks')

    def on_cast_spell(self, attacker : Character, targets, spell_name):
        print(ConsoleEventReceiver.COLOR, end = ' ')
        if len(targets) == 1:
            print(attacker.sheet.name + ' casts ' + spell_name + ' against ' + targets[0].sheet.name, end = ' ')
        else:
            print(attacker.sheet.name + ' casts ' + spell_name, end = ' ')

    def on_spell_effect(self, targets, effect):
        if effect == 'raise':
            if str(len(targets)) > 1:
                print('and creates ' + str(len(targets)) + ' ' + targets[0].sheet.name + 's')
            elif str(len(targets)) == 1:
                print('and creates ' + targets[0].sheet.name)

    def on_magic_block(self, character : Character):
        print(ConsoleEventReceiver.COLOR, end = ' ')
        print('who effectively resists magic')

    def on_wait(self, character : Character):
        print(ConsoleEventReceiver.COLOR, end = ' ')
        print(character.sheet.name + ' is waiting.')

    def on_death(self, character : Character):
        print(ConsoleEventReceiver.COLOR, end = ' ')
        print(character.sheet.name + ' died')

    def on_new_turn(self, current_character : Character, characters):
        if current_character.controlled == False:
            return
        print(ConsoleEventReceiver.COLOR2)
        for chr in characters:
            print('\t' + chr.sheet.name + '\t\t' + '[' + str(chr.stats.hp) + '/' + str(chr.sheet.hp) + ']')

    def on_move(self, character : Character):
        print(ConsoleEventReceiver.COLOR, end = ' ')
        if character.line == Character.FRONT_LINE:
            line = 'front line'
        else:
            line = "back line"
        print(character.sheet.name + ' moved to ' + line)