from gameplay.game_state import *
from system.core.library import *

class GameStateController:
    def __init__(self):
        self.game_state = None
        self.library = Library('json/spells.json', 'json/sheets.json', 'json/encounters.json')

    def new_game(self):
        self.game_state = GameState()