import pygame
import copy
from gui.interfaces.scene_interface import *
from gui.interfaces.scene_controller_interface import *
from gui.scenes.create_character.create_character_view import *
from gui.scenes.create_character.create_character_view_controller import *
from gui.scenes.create_character.creation_event_receiver import *

import gui.scenes.create_party.create_party_scene as party_scene

from gameplay.game_state_controller import *
from gameplay.party import *

from system.creation.character_creator import *

class CreateCharacterScene(SceneInterface):
    def __init_view_controller_invokers(self):
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
        self.controller.set_invokers(accept_invoker, exit_invoker)

    def __init__(self, scene_controller : SceneControllerInterface, game_state_controller : GameStateController, party : Party,
                 character_pos = (0, 0)):
        class SetCharacterFunctor(CharacterSheetReadyFunctor):
            def __init__(self, owner, character_pos):
                self.owner = owner
                self.character_pos = character_pos
            def __call__(self, sheet : CharacterSheet):
                self.owner.new_party.characters[self.character_pos[0]][self.character_pos[1]] = sheet
        self.view = CreateCharacterView('json/create_character_scene.json')
        self.controller = CreateCharacterViewController(self.view, SetCharacterFunctor(self, character_pos))
        self.scene_controller = scene_controller
        self.game_state_controller = game_state_controller
        self.party = party
        self.new_party = copy.deepcopy(party)
        self.creator = CharacterCreator(self.game_state_controller.library, CreationEventReceiver(self.controller))
        self.__init_view_controller_invokers()

    def on_start(self):
        self.creator.start()

    def on_event(self, event : InputEvent):
        self.controller.on_event(event)

    def on_frame(self, screen : pygame.Surface):
        self.view.draw_all(screen)

    def on_update(self):
        pass