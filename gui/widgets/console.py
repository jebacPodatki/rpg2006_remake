import pygame
from gui.config import *
from gui.drawable import *

class Console(DrawableObjectInterface):
    def __calculate_character_per_line_limit(self, console_width : int):
        single_ch_width = self.font.size('A')[0]
        self.character_per_line_limit = int(console_width / single_ch_width)

    def __init__(self, config : Config):
        self.config = config
        self.color = (config.console_font_color[0], config.console_font_color[1], config.console_font_color[2])
        self.font = pygame.font.SysFont(config.console_font, config.console_font_size)
        self.content = []
        self.text_content = []
        self.console_rect = (self.config.console_pos[0],
                             self.config.console_pos[1],
                             self.config.console_size[0],
                             self.config.console_size[1])
        self.__calculate_character_per_line_limit(self.config.console_size[0])

    def __print(self, text : str):
        line = self.font.render(text, 1, self.color)
        self.content.append(line)
        self.text_content.append(text)
        if len(self.content) > self.config.console_max_lines:
            del self.content[0]
            del self.text_content[0]

    def print_on_line(self, text : str):
        if len(self.content) == 0:
            return self.print_new_line(text)
        last_line_index = len(self.text_content) - 1
        last_line_text = self.text_content[last_line_index]
        del self.text_content[last_line_index]
        del self.content[last_line_index]
        return self.print_new_line(last_line_text + text)

    def print_new_line(self, text : str):
        lines = []
        while len(text) > self.character_per_line_limit:
            line = text[:self.character_per_line_limit]
            text = text[self.character_per_line_limit:]
            lines.append(line)
        lines.append(text)
        for line in lines:
            self.__print(line)

    def draw(self, screen : pygame.Surface):
        pygame.draw.rect(screen, (90, 90, 90), self.console_rect, 3)
        delta_y = 5
        for line in self.content:
            screen.blit(line, (self.config.console_pos[0] + 5, self.config.console_pos[1] + delta_y))
            delta_y += self.config.console_interline_size