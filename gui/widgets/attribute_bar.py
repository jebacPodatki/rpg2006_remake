import pygame
from gui.config import *
from gui.drawable import *

class AttributeBar(DrawableObjectInterface):
    def __init__(self, config : Config, position = (0, 0), color = (0, 0, 0), short = False):
        self.position = position
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
        pygame.draw.rect(screen, self.color, (self.position[0], self.position[1], self.value * self.width, self.height))
        screen.blit(self.img, self.position)