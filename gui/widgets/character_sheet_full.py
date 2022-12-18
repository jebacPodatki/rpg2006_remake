import pygame
from core.resource_provider import *
from gui.config import *
from gui.interfaces.drawable import *
from gui.widgets.sprite import *
from gui.widgets.text_field import *
from gui.widgets.attribute_bar_with_caption import *
from system.core.character import *

class CharacterSheetFull(DrawableObjectInterface):
    def __get_portrait_path(self, config : Config, portrait_name : str):
        return config.portraits_path + '/' + portrait_name

    def set_character(self, character : CharacterSheet):
        if character != None:
            self.portrait = Sprite(self.__get_portrait_path(self.config, character.portrait), self.position)
            self.name_label.set_text(character.name)
            self.level_label.set_text('Lv. ' + str(character.level))
            self.race_label.set_text(character.race)
            self.class_label.set_text(character.main_class)
            self.strength_label.set_text(str(character.strength))
            self.endurance_label.set_text(str(character.endurance))
            self.attack_label.set_text(str(character.attack))
            self.defence_label.set_text(str(character.defence))
            self.power_label.set_text(str(character.power))
            self.will_label.set_text(str(character.will))
            self.initiative_label.set_text(str(character.initiative))
            self.hp_bar.set_caption('HP ' + str(character.hp))
            self.hp_bar.set_value(1.0)
            self.dp_bar.set_caption('DP ' + str(character.dp))
            self.dp_bar.set_value(1.0)
            self.rp_bar.set_caption('RP ' + str(character.rp))
            self.rp_bar.set_value(1.0)
            self.mp_bar.set_caption('MP ' + str(character.mp))
            self.mp_bar.set_value(1.0)
            self.weapon_label.set_text(character.weapon_name)
            self.attack_number_label.set_text(str(character.attack_number))
            self.damage_label.set_text(str(character.dmg[0]) + ' - ' + str(character.dmg[1]))
            self.breakage_label.set_text(str(character.breakage[0]) + ' - ' + str(character.breakage[1]))
            for i in range(len(self.spell_labels)):
                if i < len(character.spells):
                    self.spell_labels[i].set_text(character.spells[i])
                else:
                    self.spell_labels[i].set_text('')
        else:
            self.portrait = None
            self.name_label.set_text('')
            self.level_label.set_text('')
            self.race_label.set_text('')
            self.class_label.set_text('')
            self.strength_label.set_text('-')
            self.endurance_label.set_text('-')
            self.attack_label.set_text('-')
            self.defence_label.set_text('-')
            self.power_label.set_text('-')
            self.will_label.set_text('-')
            self.initiative_label.set_text('-')
            self.hp_bar.set_caption('')
            self.hp_bar.set_value(0)
            self.dp_bar.set_caption('')
            self.dp_bar.set_value(0)
            self.rp_bar.set_caption('')
            self.rp_bar.set_value(0)
            self.mp_bar.set_caption('')
            self.mp_bar.set_value(0)
            self.weapon_label.set_text('-')
            self.attack_number_label.set_text('-')
            self.damage_label.set_text('-')
            self.breakage_label.set_text('-')
            for spell_label in self.spell_labels:
                spell_label.set_text('')

    def __create_attribute_label(self, config : Config, name : str, left : bool, position = (0, 0), color = (0, 0, 0)):
        if left:
            label_pos_x = position[0]
            field_pos_x = position[0] + 105
        else:
            label_pos_x = position[0] + 70
            field_pos_x = position[0]
        label = TextField(config, (label_pos_x, position[1]), color, False)
        label.set_text(name)
        self.labels.append(label)
        value_label = TextField(config, (field_pos_x, position[1]))
        self.labels.append(value_label)
        return value_label

    def __create_secondary_attribute_label(self, config : Config, name : str, position = (0, 0), color = (0, 0, 0)):
        label = TextField(config, (position[0], position[1]), color, False)
        label.set_text(name)
        self.labels.append(label)
        value_label = TextField(config, (position[0] + 140, position[1]), color, False)
        self.labels.append(value_label)
        return value_label

    def __create_attribute_bar(self, config : Config, name : str, position = (0, 0), color = (0, 0, 0), short = False):
        bar = AttributeBarWithCaption(config, name, (position[0], position[1]), color, short)
        self.labels.append(bar)
        return bar

    def __init__(self, config : Config, character : CharacterSheet, position = (0, 0)):
        self.config = config
        self.character = character
        self.position = position
        self.portrait = None
        self.portrait_border = (position[0],
                                position[1],
                                80,
                                80)
        color = (200, 200, 200)
        basic_info_pos_x = 100
        basic_info_right_pos_x = 240
        basic_info_pos_y = 60
        exp_bar_pos_y = 35
        margin = 10
        delta_y = 35
        delta_y2 = 25
        attribute_area_pos_y = 100
        right_attib_pos_x = 160
        bar_area_pos_y = 250
        bar_area_pos_y_delta = 20
        weapon_area_pos_y = 345
        spell_area_pos_y = 465
        self.name_label = TextField(config, (position[0] + basic_info_pos_x, position[1]), color, False)
        self.level_label = TextField(config, (position[0] + basic_info_right_pos_x, position[1]), color, False)
        self.race_label = TextField(config, (position[0] + basic_info_pos_x, position[1] + basic_info_pos_y), color, False)
        self.class_label = TextField(config, (position[0] + basic_info_right_pos_x, position[1] + basic_info_pos_y), color, False)
        self.labels = [self.name_label, self.level_label, self.race_label, self.class_label]
        self.exp_bar = self.__create_attribute_bar(
            config, 'Exp 0/100', (position[0] + basic_info_pos_x, position[1] + exp_bar_pos_y), (150, 150, 0), True)
        self.exp_bar.set_value(0.0)
        self.strength_label = self.__create_attribute_label(
            config, 'Strength', True, (position[0], position[1] + attribute_area_pos_y), color)
        self.endurance_label = self.__create_attribute_label(
            config, 'Endurance', False, (position[0] + right_attib_pos_x, position[1] + attribute_area_pos_y), color)
        self.attack_label = self.__create_attribute_label(
            config, '    Attack', True, (position[0], position[1] + attribute_area_pos_y + delta_y), color)
        self.defence_label = self.__create_attribute_label(
            config, 'Defence', False, (position[0] + right_attib_pos_x, position[1] + attribute_area_pos_y + delta_y), color)
        self.power_label = self.__create_attribute_label(
            config, '    Power', True, (position[0], position[1] + attribute_area_pos_y + 2 * delta_y), color)
        self.will_label = self.__create_attribute_label(
            config, 'Will', False, (position[0] + right_attib_pos_x, position[1] + attribute_area_pos_y + 2 * delta_y), color)
        self.initiative_label = self.__create_secondary_attribute_label(
            config, 'Initiative', (position[0], position[1] + attribute_area_pos_y + 3 * delta_y), color)
        self.hp_bar = self.__create_attribute_bar(
            config, '', (position[0] + margin, position[1] + bar_area_pos_y), config.sheet_hp_bar_color)
        self.dp_bar = self.__create_attribute_bar(
            config, '', (position[0] + margin, position[1] + bar_area_pos_y + bar_area_pos_y_delta), config.sheet_dp_bar_color)
        self.rp_bar = self.__create_attribute_bar(
            config, '', (position[0] + margin, position[1] + bar_area_pos_y + 2*bar_area_pos_y_delta), config.sheet_rp_bar_color)
        self.mp_bar = self.__create_attribute_bar(
            config, '', (position[0] + margin, position[1] + bar_area_pos_y + 3*bar_area_pos_y_delta), config.sheet_mp_bar_color)
        self.weapon_label = self.__create_secondary_attribute_label(
            config, 'Weapon:', (position[0], position[1] + weapon_area_pos_y), color)
        self.attack_number_label = self.__create_secondary_attribute_label(
            config, 'Attacks', (position[0] + margin, position[1] + weapon_area_pos_y + delta_y2), color)
        self.damage_label = self.__create_secondary_attribute_label(
            config, 'Damage', (position[0] + margin, position[1] + weapon_area_pos_y + 2 * delta_y2), color)
        self.breakage_label = self.__create_secondary_attribute_label(
            config, 'Breakage', (position[0] + margin, position[1] + weapon_area_pos_y + 3 * delta_y2), color)
        self.__create_secondary_attribute_label(
            config, 'Spells:', (position[0], position[1] + spell_area_pos_y), color)
        self.spell_labels = []
        for i in range(5):
            spell_label = TextField(
                config, (position[0] + margin, position[1] + spell_area_pos_y + (i + 1) * delta_y2), color, False)
            self.spell_labels.append(spell_label)
            self.labels.append(spell_label)
        if character != None:
            self.set_character(character)

    def draw(self, screen : pygame.Surface):
        #pygame.draw.rect(screen, (30, 30, 30), (self.position[0] - 5, self.position[1] - 5, 340, 540), 2)
        pygame.draw.rect(screen, (90, 90, 90), self.portrait_border, 5)
        pygame.draw.line(screen, (30, 30, 30),
                         (self.position[0] + 30, self.position[1] + 240), (self.position[0] + 280, self.position[1] + 240), 3)
        pygame.draw.line(screen, (30, 30, 30),
                         (self.position[0] + 30, self.position[1] + 335), (self.position[0] + 280, self.position[1] + 335), 3)
        pygame.draw.line(screen, (30, 30, 30),
                         (self.position[0] + 30, self.position[1] + 450), (self.position[0] + 280, self.position[1] + 450), 3)
        if self.portrait != None:
            self.portrait.draw(screen)
        for label in self.labels:
            label.draw(screen)