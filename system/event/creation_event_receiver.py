from system.core.character import *

class ChooseOptionInterface:
    def choose_option(self, option_id : int):
        pass
    def back(self):
        pass

class ChooseStringInterface:
    def choose_string(self, string : str):
        pass
    def back(self):
        pass

class CreationEventReceiverInterface:
    def on_selecting_race_stage(self, controller : ChooseOptionInterface, sheet : CharacterSheet, race_options):
        pass
    def on_selecting_class_stage(self, controller : ChooseOptionInterface, sheet : CharacterSheet, class_options):
        pass
    def on_selecting_name_stage(self, controller : ChooseStringInterface, sheet : CharacterSheet):
        pass
    def on_creation_finished(self, sheet : CharacterSheet):
        pass
    def on_wrong_choice(self, controller : ChooseOptionInterface):
        pass
    def on_wrong_name(self, controller : ChooseStringInterface, error : str):
        pass