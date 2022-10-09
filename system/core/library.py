import json
from system.core.spell import *
from system.core.character import *

class Library:
    def __load_spells(self, path : str):
        f = open(path, "r")
        source = json.load(f)
        for s in source:
            spell = Spell(s)
            self.spells[spell.name] = spell
    def __init__(self, spell_path : str):
        self.spells = {}
        self.__load_spells(spell_path)
        sheet = CharacterSheet()
        sheet.name = 'Skeleton'
        sheet.spells = []
        sheet.spells_ai_chance = []
        self.sheets = {sheet.name : sheet}