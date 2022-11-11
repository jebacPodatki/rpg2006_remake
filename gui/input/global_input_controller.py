import pygame
from gui.input.input_event import *
from gui.input.input_controller_interface import *

class GlobalInputController:
    def __init__(self):
        self.controllers = set()

    def __define_event(event : pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                return InputEvent(InputEvent.UP_PRESSED)
            if keys[pygame.K_DOWN] :
                return InputEvent(InputEvent.DOWN_PRESSED)
            if keys[pygame.K_RETURN] :
                return InputEvent(InputEvent.SELECT_PRESSED)
        return InputEvent(InputEvent.NONE)

    def register_controller(self, controller : InputControllerInterface):
        self.controllers.add(controller)

    def unregister_controller(self, controller : InputControllerInterface):
        self.controllers.discard(controller)

    def process_pygame_event(self, pygame_event : pygame.event.Event):
        event = GlobalInputController.__define_event(pygame_event)
        if event.event != InputEvent.NONE:
            for controller in self.controllers:
                controller.on_event(event)