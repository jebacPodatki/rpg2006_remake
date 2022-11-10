import pygame
from core.resource_provider import *
from gui.config import *
from gui.interfaces.drawable import *
from system.core.character import *

class CharacterPortrait(DrawableObjectInterface):
    def __calculate_caption_position(base_pos, img_size, caption_size):
        x = base_pos[0] + img_size[0] / 2 - caption_size[0] / 2
        y = base_pos[1] + img_size[1] + 4
        return (x, y)

    def _get_portrait_path(self, config : Config, portrait_name : str):
        return config.portraits_path + '/' + portrait_name

    def __init__(self, config : Config, character : Character, position = (0, 0)):
        self.position = position
        self.character = character
        self.img = ResourceProvider.get(self._get_portrait_path(config, character.sheet.portrait))
        self.img_dead = ResourceProvider.get(self._get_portrait_path(config, character.sheet.dead_portrait))
        font = pygame.font.SysFont(config.portrait_caption_font, config.portrait_caption_font_size)
        self.caption = font.render(character.sheet.name, 1, config.portrait_caption_font_color)
        if character.faction == Character.BLUE_FACTION:
            selected_color = config.portrait_caption_font_color_selected_blue
        else:
            selected_color = config.portrait_caption_font_color_selected_red
        self.caption_selected = font.render(character.sheet.name, 1, selected_color)
        self.caption_position = CharacterPortrait.__calculate_caption_position(
            position, self.img.get_size(), self.caption.get_size())
        self.selected = False

    def set_position(self, position = (0, 0)):
        dx = self.caption_position[0] - self.position[0]
        dy = self.caption_position[1] - self.position[1]
        self.position = position
        self.caption_position = (position[0] + dx, position[1] + dy)

    def select(self, value : bool):
        self.selected = value

    def draw(self, screen : pygame.Surface):
        if self.character.is_alive():
            screen.blit(self.img, self.position)
            if self.selected:
                screen.blit(self.caption_selected, self.caption_position)
            else:
                screen.blit(self.caption, self.caption_position)
        else:
            screen.blit(self.img_dead, self.position)
