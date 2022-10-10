import json
from system.core.spell import *
from system.core.character import *

class Library:
    def __load_json(self, path : str):
        f = open(path, "r")
        source = json.load(f)
        return source

    def __load_spells(self, path : str):
        for s in self.__load_json(path):
            spell = Spell(s)
            self.spells[spell.name] = spell

    def __load_sheets(self, path : str):
        for s in self.__load_json(path):
            sheet = CharacterSheet(s)
            self.sheets[sheet.name] = sheet

    def __init__(self, spell_path : str, sheet_path):
        self.spells = {}
        self.sheets = {}
        self.__load_spells(spell_path)
        self.__load_sheets(sheet_path)