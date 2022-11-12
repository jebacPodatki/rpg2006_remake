from gui.scenes.fight.fight_view import *
from gui.interfaces.scene_controller_interface import *
from gui.widgets.controllers.switching_menu_controller import *
from gui.input.input_event import *
from system.core.character import *

class FightViewController(SceneControllerInterface):
    def __init__(self, view : FightView):
        self.view = view
        self.menu_controller = SwitchingMenuController(view.menu)

    def on_event(self, event : InputEvent):
        self.menu_controller.on_event(event)

    def update_hud(self):
        self.view.hud.update()

    def update_arena(self):
        self.view.arena.update()

    def set_selected_character(self, character : Character):
        self.view.arena.set_selected_character(character)

    def show_effect(self, character : Character, effect : int):
        self.view.arena.show_effect_on_character(character, effect)