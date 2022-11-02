from gui.scenes.fight.fight_view import *
from gui.interfaces.scene_controller_interface import *
from gui.widgets.controllers.switching_menu_controller import *
from gui.input.input_event import *

class FightViewController(SceneControllerInterface):
    def __init__(self, view : FightView):
        self.view = view
        self.menu_controller = SwitchingMenuController(view.menu)

    def on_event(self, event : InputEvent):
        self.menu_controller.on_event(event)