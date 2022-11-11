import pygame
from gui.input.input_event import *
from gui.input.input_controller_interface import *
from gui.interfaces.scene_controller_interface import *
from gui.scenes.title_screen.title_screen_scene import *

from gameplay.game_state_controller import *

class SceneManager(SceneControllerInterface, InputControllerInterface):
    def next_scene(self, scene: SceneInterface):
        if not self.current_scene == None:
            self.current_scene.on_end()
        self.current_scene = scene
        self.current_scene.on_start()

    def set_initial_scene(self):
        self.next_scene(self.title_scene)

    def __init__(self, game_state_controller : GameStateController):
        self.current_scene = None
        self.game_state_controller = game_state_controller
        self.title_scene = TitleScreenScene(self, self.game_state_controller)
        self.set_initial_scene()

    def on_frame(self, screen : pygame.Surface):
        self.current_scene.on_frame(screen)

    def on_update(self):
        self.current_scene.on_update()

    def on_event(self, event : InputEvent):
        self.current_scene.on_event(event)