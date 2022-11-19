from gui.input.input_controller_interface import *
from gui.widgets.text_field import *
from gui.input.input_event import *

class TextFieldController(InputControllerInterface):
    def __init__(self, text_field : TextField):
        self.text_field = text_field

    def __event_to_character(self, event : InputEvent, uppercase : bool):
        delta = event.event - InputEvent.A_PRESSED
        if uppercase:
            return chr(ord('A') + delta)
        return chr(ord('a') + delta)

    def on_event(self, event : InputEvent):
        if event.event >= InputEvent.A_PRESSED and event.event <= InputEvent.Z_PRESSED:
            text = self.text_field.get_text()
            if len(text) == 0:
                self.text_field.set_text(self.__event_to_character(event, True))
            else:
                text += self.__event_to_character(event, False)
                self.text_field.set_text(text)
        elif event.event == InputEvent.BACKSPACE_PRESSED:
            text = self.text_field.get_text()
            self.text_field.set_text(text[:len(text)-1])