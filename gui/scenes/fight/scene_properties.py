from misc.decorators import *

@fromJson()
@deserialize()
class SceneProperties:
    def __init__(self):
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
        self.menu_font_color_disabled = [0, 0, 0]
        self.menu_interline_size = 0
        self.menu_indent = 40
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
        self.portrait_caption_font = ''
        self.portrait_caption_font_size = 0
        self.portrait_caption_font_color = [0, 0, 0]
        self.portrait_caption_font_color_selected_blue = [0, 0, 0]
        self.portrait_caption_font_color_selected_red = [0, 0, 0]
        self.arena_pos = [0, 0]
        self.arena_size = [0, 0]
        self.arena_color = [0, 0, 0]
        self.arena_portrait_delta_x = 0
        self.arena_front_line_pos_delta_y = 0
        self.arena_back_line_pos_delta_y = 0