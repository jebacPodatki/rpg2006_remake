from system.core.character import *
from system.core.library import Library
from system.core.action.helper import *

class Spellbook:
    def __init__(self, characters, library : Library, helper : ActionHelper):
        self.characters = characters
        self.library = library
        self.helper = helper
    def invoke_spell_effect(self, spell_effect : str, caster : Character, targets):
        class SpellbookLibrary:
            def summon_undeads(caster : Character, targets, spellbook : Spellbook):
                sheet = spellbook.library.sheets['Skeleton']
                number = int(caster.sheet.power / 5)
                if number > 0:
                    skeletons = [Character(sheet, False, caster.faction) for i in range(number)]
                    for skeleton in skeletons:
                        spellbook.characters.append(skeleton)
                        if self.helper.can_summon(caster) == False:
                            break
                    return skeletons
                return []
        return SpellbookLibrary.__dict__[spell_effect](caster, targets, self)