from gui.scenes.create_character.create_character_view import *
from gui.interfaces.scene_controller_interface import *
from gui.widgets.controllers.switching_menu_controller import *
from gui.input.input_event import *

from gameplay.party import *

class CreateCharacterViewController(SceneControllerInterface):
    def __init__(self, view : CreateCharacterView):
        self.view = view
        self.menu_controller = SwitchingMenuController(view.menu)

    def on_event(self, event : InputEvent):
        self.menu_controller.on_event(event)

    def update_menu(self, accept_character_functor, exit_functor):
        root_node = RootNode('')
        root_node.add_leaf_child('Accept character', accept_character_functor)
        root_node.add_leaf_child('Back', exit_functor)
        self.view.menu.set_root_node(root_node)

    def update_sheet(self, sheet : CharacterSheet):
        self.view.character_sheet.set_character(sheet)