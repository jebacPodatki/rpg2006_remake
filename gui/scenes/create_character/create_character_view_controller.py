from gui.scenes.create_character.create_character_view import *
from gui.interfaces.scene_controller_interface import *
from gui.widgets.controllers.switching_menu_controller import *
from gui.input.input_event import *

from gameplay.party import *

from system.event.creation_event_receiver import *

class CharacterSheetReadyFunctor:
    def __call__(self, sheet : CharacterSheet):
        pass

class CreateCharacterViewController(SceneControllerInterface):
    def __init__(self, view : CreateCharacterView, character_ready_functor : CharacterSheetReadyFunctor):
        self.view = view
        self.menu_controller = SwitchingMenuController(view.menu)
        self.accept_character_functor = None
        self.exit_functor = None
        self.character_ready_functor = character_ready_functor

    def set_invokers(self, accept_character_functor, exit_functor):
        self.accept_character_functor = accept_character_functor
        self.exit_functor = exit_functor

    def on_event(self, event : InputEvent):
        self.menu_controller.on_event(event)

    def update_menu(self):
        root_node = RootNode('Finish character creation')
        root_node.add_leaf_child('Continue', self.accept_character_functor)
        root_node.add_leaf_child('Back', self.exit_functor)
        self.view.menu.set_root_node(root_node)

    def update_menu_with_options(self, choice_controller : ChooseOptionInterface, title : str, options = []):
        class ActionInvokerChooseOption:
            def __init__(self, choice_controller : ChooseOptionInterface, option_id : int):
                self.choice_controller = choice_controller
                self.option_id = option_id
            def __call__(self):
                self.choice_controller.choose_option(self.option_id)
        class ActionInvokerBack:
            def __init__(self, choice_controller : ChooseOptionInterface):
                self.choice_controller = choice_controller
            def __call__(self):
                self.choice_controller.back()
        root_node = RootNode(title)
        for i in range(len(options)):
            root_node.add_leaf_child('- ' + options[i], ActionInvokerChooseOption(choice_controller, i))
        root_node.add_leaf_child('Back', ActionInvokerBack(choice_controller))
        root_node.add_leaf_child('Exit', self.exit_functor)
        self.view.menu.set_root_node(root_node)

    def update_sheet(self, sheet : CharacterSheet):
        self.view.character_sheet.set_character(sheet)
        self.character_ready_functor(sheet)