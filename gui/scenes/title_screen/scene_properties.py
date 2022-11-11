from misc.decorators import *

@fromJson()
@deserialize()
class SceneProperties:
    def __init__(self):
        self.title_pos = [0, 0]
        self.title_image = ''
        self.logo_pos = [0, 0]
        self.logo_image = ''
        self.menu_pos = [0, 0]
        self.menu_font = ''
        self.menu_font_size = 0
        self.menu_font_color_root = [0, 0, 0]
        self.menu_font_color_selected = [0, 0, 0]
        self.menu_font_color_unselected = [0, 0, 0]
        self.menu_font_color_disabled = [0, 0, 0]
        self.menu_interline_size = 0
        self.menu_indent = 40