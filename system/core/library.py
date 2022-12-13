import json
from system.core.spell import *
from system.core.character import *
from system.core.encounter import *
from system.core.race import *

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

    def __load_encounters(self, path : str):
        for s in self.__load_json(path):
            sheet = Encounter(s)
            self.encounters[sheet.name] = sheet

    def __load_races(self, path : str):
        for s in self.__load_json(path):
            sheet = Race(s)
            self.races[sheet.name] = sheet

    def __init__(self, spell_path : str, sheet_path : str, encounter_path : str, races_path : str):
        self.spells = {}
        self.sheets = {}
        self.encounters = {}
        self.races = {}
        self.__load_spells(spell_path)
        self.__load_sheets(sheet_path)
        self.__load_encounters(encounter_path)
        self.__load_races(races_path)