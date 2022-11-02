import pygame
from gui.input.input_event import *
from gui.input.input_controller_interface import *
from gui.interfaces.scene_controller_interface import *
from gui.scenes.fight.fight_scene import *

from gameplay.game_state_controller import *

class SceneManager(SceneControllerInterface, InputControllerInterface):
    def __init__(self, game_state_controller : GameStateController):
        self.game_state_controller = game_state_controller
        self.current_scene = FightScene(self, self.game_state_controller)
        self.current_scene.on_start()

    def next_scene(self, scene: SceneInterface):
        self.current_scene.on_end()
        self.current_scene = scene
        self.current_scene.on_start()

    def on_frame(self, screen : pygame.Surface):
        self.current_scene.on_frame(screen)

    def on_update(self):
        self.current_scene.on_update()

    def on_event(self, event : InputEvent):
        self.current_scene.on_event(event)