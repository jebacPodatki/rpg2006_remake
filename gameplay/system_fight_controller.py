from gameplay.game_state import *

from system.core.library import *
from system.core.action.selector import *
from system.core.fight import *
from system.ai.ai import *
from system.event.event_receiver import *

class SystemFightController:
    PLAYER_FACTION = Character.BLUE_FACTION

    def __init__(self, library : Library, game_state : GameState):
        self.library = library
        self.game_state = game_state
        self.characters = []
        self.fight = None

    def __on_fight_end(self):
        number_of_alives = 0
        for character in self.characters:
            if character.faction != SystemFightController.PLAYER_FACTION:
                continue
            if not character.is_alive():
                self.game_state.player_characters[character.sheet.name].alive = False
            else:
                number_of_alives += 1
        if number_of_alives > 0:
            self.game_state.level += 1

    def __get_encounter_for_level(self, level : int):
        ind = 0
        for encounter in self.library.encounters:
            if ind == level:
                return self.library.encounters[encounter]
            ind += 1

    def prepare_characters_for_new_fight(self):
        self.characters = []
        for player_character_name in self.game_state.player_characters:
            player_character = self.game_state.player_characters[player_character_name]
            if player_character.alive:
                character = Character(player_character.character_sheet, True, Character.BLUE_FACTION)
                if player_character.back_line:
                    character.line = Character.BACK_LINE
                self.characters.append(character)
        encounter = self.__get_encounter_for_level(self.game_state.level - 1)
        for sheet_name in encounter.front_line:
            character = Character(self.library.sheets[sheet_name], False, Character.RED_FACTION)
            self.characters.append(character)
        for sheet_name in encounter.back_line:
            character = Character(self.library.sheets[sheet_name], False, Character.RED_FACTION)
            character.line = Character.BACK_LINE
            self.characters.append(character)
        return self.characters

    def start_new_fight(self, selector : ActionSelectorInterface, logger : EventReceiverInterface):
        if len(self.characters) == 0:
            self.prepare_new_fight()
        self.fight = Fight(self.characters, self.library, selector, AIActionSelector(), logger)

    def get_current_character(self):
        if self.fight != None:
            return self.fight.get_current_character()
        return None

    def process_current_fight(self):
        if self.fight != None:
            self.fight.process()
            if self.fight.ended():
                self.__on_fight_end()
                self.fight = None

    def is_fight_ended(self):
        if self.fight == None:
            return True
        return False