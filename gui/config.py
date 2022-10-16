from misc.decorators import *

@fromJson()
@deserialize()
class Config:
    def __init__(self):
        self.window_size = [0, 0]
        self.console_pos = [0, 0]
        self.console_size = [0, 0]
        self.console_font = ''
        self.console_font_size = 0
        self.console_font_color = [0, 0, 0]
        self.console_max_lines = 0
        self.console_interline_size = 0
        self.menu_pos = [0, 0]
        self.menu_font = ''
        self.menu_font_size = 0
        self.menu_font_color_root = [0, 0, 0]
        self.menu_font_color_selected = [0, 0, 0]
        self.menu_font_color_unselected = [0, 0, 0]
        self.menu_interline_size = 0
        self.menu_indent = 10
        self.bar_image = ''
        self.bar_short_image = ''
        self.hud_font  = ''
        self.hud_font_size = 0
        self.hud_font_color = [0, 0, 0]
        self.hud_bar_interline = 0
        self.hud_bar_delta_x = 0
        self.hud_hp_bar_color = [0, 0, 0]
        self.hud_mp_bar_color = [0, 0, 0]
        self.hud_dp_bar_color = [0, 0, 0]
        self.hud_rp_bar_color = [0, 0, 0]