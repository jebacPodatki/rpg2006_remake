import pygame
from gui.config import *

class SwitchingMenu:
    def __init__(self, config : Config):
        self.config = config
        self.font = pygame.font.SysFont(config.menu_font, config.menu_font_size)
        self.color_selected = (config.menu_font_color_selected[0],
                               config.menu_font_color_selected[1],
                               config.menu_font_color_selected[2])
        self.color_unselected = (config.menu_font_color_unselected[0],
                               config.menu_font_color_unselected[1],
                               config.menu_font_color_unselected[2])
        self.content = []
        self.selected_index = 0
    def reset(self, lines):
        for line in lines:
            selected = self.font.render(line, 1, self.color_selected)
            unselected = self.font.render(line, 1, self.color_unselected)
            self.content.append([unselected, selected])
    def draw(self, screen):
        delta_y = 0
        for i in range(len(self.content)):
            if i == self.selected_index:
                line = self.content[i][1]
            else:
                line = self.content[i][0]
            screen.blit(line, (self.config.menu_pos[0], self.config.menu_pos[1] + delta_y))
            delta_y += self.config.menu_interline_size
    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.selected_index = (self.selected_index - 1) % len(self.content)           
            if keys[pygame.K_DOWN] :
                self.selected_index = (self.selected_index + 1) % len(self.content)        