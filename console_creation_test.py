from system.core.character import *
from system.core.library import *
from system.creation.character_creator import *
from system.event.creation_event_receiver import *

def printChar(chr : CharacterSheet):
    print('Name: ' + str(chr.name))
    print('Race: ' + str(chr.race))
    print('Class: ' + str(chr.main_class))
    print('STR: ' + str(chr.strength) + '\tEND: ' + str(chr.endurance))
    print('ATK: ' + str(chr.attack) + '\tDEF: ' + str(chr.defence))
    print('POW: ' + str(chr.power) + '\tWIL: ' + str(chr.will))


class CCreator(CreationEventReceiverInterface):
    def __init__(self, library : Library):
        self.creator = CharacterCreator(library, self)
        self.creator.start()

    def on_wrong_choice(self):
        print('wrong choice')

    def on_wrong_name(self, error : str):
        print('wrong name: ' + error)

    def on_selecting_race_stage(self, choice_controller : ChooseOptionInterface, sheet : CharacterSheet, races):
        print('Select race: ')
        i = 0
        for race in races:
            print(str(i) + ' = ' + race)
            i += 1
        choice_controller.choose_option(int(input()))

    def on_selecting_class_stage(self, choice_controller : ChooseOptionInterface, sheet : CharacterSheet, classes):
        print('Select class: ')
        i = 0
        for cls in classes:
            print(str(i) + ' = ' + cls)
            i += 1
        choice_controller.choose_option(int(input()))

    def on_selecting_name_stage(self, choice_controller : ChooseStringInterface, sheet : CharacterSheet):
        print('Type character name: ')
        choice_controller.choose_string(input())

    def on_creation_finished(self, sheet : CharacterSheet):
        print('----')
        printChar(sheet)

library = Library('json/spells.json', 'json/sheets.json', 'json/encounters.json', 'json/races.json')
creation = CCreator(library)