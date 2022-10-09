from system.core.character import *
from system.core.library import Library
from system.core.fight import Fight
from system.ai.ai import *
from console.console_action_selector import *
from console.console_event_receiver import *

def printChar(chr : Character):
    print('name: ' + str(chr.sheet.name))
    print('breakage: ' + str(chr.sheet.breakage[0]) + ' - ' + str(chr.sheet.breakage[1]))  
    print('damage: ' + str(chr.sheet.dmg[0]) + ' - ' + str(chr.sheet.dmg[1]))
    print('HP: ' + str(chr.stats.hp) + '/' + str(chr.sheet.hp))
    print('DP: ' + str(chr.stats.dp) + '/' + str(chr.sheet.dp))
        
sheet1 = CharacterSheet()
sheet1.name = 'Barsel'
sheet1.attack_number = 2

sheet2 = CharacterSheet()
sheet2.name = 'Abzare'
sheet2.breakage = [20, 50]
sheet2.dmg = [40, 80]
sheet2.hp = 140

sheet3 = CharacterSheet()
sheet3.name = 'Cersil'
sheet3.mp = 300
sheet3.spells = ['Raise dead', 'Fireball']
sheet3.spells_ai_chance = [20, 20]
sheet3.initiative = 7

sheet4 = CharacterSheet()
sheet4.name = 'Dalian'

character = Character(sheet1, True, Character.RED_FACTION)
character2 = Character(sheet2, False, Character.BLUE_FACTION)
character3 = Character(sheet3, True, Character.RED_FACTION)
character3.line = Character.BACK_LINE
character4 = Character(sheet4, False, Character.BLUE_FACTION)
character4.line = Character.BACK_LINE

printChar(character)
printChar(character2)

library = Library('json/spells.json')
ai = AISelector()
console_selector = ConsoleSelector()
logger = ConsoleEventReceiver()

fight = Fight([character, character2, character3, character4], library, console_selector, ai, logger)

while fight.ended() == False:
    fight.turn()