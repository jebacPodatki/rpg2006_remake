from gui.interfaces.abstract_view import *
from gui.scenes.title_screen.scene_properties import *
from gui.widgets.switching_menu import *
from gui.widgets.sprite import *

class TitleScreenView(AbstractView):
    def __init__(self, properties_path : str):
        super(TitleScreenView, self).__init__()
        properties = SceneProperties(properties_path)
        self.menu = SwitchingMenu(properties)
        super(TitleScreenView, self).add_object(self.menu)
        self.title = Sprite(properties.title_image, properties.title_pos)
        super(TitleScreenView, self).add_object(self.title)