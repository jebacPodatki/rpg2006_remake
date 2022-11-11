import pygame
from gui.config import *
from gui.interfaces.drawable import *
from gui.widgets.character_hud import *

from system.core.character import *

class BattleHUD(DrawableObjectInterface):
    def __add_hud_for_character(self, character):
        if character.faction == Character.BLUE_FACTION:
            self.character_huds.append(
                CharacterHUD(self.config, character, (self.left_column_pos[0], self.left_column_pos[1])))
            self.left_column_pos[1] += self.config.battle_hud_pos_delta
        elif character.faction == Character.RED_FACTION:
            self.character_huds.append(
                CharacterHUD(self.config, character, (self.right_column_pos[0], self.right_column_pos[1])))
            self.right_column_pos[1] += self.config.battle_hud_pos_delta

    def update(self):
        if len(self.characters) > len(self.character_huds):
            n = len(self.character_huds)
            m = len(self.characters)
            for i in range(n, m):
                self.__add_hud_for_character(self.characters[i])
        for hud in self.character_huds:
            hud.update()

    def __init__(self, config : Config, characters):
        self.config = config
        self.characters = characters
        self.character_huds = []
        self.left_column_pos = config.battle_hud_left_column_pos
        self.right_column_pos = config.battle_hud_right_column_pos
        for character in characters:
            self.__add_hud_for_character(character)
        self.update()

    def draw(self, screen : pygame.Surface):
        for hud in self.character_huds:
            hud.draw(screen)