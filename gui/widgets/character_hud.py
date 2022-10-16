import pygame
from gui.config import *
from gui.drawable import *
from gui.widgets.attribute_bar import *

from system.core.character import *

class CharacterHUD:
    def update(self):
        self.dp_bar.set_value(self.character.stats.dp / self.character.sheet.dp)
        self.rp_bar.set_value(self.character.stats.rp / self.character.sheet.rp)
        self.hp_bar.set_value(self.character.stats.hp / self.character.sheet.hp)
        self.mp_bar.set_value(self.character.stats.mp / self.character.sheet.mp)

    def __init__(self, config : Config, character : Character, x : int, y : int):
        self.character = character
        self.x = x
        self.y = y
        font = pygame.font.SysFont(config.hud_font, config.hud_font_size)
        self.name_text = font.render(character.sheet.name, 1, config.hud_font_color)
        delta_y = self.name_text.get_height() + 5
        self.dp_bar = AttributeBar(config, x, y + delta_y, config.hud_dp_bar_color, True)
        self.rp_bar = AttributeBar(config, x + config.hud_bar_delta_x, y + delta_y,
                                   config.hud_rp_bar_color, True)
        self.hp_bar = AttributeBar(config, x, y + delta_y + config.hud_bar_interline, config.hud_hp_bar_color, False)
        self.mp_bar = AttributeBar(config, x, y + delta_y + 2 * config.hud_bar_interline, config.hud_mp_bar_color, False)
        self.update()

    def draw(self, screen : pygame.Surface):
        screen.blit(self.name_text, (self.x, self.y))
        self.dp_bar.draw(screen)
        self.rp_bar.draw(screen)
        self.hp_bar.draw(screen)
        self.mp_bar.draw(screen)