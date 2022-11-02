import pygame
from gui.interfaces.drawable import *

class AbstractView:
    def __init__(self):
        self.objects = []

    def add_object(self, object : DrawableObjectInterface):
        self.objects.append(object)

    def draw_all(self, screen : pygame.Surface):
        for object in self.objects:
            object.draw(screen)