import pygame
from gui.interfaces.scene_interface import *
from gui.interfaces.scene_controller_interface import *
from gui.scenes.gameover_screen.gameover_screen_view import *
from gui.scenes.title_screen.title_screen_scene import *

from gameplay.game_state_controller import *

class GameOverScreenScene(SceneInterface):
    def __init__(self, scene_controller : SceneControllerInterface, game_state_controller : GameStateController):
        self.view = GameOverScreenView('json/gameover_screen_scene.json')
        self.scene_controller = scene_controller
        self.game_state_controller = game_state_controller

    def on_start(self):
        pass

    def on_event(self, event : InputEvent):
        if event.event == InputEvent.SELECT_PRESSED:
            self.scene_controller.set_initial_scene()

    def on_frame(self, screen : pygame.Surface):
        self.view.draw_all(screen)

    def on_update(self):
        pass