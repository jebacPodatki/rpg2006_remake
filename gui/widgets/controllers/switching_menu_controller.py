from gui.input.input_controller_interface import *
from gui.widgets.switching_menu import *
from gui.input.input_event import *

class SwitchingMenuController(InputControllerInterface):
    def __init__(self, menu : SwitchingMenu):
        self.menu = menu

    def on_event(self, event : InputEvent):
        if event.event == InputEvent.DOWN_PRESSED:
            self.menu.select_down()
        elif event.event == InputEvent.UP_PRESSED:
            self.menu.select_up()
        elif event.event == InputEvent.SELECT_PRESSED:
            self.menu.activate()