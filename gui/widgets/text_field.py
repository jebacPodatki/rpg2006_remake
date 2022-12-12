import pygame
from gui.config import *
from gui.interfaces.drawable import *

class TextField(DrawableObjectInterface):
    def __init__(self, config : Config, position = (0, 0), font_color = (255, 255, 255), border = True):
        self.position = position
        self.max_length = config.text_field_max_length
        self.color = font_color
        self.font = pygame.font.SysFont(config.text_field_font, config.text_field_font_size)
        self.text = ''
        self.text_line = None
        self.border = border
        if border:
            self.rect = (position[0],
                         position[1],
                         config.text_field_size[0],
                         config.text_field_size[1])

    def set_text(self, text : str):
        self.text = text[:self.max_length]
        self.text_line = self.font.render(self.text, 1, self.color, (0, 0, 0))

    def get_text(self):
        return self.text

    def draw(self, screen : pygame.Surface):
        if self.border:
            pygame.draw.rect(screen, (120, 120, 120), self.rect, 2)
        if self.text_line != None:
            screen.blit(self.text_line, (self.position[0] + 5, self.position[1] + 5))