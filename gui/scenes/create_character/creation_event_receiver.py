from gui.scenes.create_character.create_character_view_controller import *
from system.core.character import *
from system.core.library import *
from system.event.creation_event_receiver import *

class CreationEventReceiver(CreationEventReceiverInterface):
    def __init__(self, controller : CreateCharacterViewController):
        self.controller = controller

    def on_wrong_choice(self):
        pass

    def on_wrong_name(self, error : str):
        pass

    def on_selecting_race_stage(self, choice_controller : ChooseOptionInterface, sheet : CharacterSheet, races):
        self.controller.update_menu_with_options(choice_controller, 'Choose race', races)
        self.controller.update_sheet(None)

    def on_selecting_class_stage(self, choice_controller : ChooseOptionInterface, sheet : CharacterSheet, classes):
        self.controller.update_menu_with_options(choice_controller, 'Choose class', classes)
        self.controller.update_sheet(sheet)

    def on_selecting_name_stage(self, choice_controller : ChooseStringInterface, sheet : CharacterSheet):
        choice_controller.choose_string(sheet.main_class)

    def on_creation_finished(self, sheet : CharacterSheet):
        self.controller.update_menu()
        self.controller.update_sheet(sheet)