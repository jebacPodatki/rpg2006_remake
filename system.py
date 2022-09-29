import copy
import random

class Spell:
    def __init__(self):
        self.name = 'Magic bolt'
        self.impact = [70, 120]
        self.dmg = [60, 90]
        self.effect = ''
        self.mp_cost = 50

class CharacterSheet:
    def __init__(self):
        self.name = ''
        self.strength = 10
        self.endurance = 10
        self.attack = 10
        self.defence = 10
        self.power = 10
        self.will = 10
        self.breakage = [30, 70]
        self.dmg = [30, 50]
        self.dp = 100
        self.rp = 100
        self.hp = 100
        self.mp = 100
        self.spells = ['Magic bolt']

class CharacterStats:
    def __init__(self, sheet : CharacterSheet):
        self.dp = sheet.dp
        self.rp = sheet.rp
        self.hp = sheet.hp
        self.mp = sheet.mp      
        
class Library:
    def __init__(self):
        spell = Spell()
        spell2 = Spell()
        spell2.name = 'Raise dead'
        spell2.effect = 'raise'
        spell2.impact = [0, 0]
        spell2.dmg = [0, 0]
        self.spells = {spell.name : spell, spell2.name : spell2}
        sheet = CharacterSheet()
        sheet.name = 'Skeleton'
        self.sheets = {sheet.name : sheet}
    
    
class Character:
    def __init__(self, sheet : CharacterSheet, controlled : bool, faction):
        self.sheet = copy.deepcopy(sheet)
        self.stats = CharacterStats(sheet)
        self.controlled = controlled
        self.faction = faction
    def reset(self):
        self.stats = CharacterStats(self.sheet)
    def is_alive(self):
        if self.stats.hp > 0:
            return True
        else:
            return False
        
def printChar(chr : Character):
    print('name: ' + str(chr.sheet.name))
    print('breakage: ' + str(chr.sheet.breakage[0]) + ' - ' + str(chr.sheet.breakage[1]))  
    print('damage: ' + str(chr.sheet.dmg[0]) + ' - ' + str(chr.sheet.dmg[1]))
    print('HP: ' + str(chr.stats.hp) + '/' + str(chr.sheet.hp))
    print('DP: ' + str(chr.stats.dp) + '/' + str(chr.sheet.dp))
    
class SpellHelper:
    def __init__(self, library : Library):
        self.library = library
    def can_use(self, character : Character, spell_name):
        if spell_name in library.spells:
            spell = library.spells[spell_name]
            if character.stats.mp >= spell.mp_cost:
                return True
            else:
                return False
        else:
            return False


ACTION_NONE = 0
ACTION_ATTACK = 1
ACTION_MAGIC = 2
ACTION_WAIT = 3
        
class Action:
    def __init__(self, type, actor : Character, target : Character, spell_name):
        self.type = type
        self.actor = actor
        self.target = target
        self.spell_name = spell_name
        
class ActionSelector:
    def select(self, character : Character, characterList, helper : SpellHelper):
        return Action(ACTION_NONE, None, None, '')
    
class AISelector(ActionSelector):
    def select(self, character : Character, character_list, helper : SpellHelper):
        targets = []
        for chr in character_list:
            if chr.faction != character.faction and chr.is_alive():
                targets.append(chr)
        index = random.randint(0, len(targets) - 1)
        return Action(ACTION_ATTACK, character, targets[index], '')
            
class ConsoleSelector(ActionSelector):
    def select(self, character : Character, characterList, helper : SpellHelper):
        print('\033[94m')
        print('Current character: ' + character.sheet.name)
        print('Action: 1 - Attack, 2 - Magic, 3 - Wait')
        action = int(input())
        if action == 3:
            return Action(ACTION_WAIT, character, None, '')
        selected_spell = ''
        if action == 2:
            msg = 'Choose spell: '
            i = 1
            for spell in character.sheet.spells:
                if helper.can_use(character, spell):
                    msg += str(i) + ' - ' + spell + ', '
                    i += 1
            if i > 1:                
                print(msg)
                selected_spell = character.sheet.spells[int(input()) - 1]
            else:
                print("No spells")
                action = 1
        targets = []
        for chr in characterList:
            if chr.faction != character.faction:
                targets.append(chr)
        msg = 'Choose target: '
        i = 1
        for target in targets:
            if target.is_alive():            
                msg += str(i) + ' - ' + target.sheet.name + ', '
            i += 1
        print(msg)
        selected_target = targets[int(input()) - 1]
                            
        if action == 1:
            return Action(ACTION_ATTACK, character, selected_target, '')
        else:
            return Action(ACTION_MAGIC, character, selected_target, selected_spell)
            
class Logger:
    def on_attack(self, attacker : Character, target : Character, damage):
        pass
    def on_block(self, attacker : Character, target : Character):
        pass    
    def on_magic(self, attacker : Character, target : Character, damage, effect, spell_name):
        pass
    def on_magic_block(self, attacker : Character, target : Character):
        pass     
    def on_wait(self, chr : Character):
        pass
    def on_death(self, chr : Character):
        pass
    def on_new_turn(self, current_character : Character, characters):
        pass
    
