import pygame
from core.resource_provider import *
from gui.interfaces.drawable import *

class Sprite(DrawableObjectInterface):
    def __init__(self, image_path : str, position = (0, 0)):
        self.position = position
        self.img = ResourceProvider.get(image_path)

    def set_position(self, position = (0, 0)):
        self.position = position

    def draw(self, screen : pygame.Surface):
        screen.blit(self.img, self.position)