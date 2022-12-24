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
        self.strength = 0
        self.endurance = 0
        self.attack = 0
        self.defence = 0
        self.power = 0
        self.will = 0
        self.initiative = 0
        self.action_number = 0
        self.attack_number = 0
        self.breakage = [0, 0]
        self.dmg = [0, 0]
        self.dp = 0
        self.rp = 0
        self.hp = 0
        self.mp = 0
        self.attack_area = ActionTarget.TARGET_SINGLE_ENEMY_FRONTLINE
        self.distant = False
        self.weapon_name = ''
        self.critical_hit_chance = 0
        self.critical_hit_dmg_factor = 0
        self.armor_name = ''
        self.armor = 0
        self.spells = []
        self.spells_ai_chance = []

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