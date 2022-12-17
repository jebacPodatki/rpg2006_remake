import pygame
from gui.interfaces.scene_interface import *
from gui.interfaces.scene_controller_interface import *
from gui.scenes.create_party.create_party_view import *
from gui.scenes.create_party.create_party_view_controller import *

import gui.scenes.fight.fight_scene as fight_scene
import gui.scenes.title_screen.title_screen_scene as title_scene
import gui.scenes.create_character.create_character_scene as create_character_scene

from gameplay.game_state_controller import *
from gameplay.party import *

class CreatePartyScene(SceneInterface):
    def __init__(self, scene_controller : SceneControllerInterface, game_state_controller : GameStateController, party : Party):
        self.view = CreatePartyView('json/create_party_scene.json')
        self.controller = CreatePartyViewController(self.view)
        self.scene_controller = scene_controller
        self.game_state_controller = game_state_controller
        self.party = party

    def on_start(self):
        class ActionInvokerCreateCharacter:
            def __init__(self, game_state_controller : GameStateController, scene_controller : SceneControllerInterface,
                         party : Party, party_position = (0, 0)):
                self.game_state_controller = game_state_controller
                self.scene_controller = scene_controller
                self.party = party
                self.party_position = party_position
            def __call__(self):
                self.scene_controller.next_scene(
                    create_character_scene.CreateCharacterScene(
                        self.scene_controller, self.game_state_controller, self.party, self.party_position))
        class ActionInvokerDeleteCharacter:
            def __init__(self, controller : CreatePartyViewController, party : Party, party_position = (0, 0)):
                self.controller = controller
                self.party = party
                self.party_position = party_position
            def __call__(self):
                self.party.characters[self.party_position[0]][self.party_position[1]] = None
                self.controller.update_menu_partially(self.party)
                self.controller.update_sheets(self.party)
        class ActionInvokerStartJourney:
            def __init__(self, game_state_controller : GameStateController, scene_controller : SceneControllerInterface,
                         party : Party):
                self.game_state_controller = game_state_controller
                self.scene_controller = scene_controller
                self.party = party
            def __call__(self):
                for character in self.party.characters[0]:
                    if character != None:
                        self.game_state_controller.game_state.add_player_character(character, False)
                for character in self.party.characters[1]:
                    if character != None:
                        self.game_state_controller.game_state.add_player_character(character, True)
                self.scene_controller.next_scene(fight_scene.FightScene(self.scene_controller, self.game_state_controller))
        class ActionInvokerExit:
            def __init__(self, game_state_controller : GameStateController, scene_controller : SceneControllerInterface):
                self.game_state_controller = game_state_controller
                self.scene_controller = scene_controller
            def __call__(self):
                self.scene_controller.next_scene(title_scene.TitleScreenScene(self.scene_controller, self.game_state_controller))
        create_character_invokers = [
            ActionInvokerCreateCharacter(self.game_state_controller, self.scene_controller, self.party, (0, 0)),
            ActionInvokerCreateCharacter(self.game_state_controller, self.scene_controller, self.party, (0, 1)),
            ActionInvokerCreateCharacter(self.game_state_controller, self.scene_controller, self.party, (1, 0)),
            ActionInvokerCreateCharacter(self.game_state_controller, self.scene_controller, self.party, (1, 1))
        ]
        delete_character_invokers = [
            ActionInvokerDeleteCharacter(self.controller, self.party, (0, 0)),
            ActionInvokerDeleteCharacter(self.controller, self.party, (0, 1)),
            ActionInvokerDeleteCharacter(self.controller, self.party, (1, 0)),
            ActionInvokerDeleteCharacter(self.controller, self.party, (1, 1))
        ]
        start_invoker = ActionInvokerStartJourney(self.game_state_controller, self.scene_controller, self.party)
        exit_invoker = ActionInvokerExit(self.game_state_controller, self.scene_controller)
        self.controller.update_menu(self.party, create_character_invokers, delete_character_invokers, start_invoker, exit_invoker)
        self.controller.update_sheets(self.party)

    def on_event(self, event : InputEvent):
        self.controller.on_event(event)

    def on_frame(self, screen : pygame.Surface):
        self.view.draw_all(screen)

    def on_update(self):
        pass