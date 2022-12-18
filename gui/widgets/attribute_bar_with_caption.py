import pygame
from gui.widgets.attribute_bar import *
from gui.config import *
from gui.interfaces.drawable import *

class AttributeBarWithCaption(AttributeBar):
    def set_caption(self, caption : str):
        self.caption = self.font.render(caption, 1, self.config.bar_font_color, None)
        self.caption_position = (self.position[0] - self.caption.get_width() / 2 + self.width / 2, self.position[1])

    def __init__(self, config : Config, caption : str = '', position = (0, 0), color = (0, 0, 0), short = False):
        super().__init__(config, position, color, short)
        self.config = config
        self.font = pygame.font.SysFont(config.bar_font, config.bar_font_size)
        self.caption = None
        self.caption_position = position
        self.set_caption(caption)

    def draw(self, screen : pygame.Surface):
        super().draw(screen)
        screen.blit(self.caption, self.caption_position)
