import copy
from system.core.action.target import *
from misc.decorators import *

@deserialize()
class CharacterSheet:
    def __init__(self):
        self.name = ''
        self.race = ''
        self.main_class = ''
        self.level = 0
        self.portrait = ''
        self.dead_portrait = ''
        self.strength = 10
        self.endurance = 10
        self.attack = 10
        self.defence = 10
        self.power = 10
        self.will = 10
        self.initiative = 10
        self.action_number = 1
        self.attack_number = 1
        self.breakage = [30, 70]
        self.dmg = [30, 50]
        self.dp = 100
        self.rp = 100
        self.hp = 100
        self.mp = 100
        self.attack_area = ActionTarget.TARGET_SINGLE_ENEMY_FRONTLINE
        self.distant = False
        self.weapon_name = ''
        self.critical_hit_chance = 0
        self.critical_hit_dmg_factor = 1
        self.armor_name = ''
        self.armor = 0
        self.spells = ['Magic bolt']
        self.spells_ai_chance = [30]

class CharacterStats:
    def __init__(self, sheet : CharacterSheet):
        self.dp = sheet.dp
        self.rp = sheet.rp
        self.hp = sheet.hp
        self.mp = sheet.mp
        self.action_number = sheet.action_number

class Character:
    FRONT_LINE = 1
    BACK_LINE = 2
    RED_FACTION = -1
    BLUE_FACTION = 1

    def __init__(self, sheet : CharacterSheet, controlled : bool, faction):
        self.sheet = copy.deepcopy(sheet)
        self.stats = CharacterStats(sheet)
        self.controlled = controlled
        self.faction = faction
        self.line = Character.FRONT_LINE

    def reset(self):
        self.stats = CharacterStats(self.sheet)

    def is_alive(self):
        if self.stats.hp > 0:
            return True
        else:
            return False