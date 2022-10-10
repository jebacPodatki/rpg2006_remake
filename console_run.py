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

library = Library('json/spells.json', 'json/sheets.json')

character = Character(library.sheets['Barsel'], True, Character.RED_FACTION)
character2 = Character(library.sheets['Abzare'], False, Character.BLUE_FACTION)
character3 = Character(library.sheets['Cersil'], True, Character.RED_FACTION)
character3.line = Character.BACK_LINE
character4 = Character(library.sheets['Dalian'], False, Character.BLUE_FACTION)
character4.line = Character.BACK_LINE

printChar(character)
printChar(character2)

ai = AISelector()
console_selector = ConsoleSelector()
logger = ConsoleEventReceiver()

fight = Fight([character, character2, character3, character4], library, console_selector, ai, logger)

while fight.ended() == False:
    fight.process()