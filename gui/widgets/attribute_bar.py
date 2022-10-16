import pygame
from gui.config import *
from gui.drawable import *

class AttributeBar(DrawableObjectInterface):
    def __init__(self, config : Config, x : int, y : int, color, short : bool):
        self.x = x
        self.y = y
        self.color = color
        self.value = 1.0
        if short == False:
            self.img = pygame.image.load(config.bar_image)
        else:
            self.img = pygame.image.load(config.bar_short_image)
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def set_value(self, value : float):
        self.value = value

    def draw(self, screen : pygame.Surface):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.value * self.width, self.height))
        screen.blit(self.img, (self.x, self.y))