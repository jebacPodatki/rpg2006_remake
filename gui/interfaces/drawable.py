import pygame

class DrawableObjectInterface:
    def draw(self, screen : pygame.Surface):
        pass
    def update(self):
        pass