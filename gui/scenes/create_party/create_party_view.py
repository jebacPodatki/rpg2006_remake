from gui.interfaces.abstract_view import *
from gui.scenes.create_party.scene_properties import *
from gui.widgets.switching_menu import *
from gui.widgets.sprite import *

class CreatePartyView(AbstractView):
    def __init__(self, properties_path : str):
        super(CreatePartyView, self).__init__()
        properties = SceneProperties(properties_path)
        self.menu = SwitchingMenu(properties)
        super(CreatePartyView, self).add_object(self.menu)
        self.title = Sprite(properties.title_image, properties.title_pos)
        super(CreatePartyView, self).add_object(self.title)