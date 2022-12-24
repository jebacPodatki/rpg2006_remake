import copy
from system.core.character import *
from system.core.library import *
from system.event.creation_event_receiver import *

class CharacterCreator:

    class ControllerChooseOption(ChooseOptionInterface):
        def __init__(self, creator):
            self.creator = creator

        def choose_option(self, option_id : int):
            self.creator.choose(option_id)

        def back(self):
            self.creator.back()

    class ControllerChooseString(ChooseStringInterface):
        def __init__(self, creator):
            self.creator = creator

        def choose_string(self, string : str):
            self.creator.choose_name(string)

        def back(self):
            self.creator.back()

    class CreationStageInterface:
        def start(self, sheet : CharacterSheet):
            pass
        def choose(self, option_id : int):
            pass
        def choose_string(self, name : str):
            pass

    class ChooseRaceStage(CreationStageInterface):
        def __init__(self, creator):
            self.creator = creator
            self.sheet = None
            self.options = []

        def start(self, sheet : CharacterSheet):
            self.sheet = copy.deepcopy(sheet)
            controller = CharacterCreator.ControllerChooseOption(self.creator)
            self.options = []
            for race in self.creator.library.races:
                self.options.append(race)
            self.creator.event_receiver.on_selecting_race_stage(controller, self.sheet, self.options)

        def choose(self, option_id : int):
            if option_id >= len(self.creator.library.races):
                self.creator.event_receiver.on_wrong_choice()
                return False
            race_name = self.options[option_id]
            self.sheet.race = race_name
            self.sheet.portrait = self.creator.library.races[race_name].portrait
            return True

    class ChooseClassStage(CreationStageInterface):
        def __init__(self, creator):
            self.creator = creator
            self.sheet = None

        def start(self, sheet : CharacterSheet):
            self.sheet = copy.deepcopy(sheet)
            self.options = []
            for main_class in self.creator.library.races[self.sheet.race].classes:
                self.options.append(main_class)
            controller = CharacterCreator.ControllerChooseOption(self.creator)
            self.creator.event_receiver.on_selecting_class_stage(controller, self.sheet, self.options)

        def choose(self, option_id : int):
            classes = self.creator.library.races[self.sheet.race].classes
            if option_id >= len(classes):
                self.creator.event_receiver.on_wrong_choice()
                return False
            class_name = self.options[option_id]
            class_sheet = self.creator.library.get_class_sheet(self.sheet.race, class_name)
            self.sheet = copy.deepcopy(class_sheet)
            self.sheet.name = ''
            return True

    class ChooseNameStage(CreationStageInterface):
        def __init__(self, creator):
            self.creator = creator
            self.sheet = None

        def start(self, sheet : CharacterSheet):
            self.sheet = copy.deepcopy(sheet)
            controller = CharacterCreator.ControllerChooseString(self.creator)
            self.creator.event_receiver.on_selecting_name_stage(controller, self.sheet)

        def choose_string(self, name : str):
            if len(name) > 0:
                self.sheet.name = name
                return True
            else:
                self.creator.event_receiver.on_wrong_name('Character has no name')
                return False

    def __init__(self, library : Library, event_receiver : CreationEventReceiverInterface):
        self.library = library
        self.event_receiver = event_receiver
        self.stages = [CharacterCreator.ChooseRaceStage(self),
                       CharacterCreator.ChooseClassStage(self),
                       CharacterCreator.ChooseNameStage(self)]
        self.current_stage_index = 0

    def back(self):
        if self.current_stage_index <= 1:
            sheet = CharacterSheet()
        else:
            sheet = self.stages[self.current_stage_index - 2].sheet
        if self.current_stage_index > 0:
            self.current_stage_index -= 1
        self.stages[self.current_stage_index].start(sheet)

    def choose(self, option_id : int):
        if option_id == -1:
            self.back()
            return
        result = self.stages[self.current_stage_index].choose(option_id)
        sheet = self.stages[self.current_stage_index].sheet
        if result:
            self.current_stage_index += 1
        if self.current_stage_index >= len(self.stages):
            self.event_receiver.on_creation_finished(sheet)
            return
        self.stages[self.current_stage_index].start(sheet)

    def choose_name(self, name : str):
        sheet = self.stages[self.current_stage_index].sheet
        if self.stages[self.current_stage_index].choose_string(name):
            self.current_stage_index += 1
        if self.current_stage_index >= len(self.stages):
            self.event_receiver.on_creation_finished(sheet)
            return
        self.stages[self.current_stage_index].start(sheet)

    def start(self):
       self.stages[self.current_stage_index].start(CharacterSheet())

    def reset(self):
        self.current_stage_index = 0