import sys
import pygame
from gui.interfaces.scene_interface import *
from gui.interfaces.scene_controller_interface import *
from gui.scenes.title_screen.title_screen_view import *
from gui.scenes.title_screen.title_screen_view_controller import *
from gui.scenes.create_party.create_party_scene import *

from gameplay.game_state_controller import *
from gameplay.party import *

class TitleScreenScene(SceneInterface):
    def __init__(self, scene_controller : SceneControllerInterface, game_state_controller : GameStateController):
        self.view = TitleScreenView('json/title_screen_scene.json')
        self.controller = TitleScreenViewController(self.view)
        self.scene_controller = scene_controller
        self.game_state_controller = game_state_controller

    def on_start(self):
        class ActionInvokerNewGame:
            def __init__(self, game_state_controller : GameStateController, scene_controller : SceneControllerInterface):
                self.game_state_controller = game_state_controller
                self.scene_controller = scene_controller
            def __call__(self):
                self.game_state_controller.new_game()
                self.scene_controller.next_scene(CreatePartyScene(self.scene_controller, self.game_state_controller, Party()))
        class ActionInvokerExitGame:
            def __init__(self):
                pass
            def __call__(self):
                sys.exit()
        new_game_invoker = ActionInvokerNewGame(self.game_state_controller, self.scene_controller)
        self.controller.update_menu(ActionInvokerExitGame(), new_game_invoker, ActionInvokerExitGame())

    def on_event(self, event : InputEvent):
        self.controller.on_event(event)

    def on_frame(self, screen : pygame.Surface):
        self.view.draw_all(screen)

    def on_update(self):
        pass