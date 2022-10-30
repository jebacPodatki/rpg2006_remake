from gui.controller_interface import ControllerInterface
from gui.controller_interface import *
from gui.widgets.switching_menu import *
from gui.input_event import *

class SwitchingMenuController(ControllerInterface):
    def __init__(self, menu : SwitchingMenu):
        self.menu = menu

    def on_event(self, event : InputEvent):
        if event.event == InputEvent.DOWN:
            self.menu.down()
        elif event.event == InputEvent.UP:
            self.menu.up()
        elif event.event == InputEvent.SELECT:
            self.menu.select()