import pygame
from gui.input_interface import *

class InputController:
    def __init__(self):
        self.objects = []
        pass
    def __process_event_on_object(self, object : InputInterface, event):
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                object.on_up()
            if keys[pygame.K_DOWN] :
                object.on_down()
            if keys[pygame.K_RETURN] :
                object.on_select()
    def register_object(self, object : InputInterface):
        self.objects.append(object)
    def process_pygame_event(self, pygame_event):
        for object in self.objects:
            self.__process_event_on_object(object, pygame_event)