import pygame
from gui.config import *
from gui.scenes.scene_manager import *
from gui.input.global_input_controller import *
from gameplay.game_state_controller import *

class CoreGUI:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("RPG2006 Remake")
        config = Config('json/config.json')
        self.screen = pygame.display.set_mode((config.window_size[0], config.window_size[1]))
        self.game_state_controller = GameStateController()
        self.game_state_controller.new_game() #temporary
        self.scene_manager = SceneManager(self.game_state_controller)
        self.input_controller = GlobalInputController()
        self.input_controller.register_controller(self.scene_manager)

    def start(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.input_controller.process_pygame_event(event)
            self.screen.fill((0, 0, 0))
            self.scene_manager.on_frame(self.screen)
            self.scene_manager.on_update()
            pygame.display.update()