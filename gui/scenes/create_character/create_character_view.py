from gui.interfaces.abstract_view import *
from gui.scenes.create_character.scene_properties import *
from gui.widgets.switching_menu import *
from gui.widgets.sprite import *
from gui.widgets.character_sheet_full import *

class CreateCharacterView(AbstractView):
    def __init__(self, properties_path : str):
        super().__init__()
        properties = SceneProperties(properties_path)
        self.menu = SwitchingMenu(properties)
        self.add_object(self.menu)
        self.title = Sprite(properties.title_image, properties.title_pos)
        self.add_object(self.title)
        self.character_sheet = CharacterSheetFull(properties, None, properties.character_sheet_pos)
        self.add_object(self.character_sheet)