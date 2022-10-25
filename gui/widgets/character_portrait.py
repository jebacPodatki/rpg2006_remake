import pygame
from gui.config import *
from gui.drawable import *
from system.core.character import *

class CharacterPortrait(DrawableObjectInterface):
    def __calculate_caption_position(base_pos, img_size, caption_size):
        x = base_pos[0] + img_size[0] / 2 - caption_size[0] / 2
        y = base_pos[1] + img_size[1] + 4
        return (x, y)

    def __init__(self, config : Config, character : Character, position = (0, 0)):
        self.position = position
        self.img = pygame.image.load(character.sheet.portrait)
        font = pygame.font.SysFont(config.portrait_caption_font, config.portrait_caption_font_size)
        self.caption = font.render(character.sheet.name, 1, config.portrait_caption_font_color)
        self.caption_position = CharacterPortrait.__calculate_caption_position(
            position, self.img.get_size(), self.caption.get_size())

    def set_position(self, position = (0, 0)):
        dx = self.caption_position[0] - self.position[0]
        dy = self.caption_position[1] - self.position[1]
        self.position = position
        self.caption_position = (position[0] + dx, position[1] + dy)

    def draw(self, screen : pygame.Surface):
        screen.blit(self.img, self.position)
        screen.blit(self.caption, self.caption_position)
