from gui.interfaces.abstract_view import *
from gui.scenes.gameover_screen.scene_properties import *
from gui.widgets.sprite import *

class GameOverScreenView(AbstractView):
    def __init__(self, properties_path : str):
        super().__init__()
        properties = SceneProperties(properties_path)
        self.sprite = Sprite(properties.sprite_image, properties.sprite_pos)
        self.add_object(self.sprite)