COLOR = '\033[0m'
COLOR2 = '\033[92m'
class PrintLogger(Logger):
    def on_attack(self, attacker : Character, target : Character, damage):
        print(COLOR)
        print(attacker.sheet.name + ' attacks ' + target.sheet.name + ' and deals ' + str(damage) + ' damage. ' + 
              target.sheet.name + ' has ' + str(target.stats.hp) + ' HP now.')
    def on_block(self, attacker : Character, target : Character):
        print(COLOR)      
        print(attacker.sheet.name + ' attacks ' + target.sheet.name + ' who blocks')        
    def on_magic(self, attacker : Character, target : Character, damage, effect, spell_name):
        print(COLOR)       
        print(attacker.sheet.name + ' casts ' + spell_name + ' against ' + target.sheet.name + ' and deals ' + str(damage) + ' damage. ' + 
              target.sheet.name + ' has ' + str(target.stats.hp) + ' HP now.')
    def on_magic_block(self, attacker : Character, target : Character, spell_name):
        print(COLOR)      
        print(attacker.sheet.name + ' casts ' + spell_name + ' against ' + target.sheet.name + ' who effectively resists magic')      
    def on_wait(self, chr : Character):
        print(COLOR)        
        print(chr.sheet.name + ' is waiting.')
    def on_death(self, chr : Character):
        print(COLOR)        
        print(chr.sheet.name + ' died')
    def on_new_turn(self, current_character : Character, characters):
        if current_character.controlled == False:
            return
        print(COLOR2)        
        for chr in characters:
            print('\t' + chr.sheet.name + '\t\t' + '[' + str(chr.stats.hp) + '/' + str(chr.sheet.hp) + ']')        
 
class Fight:
    def __init__(self, characters, library : Library, selectorA : ActionSelector, selectorB : ActionSelector, logger):
        self.characters = characters
        self.library = library
        self.selector = [selectorA, selectorB]
        self.current = 0
        self.alive = [0, 0]
        self.logger = logger
        for chr in characters:
            self.alive[chr.faction] += 1
                
    def attack(self, attacker, target):
        atk_factor = attacker.sheet.attack / target.sheet.defence
        atk = atk_factor * random.randint(attacker.sheet.breakage[0], attacker.sheet.breakage[1])        
        target.stats.dp -= atk        
        if target.stats.dp <= 0:
            dmg_factor = attacker.sheet.strength / target.sheet.endurance
            dmg = dmg_factor * random.randint(attacker.sheet.dmg[0], attacker.sheet.dmg[1])
            target.stats.hp -= dmg
            self.logger.on_attack(attacker, target, dmg)
            if target.stats.hp < 0:
                self.alive[target.faction] -= 1
                self.logger.on_death(target)
            else:
                target.stats.dp = target.sheet.dp
        else:
            self.logger.on_block(attacker, target)
            
    def magic(self, attacker, target, spell_name):
        if spell_name in self.library.spells:
            spell = self.library.spells[spell_name]
        else:
            return
        if attacker.stats.mp < spell.mp_cost:
            return
        attacker.stats.mp -= spell.mp_cost
        if spell.effect == 'raise':
            sheet = self.library.sheets['Skeleton']
            #skeleton = Character(sheet, False, attacker.faction)
            #self.characters.append(skeleton)
            #self.alive[attacker.faction] += 1
            number = int(attacker.sheet.power / 5)
            if number > 0:
                skeletons = [Character(sheet, False, attacker.faction) for i in range(number)]
                for skeleton in skeletons:
                    self.characters.append(skeleton)
                self.alive[attacker.faction] += number
            return
        atk_factor = attacker.sheet.power / target.sheet.will
        atk = atk_factor * random.randint(spell.impact[0], spell.impact[1])
        target.stats.rp -= atk        
        if target.stats.rp <= 0:
            dmg_factor = attacker.sheet.power / target.sheet.will
            dmg = dmg_factor * random.randint(spell.dmg[0], spell.dmg[1])
            target.stats.hp -= dmg
            self.logger.on_magic(attacker, target, dmg, spell.effect, spell.name)
            if target.stats.hp < 0:
                self.alive[target.faction] -= 1
                self.logger.on_death(target)
            else:
                target.stats.rp = target.sheet.rp
        else:
            self.logger.on_magic_block(attacker, target, spell.name)             
                
    def processAction(self, action : Action):
        if action.type == ACTION_WAIT:
            self.logger.on_wait(action.actor)
        elif action.type == ACTION_ATTACK:
            self.attack(action.actor, action.target)
        elif action.type == ACTION_MAGIC:
            self.magic(action.actor, action.target, action.spell_name)
        else:
            pass
                
    def turn(self):
        current_character = self.characters[self.current]
        if current_character.is_alive():
            logger.on_new_turn(current_character, self.characters)
            if current_character.controlled == True:
                selector = self.selector[0]
            else:
                selector = self.selector[1]
            helper = SpellHelper(self.library)
            action = selector.select(current_character, self.characters, helper)
            self.processAction(action)
        self.current += 1
        if self.current >= len(self.characters):
            self.current = 0
    
    def ended(self):
        if self.alive[0] <= 0 or self.alive[1] <= 0:
            return True
        return False
            
            
sheet1 = CharacterSheet()
sheet1.name = 'Barsel'

sheet2 = CharacterSheet()
sheet2.name = 'Abzare'
sheet2.breakage = [20, 50]
sheet2.dmg = [40, 80]
sheet2.hp = 140

sheet3 = CharacterSheet()
sheet3.name = 'Cersil'
sheet3.mp = 300
sheet3.spells = ['Raise dead']

sheet4 = CharacterSheet()
sheet4.name = 'Dalian'

character = Character(sheet1, True, 0)
character2 = Character(sheet2, False, 1)
character3 = Character(sheet3, True, 0)
character4 = Character(sheet4, False, 1)

printChar(character)
printChar(character2)

library = Library()
ai = AISelector()
console_selector = ConsoleSelector()
logger = PrintLogger()

fight = Fight([character, character2, character3, character4], library, console_selector, ai, logger)

while fight.ended() == False:
    fight.turn()