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
        self.menu_font_color_selected = [0, 0, 0]
        self.menu_font_color_unselected = [0, 0, 0]
        self.menu_interline_size = 0