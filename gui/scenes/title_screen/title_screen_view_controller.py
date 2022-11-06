from gui.scenes.title_screen.title_screen_view import *
from gui.interfaces.scene_controller_interface import *
from gui.widgets.controllers.switching_menu_controller import *
from gui.input.input_event import *

class TitleScreenViewController(SceneControllerInterface):
    def __init__(self, view : TitleScreenView):
        self.view = view
        self.menu_controller = SwitchingMenuController(view.menu)

    def on_event(self, event : InputEvent):
        self.menu_controller.on_event(event)

    def update_menu(self, continue_functor, new_game_functor, exit_functor):
        root_node = RootNode('')
        root_node.add_leaf_child('Continue', continue_functor, False)
        root_node.add_leaf_child('New game', new_game_functor)
        root_node.add_leaf_child('Exit', exit_functor)
        self.view.menu.set_root_node(root_node)