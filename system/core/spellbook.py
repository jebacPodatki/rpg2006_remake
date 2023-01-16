import random
from system.core.character import *
from system.core.library import Library
from system.core.spell import *
from system.core.action.helper import *

class Spellbook:
    def __init__(self, characters, library : Library, helper : ActionHelper):
        self.characters = characters
        self.library = library
        self.helper = helper

    def invoke_spell_effect(self, spell : Spell, spell_effect : str, caster : Character, target : Character):
        class SpellbookLibrary:
            def summon_undeads(spell : Spell, caster : Character, targets, spellbook : Spellbook):
                sheet = spellbook.library.sheets['Skeleton']
                number = int(caster.sheet.power / 5)
                if number > 0:
                    skeletons = []
                    for i in range(number):
                        if self.helper.can_summon(caster) == False:
                            break
                        spellbook.characters.append(Character(sheet, False, caster.faction))
                    return skeletons
                return []

            def heal(spell : Spell, caster : Character, target, spellbook : Spellbook):
                heal_factor = caster.sheet.power / 20
                heal_value = int(heal_factor * random.randint(spell.dmg[0], spell.dmg[1]))
                target.stats.hp += heal_value
                if target.stats.hp > target.sheet.hp:
                    target.stats.hp = target.sheet.hp
                return [target]

        return SpellbookLibrary.__dict__[spell_effect](spell, caster, target, self)