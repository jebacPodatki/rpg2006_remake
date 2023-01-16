import pygame
from gui.config import *
from gui.interfaces.drawable import *
from gui.widgets.attribute_bar import *

from system.core.character import *

class CharacterHUD(DrawableObjectInterface):
    def update(self):
        if self.character.is_alive():
            self.dp_bar.set_value(self.character.stats.dp / self.character.sheet.dp)
            self.rp_bar.set_value(self.character.stats.rp / self.character.sheet.rp)
            self.hp_bar.set_value(self.character.stats.hp / self.character.sheet.hp)
            if self.character.sheet.mp > 0:
                self.mp_bar.set_value(self.character.stats.mp / self.character.sheet.mp)
            else:
                self.mp_bar.set_value(0)
        else:
            self.dp_bar.set_value(0)
            self.rp_bar.set_value(0)
            self.hp_bar.set_value(0)
            self.mp_bar.set_value(0)

    def __init__(self, config : Config, character : Character, position = (0, 0)):
        self.character = character
        self.position = position
        font = pygame.font.SysFont(config.hud_font, config.hud_font_size)
        self.caption = font.render(character.sheet.name, 1, config.hud_font_color)
        delta_y = self.caption.get_height() + 5
        self.dp_bar = AttributeBar(config, (position[0], position[1] + delta_y), config.hud_dp_bar_color, True)
        self.rp_bar = AttributeBar(config, (position[0] + config.hud_bar_delta_x, position[1] + delta_y),
                                   config.hud_rp_bar_color, True)
        self.hp_bar = AttributeBar(config, (position[0], position[1] + delta_y + config.hud_bar_interline),
                                   config.hud_hp_bar_color, False)
        self.mp_bar = AttributeBar(config, (position[0], position[1] + delta_y + 2 * config.hud_bar_interline),
                                   config.hud_mp_bar_color, False)
        self.update()

    def draw(self, screen : pygame.Surface):
        screen.blit(self.caption, self.position)
        self.dp_bar.draw(screen)
        self.rp_bar.draw(screen)
        self.hp_bar.draw(screen)
        self.mp_bar.draw(screen)
