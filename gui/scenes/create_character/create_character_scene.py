import pygame
import copy
from gui.interfaces.scene_interface import *
from gui.interfaces.scene_controller_interface import *
from gui.scenes.create_character.create_character_view import *
from gui.scenes.create_character.create_character_view_controller import *

import gui.scenes.create_party.create_party_scene as party_scene

from gameplay.game_state_controller import *
from gameplay.party import *

class CreateCharacterScene(SceneInterface):
    def __prepare_new_party(self, character_pos = (0, 0)):
        party_size = self.party.size()
        if party_size == 0:
            sheet = self.game_state_controller.library.sheets['Barsel']
        elif party_size == 1:
            sheet = self.game_state_controller.library.sheets['Cersil']
        elif party_size == 2:
            sheet = self.game_state_controller.library.sheets['Abzare']
        self.character_sheet = sheet
        self.new_party.characters[character_pos[0]][character_pos[1]] = self.character_sheet

    def __init__(self, scene_controller : SceneControllerInterface, game_state_controller : GameStateController, party : Party,
                 character_pos = (0, 0)):
        self.view = CreateCharacterView('json/create_character_scene.json')
        self.controller = CreateCharacterViewController(self.view)
        self.scene_controller = scene_controller
        self.game_state_controller = game_state_controller
        self.party = party
        self.new_party = copy.deepcopy(party)
        self.character_sheet = None
        self.__prepare_new_party(character_pos)

    def on_start(self):
        class ActionInvokerAccept:
            def __init__(self, game_state_controller : GameStateController, scene_controller : SceneControllerInterface,
                         party : Party):
                self.game_state_controller = game_state_controller
                self.scene_controller = scene_controller
                self.party = party
            def __call__(self):
                self.scene_controller.next_scene(
                    party_scene.CreatePartyScene(self.scene_controller, self.game_state_controller, self.party))
        class ActionInvokerExit:
            def __init__(self, game_state_controller : GameStateController, scene_controller : SceneControllerInterface,
                         party : Party):
                self.game_state_controller = game_state_controller
                self.scene_controller = scene_controller
                self.party = party
            def __call__(self):
                self.scene_controller.next_scene(
                    party_scene.CreatePartyScene(self.scene_controller, self.game_state_controller, self.party))
        accept_invoker = ActionInvokerAccept(self.game_state_controller, self.scene_controller, self.new_party)
        exit_invoker = ActionInvokerExit(self.game_state_controller, self.scene_controller, self.party)
        self.controller.update_menu(accept_invoker, exit_invoker)
        self.controller.update_sheet(self.character_sheet)

    def on_event(self, event : InputEvent):
        self.controller.on_event(event)

    def on_frame(self, screen : pygame.Surface):
        self.view.draw_all(screen)

    def on_update(self):
        pass