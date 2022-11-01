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

    def start_new_fight(self, selector : ActionSelectorInterface, logger : EventReceiverInterface):
        self.characters = []
        for player_character_name in self.game_state.player_characters:
            player_character = self.game_state.player_characters[player_character_name]
            if player_character.alive:
                self.characters.append(Character(player_character.character_sheet, True, Character.BLUE_FACTION))
        for sheet_name in self.library.encounters[self.game_state.level - 1]:
            sheet = self.library.sheets[sheet_name]
            self.characters.append(Character(sheet, False, Character.RED_FACTION))
        self.fight = Fight(self.characters, self.library, selector, AIActionSelector(), logger)

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