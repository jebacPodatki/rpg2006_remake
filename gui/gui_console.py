import pygame
from gui.config import *

class GUIConsole:
    def __init__(self, config : Config):
        self.config = config
        self.color = (config.console_font_color[0], config.console_font_color[1], config.console_font_color[2])
        self.font = pygame.font.SysFont(config.console_font, config.console_font_size)
        self.content = []
        self.console_rect = (self.config.console_pos[0],
                             self.config.console_pos[1],
                             self.config.console_size[0],
                             self.config.console_size[1])
    def print_on(self, text : str):
        line = self.font.render(text, 1, self.color)
        self.content.append(line)
        if len(self.content) > self.config.console_max_lines:
            del self.content[0]
    def draw(self, screen):
        pygame.draw.rect(screen, (20, 20, 20), self.console_rect, 2)
        delta_y = 2
        for line in self.content:
            screen.blit(line, (self.config.console_pos[0] + 4, self.config.console_pos[1] + delta_y))
            delta_y += self.config.console_interline_size