import pygame
from gui.interfaces.scene_interface import *
from gui.interfaces.scene_controller_interface import *
from gui.scenes.fight.fight_view import *
from gui.scenes.fight.fight_view_controller import *
from gui.scenes.fight.fight_event_receiver import *
from gui.action_selector import *
from gui.event_receiver import *

import gui.scenes.gameover_screen.gameover_screen_scene as gameover_scene

from gameplay.game_state_controller import *
from gameplay.system_fight_controller import *

class FightScene(SceneInterface):
    def __init__(self, scene_controller : SceneControllerInterface, game_state_controller : GameStateController):
        self.fight_controller = SystemFightController(game_state_controller.library, game_state_controller.game_state)
        self.view = FightView('json/fight_scene.json', self.fight_controller.prepare_characters_for_new_fight())
        self.controller = FightViewController(self.view)
        self.scene_controller = scene_controller
        self.game_state_controller = game_state_controller
        self.fight_event_receiver = FightEventReceiver(self.controller, SystemEventReceiver(self.view.console))
        self.fight_ended = False
        self.fight_ended_time = 0

    def on_start(self):
        selector = InteractiveActionSelector(self.view.menu)
        self.fight_controller.start_new_fight(selector, self.fight_event_receiver)

    def on_event(self, event : InputEvent):
        self.controller.on_event(event)

    def on_frame(self, screen : pygame.Surface):
        self.view.draw_all(screen)

    def on_update(self):
        if self.fight_ended and pygame.time.get_ticks() > self.fight_ended_time + 2000:
            if self.fight_controller.is_player_winner():
                self.scene_controller.next_scene(FightScene(self.scene_controller, self.game_state_controller))
            else:
                self.scene_controller.next_scene(
                    gameover_scene.GameOverScreenScene(self.scene_controller, self.game_state_controller))
            return
        self.fight_controller.process_current_fight()
        if self.fight_controller.is_fight_ended() and self.fight_ended == False:
            self.fight_ended = True
            self.fight_ended_time = pygame.time.get_ticks()