import pygame
from gui.input_event import *
from gui.input_interface import *

class InputController:
    def __init__(self):
        self.objects = []
        pass
    def __define_event(event):
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                return InputEvent(InputEvent.UP)
            if keys[pygame.K_DOWN] :
                return InputEvent(InputEvent.DOWN)
            if keys[pygame.K_RETURN] :
                return InputEvent(InputEvent.ENTER)
        return InputEvent(InputEvent.NONE)
    def register_object(self, object : InputInterface):
        self.objects.append(object)
    def process_pygame_event(self, pygame_event):
        event = InputController.__define_event(pygame_event)
        for object in self.objects:
            object.on_event(event)