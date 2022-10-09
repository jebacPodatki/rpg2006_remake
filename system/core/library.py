from system.core.spell import Spell
from system.core.character import *

class Library:
    def __init__(self):
        spell = Spell()
        spell2 = Spell()
        spell2.name = 'Raise dead'
        spell2.effect = 'raise'
        spell2.impact = [0, 0]
        spell2.dmg = [0, 0]
        spell2.target = Spell.TARGET_NONE
        spell3 = Spell()
        spell3.name = 'Fireball'
        spell3.impact = [60, 120]
        spell3.dmg = [80, 160]
        spell3.target = Spell.TARGET_ALL_ENEMIES
        spell3.mp_cost = 80
        self.spells = {spell.name : spell, spell2.name : spell2, spell3.name : spell3}
        sheet = CharacterSheet()
        sheet.name = 'Skeleton'
        sheet.spells = []
        sheet.spells_ai_chance = []
        self.sheets = {sheet.name : sheet}