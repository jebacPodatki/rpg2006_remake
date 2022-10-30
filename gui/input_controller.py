import pygame
from gui.input_event import *
from gui.controller_interface import *

class InputController:
    def __init__(self):
        self.controllers = []
        pass
    def __define_event(event):
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                return InputEvent(InputEvent.UP)
            if keys[pygame.K_DOWN] :
                return InputEvent(InputEvent.DOWN)
            if keys[pygame.K_RETURN] :
                return InputEvent(InputEvent.SELECT)
        return InputEvent(InputEvent.NONE)
    def register_controller(self, controller : ControllerInterface):
        self.controllers.append(controller)
    def process_pygame_event(self, pygame_event):
        event = InputController.__define_event(pygame_event)
        for controller in self.controllers:
            controller.on_event(event)