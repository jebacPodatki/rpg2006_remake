from gui.interfaces.abstract_view import *
from gui.scenes.create_party.scene_properties import *
from gui.widgets.switching_menu import *
from gui.widgets.sprite import *
from gui.widgets.character_sheet_short import *

class CreatePartyView(AbstractView):
    def __init__(self, properties_path : str):
        super(CreatePartyView, self).__init__()
        properties = SceneProperties(properties_path)
        self.menu = SwitchingMenu(properties)
        super(CreatePartyView, self).add_object(self.menu)
        self.title = Sprite(properties.title_image, properties.title_pos)
        super(CreatePartyView, self).add_object(self.title)
        pos_x = 110
        pos_y = 230
        delta_x = 250
        self.character_sheets = [CharacterSheetShort(properties, None, (pos_x, pos_y)),
                                 CharacterSheetShort(properties, None, (pos_x + delta_x, pos_y)),
                                 CharacterSheetShort(properties, None, (pos_x + 2 * delta_x, pos_y)),
                                 CharacterSheetShort(properties, None, (pos_x + 3 * delta_x, pos_y))
        ]
        for character_sheet in self.character_sheets:
            super(CreatePartyView, self).add_object(character_sheet)