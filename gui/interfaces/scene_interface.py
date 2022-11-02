import pygame
from gui.input.input_event import *

class SceneInterface:
    def on_start(self):
        pass
    def on_end(self):
        pass
    def on_event(self, event : InputEvent):
        pass
    def on_frame(self, screen : pygame.Surface):
        pass
    def on_update(self):
        pass