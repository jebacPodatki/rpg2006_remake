from gui.interfaces.abstract_view import *
from gui.scenes.title_screen.scene_properties import *
from gui.widgets.switching_menu import *
from gui.widgets.sprite import *

class TitleScreenView(AbstractView):
    def __init__(self, properties_path : str):
        super().__init__()
        properties = SceneProperties(properties_path)
        self.menu = SwitchingMenu(properties)
        self.add_object(self.menu)
        self.title = Sprite(properties.title_image, properties.title_pos)
        self.add_object(self.title)
        self.logo = Sprite(properties.logo_image, properties.logo_pos)
        self.add_object(self.logo)