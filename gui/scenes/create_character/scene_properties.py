from misc.decorators import *

@fromJson()
@deserialize()
class SceneProperties:
    def __init__(self):
        self.title_pos = [0, 0]
        self.title_image = ''
        self.menu_pos = [0, 0]
        self.menu_font = ''
        self.menu_font_size = 0
        self.menu_font_color_root = [0, 0, 0]
        self.menu_font_color_selected = [0, 0, 0]
        self.menu_font_color_unselected = [0, 0, 0]
        self.menu_font_color_disabled = [0, 0, 0]
        self.menu_interline_size = 0
        self.menu_indent = 40
        self.text_field_size = [0, 0]
        self.text_field_font = ''
        self.text_field_font_size = 0
        self.text_field_font_color = [0, 0, 0]
        self.text_field_max_length = 0
        self.portraits_path = ''
        self.character_sheet_pos = [0, 0]
        self.bar_image = ''
        self.bar_short_image = ''
        self.bar_font = ''
        self.bar_font_size = 0
        self.bar_font_color = [0, 0, 0]
        self.sheet_hp_bar_color = [0, 0, 0]
        self.sheet_mp_bar_color = [0, 0, 0]
        self.sheet_dp_bar_color = [0, 0, 0]
        self.sheet_rp_bar_color = [0, 0, 0]