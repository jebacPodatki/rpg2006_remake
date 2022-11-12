import pygame
from core.resource_provider import *
from gui.config import *
from gui.interfaces.drawable import *
from system.core.character import *

class CharacterPortrait(DrawableObjectInterface):
    EFFECT_BLOOD = 1
    EFFECT_MOVE_FORWARD = 2
    EFFECT_MOVE_BACKWARD =3

    class BloodEffect:
        def __init__(self, rect = (0, 0, 0, 0)):
            self.rect = pygame.Rect(rect)
            self.fill_color = (250, 94, 94, 80)
        def draw(self, screen : pygame.Surface):
            screen.fill(self.fill_color, self.rect, special_flags = pygame.BLEND_RGBA_MULT)
        def override(self):
            return False

    class MoveEffect:
        def __init__(self, img, pos, character : Character, direction : int):
            self.img = img
            self.pos = [pos[0], pos[1]]
            if character.faction == Character.BLUE_FACTION:
                self.direction = direction
            else:
                self.direction = direction * -1
        def draw(self, screen : pygame.Surface):
            self.pos[1] -= 2 *self.direction
            screen.blit(self.img, (self.pos[0], self.pos[1]))
        def override(self):
            return True

    def __calculate_caption_position(base_pos, img_size, caption_size):
        x = base_pos[0] + img_size[0] / 2 - caption_size[0] / 2
        y = base_pos[1] + img_size[1] + 4
        return (x, y)

    def _get_portrait_path(self, config : Config, portrait_name : str):
        return config.portraits_path + '/' + portrait_name

    def __init__(self, config : Config, character : Character, position = (0, 0)):
        self.position = position
        self.character = character
        self.img = ResourceProvider.get(self._get_portrait_path(config, character.sheet.portrait))
        self.img_dead = ResourceProvider.get(self._get_portrait_path(config, character.sheet.dead_portrait))
        font = pygame.font.SysFont(config.portrait_caption_font, config.portrait_caption_font_size)
        self.caption = font.render(character.sheet.name, 1, config.portrait_caption_font_color)
        if character.faction == Character.BLUE_FACTION:
            selected_color = config.portrait_caption_font_color_selected_blue
        else:
            selected_color = config.portrait_caption_font_color_selected_red
        self.caption_selected = font.render(character.sheet.name, 1, selected_color)
        self.caption_position = CharacterPortrait.__calculate_caption_position(
            position, self.img.get_size(), self.caption.get_size())
        self.selected = False
        self.effect = None
        self.effect_duration = 0
        self.effect_delay = 0

    def add_effect(self, effect_id : int):
        if effect_id == CharacterPortrait.EFFECT_BLOOD:
            rect = (self.position[0], self.position[1], self.img.get_size()[0], self.img.get_size()[1])
            self.effect = CharacterPortrait.BloodEffect(rect)
            self.effect_delay = 14
            self.effect_duration = 7
        elif effect_id == CharacterPortrait.EFFECT_MOVE_FORWARD:
            self.effect = CharacterPortrait.MoveEffect(self.img, self.position, self.character, 1)
            self.effect_delay = 2
            self.effect_duration = 8
        elif effect_id == CharacterPortrait.EFFECT_MOVE_BACKWARD:
            self.effect = CharacterPortrait.MoveEffect(self.img, self.position, self.character, -1)
            self.effect_delay = 4
            self.effect_duration = 6

    def set_position(self, position = (0, 0)):
        dx = self.caption_position[0] - self.position[0]
        dy = self.caption_position[1] - self.position[1]
        self.position = position
        self.caption_position = (position[0] + dx, position[1] + dy)

    def select(self, value : bool):
        self.selected = value

    def draw(self, screen : pygame.Surface):
        if not self.character.is_alive() and self.effect == None:
            screen.blit(self.img_dead, self.position)
        else:
            if self.effect == None or self.effect.override() == False or self.effect_delay > 0:
                screen.blit(self.img, self.position)
                if self.selected:
                    screen.blit(self.caption_selected, self.caption_position)
                else:
                    screen.blit(self.caption, self.caption_position)
        if self.effect != None:
            if self.effect_delay == 0:
                self.effect.draw(screen)
                self.effect_duration -= 1
                if self.effect_duration == 0:
                    self.effect = None
            else:
                self.effect_delay -= 1
