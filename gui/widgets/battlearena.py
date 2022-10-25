import pygame
from gui.config import *
from gui.drawable import *
from gui.widgets.character_portrait import *
from system.core.character import *

class BattleArena(DrawableObjectInterface):
    def reset(self):
        lines = [[], [], [], [], []]
        for character in self.characters:
            line_index = character.line * character.faction + 2
            lines[line_index].append(character)
        cx = self.config.arena_pos[0]
        cy = self.config.arena_pos[1]
        dy_back = self.config.arena_back_line_pos_delta_y
        dy_front = self.config.arena_front_line_pos_delta_y
        cyt = [cy - dy_back, cy - dy_front, cy, cy + dy_front, cy + dy_back]
        idx = 0
        for line in lines:
            y = cyt[idx]
            idx += 1
            if len(line) % 2 == 0:
                delta_x = int(self.config.arena_portrait_delta_x / 2)
                fx = -1
            else:
                delta_x = 0
                fx = 1
            for character in line:
                position = (cx + delta_x * fx - 35, y - 45)
                if character in self.character_portraits:
                    self.character_portraits[character].set_position(position)
                else:
                    self.character_portraits[character] = CharacterPortrait(self.config, character, position)
                if fx == 1:
                    delta_x += self.config.arena_portrait_delta_x
                fx *= -1
    def update(self):
        self.reset()
    def __init__(self, config : Config, characters):
        self.config = config
        self.characters = characters
        self.character_portraits = {}
        self.rect = (self.config.arena_pos[0] - self.config.arena_size[0] / 2,
                     self.config.arena_pos[1] - self.config.arena_size[1] / 2,
                     self.config.arena_size[0],
                     self.config.arena_size[1])
        self.reset()
    def draw(self, screen : pygame.Surface):
        pygame.draw.rect(screen, self.config.arena_color, self.rect, 2)
        for portrait in self.character_portraits:
            self.character_portraits[portrait].draw(screen)