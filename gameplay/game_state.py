from system.core.character import *

class CharacterState:
    def __init__(self, character_sheet : CharacterSheet, back_line : bool):
        self.character_sheet = character_sheet
        self.alive = True
        self.back_line = back_line

class GameState:
    def __init__(self):
        self.player_characters = {}
        self.level = 1
    def add_player_character(self, character_sheet : CharacterSheet, back_line : bool:
        self.player_characters[character_sheet.name] = CharacterState(character_sheet, back_line)