import pygame
from core.resource_provider import *
from gui.config import *
from gui.interfaces.drawable import *
from gui.widgets.sprite import *
from gui.widgets.text_field import *
from system.core.character import *

class CharacterSheetShort(DrawableObjectInterface):
    def __get_portrait_path(self, config : Config, portrait_name : str):
        return config.portraits_path + '/' + portrait_name

    def set_character(self, character : CharacterSheet):
        if character != None:
            self.portrait = Sprite(self.__get_portrait_path(self.config, character.portrait), self.position)
            self.name_label.set_text(character.name)
            self.race_label.set_text(character.race)
            self.class_label.set_text(character.main_class)
            self.strength_label.set_text(str(character.strength))
            self.endurance_label.set_text(str(character.endurance))
            self.attack_label.set_text(str(character.attack))
            self.defence_label.set_text(str(character.defence))
            self.power_label.set_text(str(character.power))
            self.will_label.set_text(str(character.will))
            self.hp_label.set_text(str(character.hp))
            self.dp_label.set_text(str(character.dp))
            self.mp_label.set_text(str(character.mp))
            self.rp_label.set_text(str(character.rp))

        else:
            self.portrait = None
            self.name_label.set_text('-')
            self.race_label.set_text('-')
            self.class_label.set_text('-')
            self.strength_label.set_text('')
            self.endurance_label.set_text('')
            self.attack_label.set_text('')
            self.defence_label.set_text('')
            self.power_label.set_text('')
            self.will_label.set_text('')
            self.hp_label.set_text('')
            self.dp_label.set_text('')
            self.mp_label.set_text('')
            self.rp_label.set_text('')

    def __create_attribute_label(self, config : Config, name : str, left : bool, position = (0, 0), color = (0, 0, 0)):
        if left:
            label_pos_x = position[0]
            field_pos_x = position[0] + 45
        else:
            label_pos_x = position[0] + 45
            field_pos_x = position[0]
        label = TextField(config, (label_pos_x, position[1]), color, False)
        label.set_text(name)
        self.labels.append(label)
        value_label = TextField(config, (field_pos_x, position[1]))
        self.labels.append(value_label)
        return value_label

    def __init__(self, config : Config, character : CharacterSheet, position = (0, 0)):
        self.config = config
        self.character = character
        self.position = position
        self.portrait = None
        self.portrait_border = (position[0], position[1], 80, 80)
        field_color = (120, 120, 120)
        race_class_color = (200, 200, 200)
        name_color = (250, 250, 250)
        label_position_x = 100
        label_delta = 30
        right_field_position_x = 95
        field_position_y = 100
        sec_field_position_y = 215
        delta_y = 35
        self.name_label = TextField(config, (position[0] + label_position_x, position[1]), name_color, False)
        self.race_label = TextField(config, (position[0] + label_position_x, position[1] + label_delta), race_class_color, False)
        self.class_label = TextField(config, (position[0] + label_position_x, position[1] +2*label_delta), race_class_color, False)
        self.labels = [self.name_label, self.race_label, self.class_label]
        self.strength_label = self.__create_attribute_label(
            config, 'STR', True, (position[0], position[1] + field_position_y), field_color)
        self.endurance_label = self.__create_attribute_label(
            config, 'END', False, (position[0] + right_field_position_x, position[1] + field_position_y), field_color)
        self.attack_label = self.__create_attribute_label(
            config, 'ATK', True, (position[0], position[1] + field_position_y + delta_y), field_color)
        self.defence_label = self.__create_attribute_label(
            config, 'DEF', False, (position[0] + right_field_position_x, position[1] + field_position_y + delta_y), field_color)
        self.power_label = self.__create_attribute_label(
            config, 'POW', True, (position[0], position[1] + field_position_y + 2 * delta_y), field_color)
        self.will_label = self.__create_attribute_label(
            config, 'WIL', False, (position[0] + right_field_position_x, position[1] + field_position_y + 2* delta_y), field_color)
        self.hp_label = self.__create_attribute_label(
            config, ' HP', True, (position[0], position[1] + sec_field_position_y), field_color)
        self.dp_label = self.__create_attribute_label(
            config, 'DP ', False, (position[0] + right_field_position_x, position[1] + sec_field_position_y), field_color)
        self.mp_label = self.__create_attribute_label(
            config, ' MP', True, (position[0], position[1] + sec_field_position_y + delta_y), field_color)
        self.rp_label = self.__create_attribute_label(
            config, 'RP ', False, (position[0] + right_field_position_x, position[1] + sec_field_position_y +delta_y), field_color)
        self.set_character(character)

    def draw(self, screen : pygame.Surface):
        pygame.draw.rect(screen, (30, 30, 30), (self.position[0] - 5, self.position[1] - 5, 190, 290), 2)
        pygame.draw.rect(screen, (90, 90, 90), self.portrait_border, 5)
        if self.portrait != None:
            self.portrait.draw(screen)
        for label in self.labels:
            label.draw(screen)