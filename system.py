import copy
import random

class Spell:
    TARGET_NONE = 'none'
    TARGET_SINGLE_ENEMY_FRONTLINE = 'single_enemy_frontline'
    TARGET_SINGLE_ENEMY_BOTHLINE = 'single_enemy'
    TARGET_SINGLE_ALLY = 'single_ally'
    TARGET_ALL_ENEMIES_FRONTLINE = 'all_enemies_frontline'
    TARGET_ALL_ENEMIES = 'all_enemies'
    TARGET_ALL_ALLIES = 'all_allies'
    def __init__(self):
        self.name = 'Magic bolt'
        self.impact = [70, 120]
        self.dmg = [60, 90]
        self.effect = ''
        self.mp_cost = 50
        self.target = Spell.TARGET_SINGLE_ENEMY_BOTHLINE

class CharacterSheet:
    def __init__(self):
        self.name = ''
        self.strength = 10
        self.endurance = 10
        self.attack = 10
        self.defence = 10
        self.power = 10
        self.will = 10
        self.initiative = 10
        self.attack_number = 1
        self.breakage = [30, 70]
        self.dmg = [30, 50]
        self.dp = 100
        self.rp = 100
        self.hp = 100
        self.mp = 100
        self.attack_area = Spell.TARGET_SINGLE_ENEMY_FRONTLINE
        self.distant = False
        self.spells = ['Magic bolt']
        self.spells_ai_chance = [30]

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
        
def printChar(chr : Character):
    print('name: ' + str(chr.sheet.name))
    print('breakage: ' + str(chr.sheet.breakage[0]) + ' - ' + str(chr.sheet.breakage[1]))  
    print('damage: ' + str(chr.sheet.dmg[0]) + ' - ' + str(chr.sheet.dmg[1]))
    print('HP: ' + str(chr.stats.hp) + '/' + str(chr.sheet.hp))
    print('DP: ' + str(chr.stats.dp) + '/' + str(chr.sheet.dp))
    
class ActionHelper:
    def __init__(self, library : Library, characters):
        self.library = library
        self.characters = characters
    def can_use(self, character : Character, spell_name):
        if spell_name in library.spells:
            spell = self.library.spells[spell_name]
            if character.stats.mp >= spell.mp_cost:
                return True
            else:
                return False
        else:
            return False
    def can_move(self, character : Character):
        if character.line == Character.FRONT_LINE:
            if self.is_backline_empty(character.faction):
                return False
            possible = True
            character.line = Character.BACK_LINE
            if self.is_frontline_empty(character.faction):
                possible = False
            character.line = Character.FRONT_LINE
            return possible
        return True
    def is_single_target(self, spell_name):
        if spell_name in self.library.spells:
            spell = self.library.spells[spell_name]
            return spell.target == Spell.TARGET_SINGLE_ENEMY_FRONTLINE \
                or spell.target == Spell.TARGET_SINGLE_ENEMY_BOTHLINE \
                or spell.target == Spell.TARGET_SINGLE_ALLY
        else:
            return False
        
    def is_frontline_empty(self, faction):
        for chr in self.characters:
            if chr.is_alive() and chr.faction == faction and chr.line == Character.FRONT_LINE:
                return False
        return True

    def is_backline_empty(self, faction):
        for chr in self.characters:
            if chr.is_alive() and chr.faction == faction and chr.line == Character.BACK_LINE:
                return False
        return True

    def __get_possible_targets(self, character : Character, target_type, with_spell : bool):
        if target_type == Spell.TARGET_NONE:
            return []
        elif target_type == Spell.TARGET_ALL_ALLIES or target_type == Spell.TARGET_ALL_ENEMIES:
            all = []
            if target_type == Spell.TARGET_ALL_ALLIES:
                target_faction = character.faction
            else:
                target_faction = -character.faction
            for chr in self.characters:
                if chr.faction == target_faction and chr.is_alive():
                    all.append(chr)
            return [all]
        elif target_type == Spell.TARGET_SINGLE_ALLY or target_type == Spell.TARGET_SINGLE_ENEMY_BOTHLINE:
            targets = []
            if target_type == Spell.TARGET_SINGLE_ALLY:
                target_faction = character.faction
            else:
                target_faction = -character.faction
            for chr in self.characters:
                if chr.faction == target_faction and chr.is_alive():
                    targets.append([chr])
            return targets
        elif target_type == Spell.TARGET_ALL_ENEMIES_FRONTLINE:
            if self.is_frontline_empty(-character.faction):
                return self.get_possible_targets(character, Spell.TARGET_ALL_ENEMIES)
            if character.line == Character.BACK_LINE and not character.sheet.distant and with_spell == False:
                return []
            all = []
            for chr in self.characters:
                if chr.faction == -character.faction and chr.is_alive() and chr.line == Character.FRONT_LINE:
                    all.append(chr)
            return [all]
        elif target_type == Spell.TARGET_SINGLE_ENEMY_FRONTLINE:
            if self.is_frontline_empty(-character.faction):
                return self.get_possible_targets(character, Spell.TARGET_SINGLE_ENEMY_BOTHLINE)
            if character.line == Character.BACK_LINE and not character.sheet.distant and with_spell == False:
                return []
            targets = []
            for chr in self.characters:
                if chr.faction == -character.faction and chr.is_alive() and chr.line == Character.FRONT_LINE:
                    targets.append([chr])
            return targets

    def get_possible_targets(self, character : Character, spell_name = ''):
        uses_spell = False
        if spell_name == '':
            target_type = character.sheet.attack_area
        else:
            if spell_name in library.spells:
                spell = library.spells[spell_name]
            else:
                return []
            target_type = spell.target
            uses_spell = True
        return self.__get_possible_targets(character, target_type, uses_spell)


class Action:
    ACTION_NONE = 0
    ACTION_ATTACK = 1
    ACTION_MAGIC = 2
    ACTION_WAIT = 3
    ACTION_MOVE = 4
    def __init__(self, type, actor : Character, targets, spell_name):
        self.type = type
        self.actor = actor
        self.targets = targets
        self.spell_name = spell_name
        
class ActionSelector:
    def select(self, character : Character, characterList, helper : ActionHelper):
        return Action(Action.ACTION_NONE, None, [], '')
    
class AISelector(ActionSelector):
    def select(self, character : Character, character_list, helper : ActionHelper):
        selected_spell_name = ''
        for i in range(0, len(character.sheet.spells)):
            if helper.can_use(character, character.sheet.spells[i]) and \
                random.randint(1, 100) < character.sheet.spells_ai_chance[i]:
                selected_spell_name = character.sheet.spells[i]
        target_groups = helper.get_possible_targets(character, selected_spell_name)
        if len(target_groups) == 0:
            selected_targets = []
        elif len(target_groups) == 1:
            if len(target_groups[0]) >= 1:
                selected_targets = target_groups[0]
            else:
                selected_targets = []
        else:
            index = random.randint(0, len(target_groups) - 1)
            selected_targets = target_groups[index]
        if selected_spell_name == '':
            if len(selected_targets) == 0:
                return Action(Action.ACTION_WAIT, character, [], '')
            else:
                return Action(Action.ACTION_ATTACK, character, selected_targets, '')
        else:
            return Action(Action.ACTION_MAGIC, character, selected_targets, selected_spell_name)
            
class ConsoleSelector(ActionSelector):
    def select(self, character : Character, characterList, helper : ActionHelper):
        print('\033[94m')
        print('Current character: ' + character.sheet.name)
        print('Action: 1 - Attack, 2 - Magic, 3 - Wait, 4 - Move.: ', end = " ")
        action = int(input())
        if action == 3:
            return Action(Action.ACTION_WAIT, character, [], '')
        if action == 4:
            if helper.can_move(character):
                return Action(Action.ACTION_MOVE, character, [], '')
            else:
                return Action(Action.ACTION_WAIT, character, [], '')
        selected_spell = ''
        if action == 2:
            msg = 'Choose spell: '
            i = 1
            for spell in character.sheet.spells:
                if helper.can_use(character, spell):
                    msg += str(i) + ' - ' + spell + ', '
                    i += 1
            if i > 1:                
                print(msg + ': ', end = " ")
                selected_spell = character.sheet.spells[int(input()) - 1]
            else:
                print("No spells", end = " ")
                action = 1
        target_groups = helper.get_possible_targets(character, selected_spell)
        if len(target_groups) == 0:
            selected_targets = []
        elif len(target_groups) == 1:
            if len(target_groups[0]) >= 1:
                selected_targets = target_groups[0]
            else:
                selected_targets = []
        else:
            msg = 'Choose target: '
            i = 1
            for target_group in target_groups:
                if len(target_group) == 1:
                    msg += str(i) + ' - ' + target_group[0].sheet.name + ', '
                else:
                    msg += str(i) + ' - ('
                    for target in target_group:
                        msg += target.sheet.name + ', '
                    msg += '),'
                i += 1
            print(msg + ': ', end = " ")
            selected_targets = [target_groups[int(input()) - 1][0]]
        if action == 1:
            return Action(Action.ACTION_ATTACK, character, selected_targets, '')
        else:
            return Action(Action.ACTION_MAGIC, character, selected_targets, selected_spell)
            
class EventReceiver:
    def on_attack(self, attacker : Character, targets):
        pass
    def on_damage(self, character : Character, damage):
        pass    
    def on_block(self, character : Character):
        pass
    def on_cast_spell(self, attacker : Character, targets, spell_name):
        pass
    def on_spell_effect(self, targets, effect):
        pass
    def on_magic_block(self, character : Character):
        pass     
    def on_wait(self, character : Character):
        pass
    def on_death(self, character : Character):
        pass
    def on_new_turn(self, current_character : Character, characters):
        pass
    def on_move(self, character : Character):
        pass
    
class ConsoleEventReceiver(EventReceiver):
    COLOR = '\033[0m'
    COLOR2 = '\033[92m'    
    def on_attack(self, attacker : Character, targets):
        print(ConsoleEventReceiver.COLOR, end = ' ')
        print(attacker.sheet.name + ' attacks ' + targets[0].sheet.name, end = ' ')
    def on_damage(self, character : Character, damage):
        print('and deals ' + str(damage) + ' damage. ' + character.sheet.name + ' has ' + str(character.stats.hp) + ' HP now.')  
    def on_block(self, character : Character):
        print('who blocks')
    def on_cast_spell(self, attacker : Character, targets, spell_name):
        print(ConsoleEventReceiver.COLOR, end = ' ')
        if len(targets) == 1:
            print(attacker.sheet.name + ' casts ' + spell_name + ' against ' + targets[0].sheet.name, end = ' ')
        else:
            print(attacker.sheet.name + ' casts ' + spell_name, end = ' ')
    def on_spell_effect(self, targets, effect):
        if effect == 'raise':
            print('and creates ' + str(len(targets)) + ' ' + targets[0].sheet.name + 's')
    def on_magic_block(self, character : Character):
        print(ConsoleEventReceiver.COLOR, end = ' ')
        print('who effectively resists magic')
    def on_wait(self, character : Character):
        print(ConsoleEventReceiver.COLOR, end = ' ')
        print(character.sheet.name + ' is waiting.')
    def on_death(self, character : Character):
        print(ConsoleEventReceiver.COLOR, end = ' ')
        print(character.sheet.name + ' died')
    def on_new_turn(self, current_character : Character, characters):
        if current_character.controlled == False:
            return
        print(ConsoleEventReceiver.COLOR2)
        for chr in characters:
            print('\t' + chr.sheet.name + '\t\t' + '[' + str(chr.stats.hp) + '/' + str(chr.sheet.hp) + ']')
    def on_move(self, character : Character):
        print(ConsoleEventReceiver.COLOR, end = ' ')
        if character.line == Character.FRONT_LINE:
            line = 'front line'
        else:
            line = "back line"
        print(character.sheet.name + ' moved to ' + line)
 
class Fight:
    def __init__(self, characters, library : Library, selectorA : ActionSelector, selectorB : ActionSelector, logger):
        self.characters = characters
        self.library = library
        self.selector = [selectorA, selectorB]
        self.current = 0
        self.logger = logger
        self.characters.sort(key=lambda x: x.sheet.initiative, reverse=True)
        self.helper = ActionHelper(self.library, self.characters)
                
    def attack_target(self, attacker, target):
        atk_factor = attacker.sheet.attack / target.sheet.defence
        atk = atk_factor * random.randint(attacker.sheet.breakage[0], attacker.sheet.breakage[1])        
        target.stats.dp -= atk        
        if target.stats.dp <= 0:
            dmg_factor = attacker.sheet.strength / target.sheet.endurance
            dmg = dmg_factor * random.randint(attacker.sheet.dmg[0], attacker.sheet.dmg[1])
            target.stats.hp -= dmg
            self.logger.on_damage(target, dmg)
            if target.stats.hp < 0:
                self.logger.on_death(target)
            else:
                target.stats.dp = target.sheet.dp
        else:
            self.logger.on_block(target)
            
    def attack(self, attacker, targets):
        if len(targets) == 0:
            return
        self.logger.on_attack(attacker, targets)
        for target in targets:
            self.attack_target(attacker, target)
            
    def magic_on_target(self, attacker, target, spell):
        if spell.effect == 'raise':
            sheet = self.library.sheets['Skeleton']
            number = int(attacker.sheet.power / 5)
            if number > 0:
                skeletons = [Character(sheet, False, attacker.faction) for i in range(number)]
                for skeleton in skeletons:
                    self.characters.append(skeleton)
                self.logger.on_spell_effect(skeletons, spell.effect)
            return
        atk_factor = attacker.sheet.power / target.sheet.will
        atk = atk_factor * random.randint(spell.impact[0], spell.impact[1])
        target.stats.rp -= atk        
        if target.stats.rp <= 0:
            dmg_factor = attacker.sheet.power / target.sheet.will
            dmg = dmg_factor * random.randint(spell.dmg[0], spell.dmg[1])
            target.stats.hp -= dmg
            self.logger.on_damage(target, dmg)
            if target.stats.hp < 0:
                self.logger.on_death(target)
            else:
                target.stats.rp = target.sheet.rp
        else:
            self.logger.on_magic_block(target)
            
    def magic(self, attacker, targets, spell_name):
        if spell_name in self.library.spells:
            spell = self.library.spells[spell_name]
        else:
            return
        if attacker.stats.mp < spell.mp_cost:
            return
        attacker.stats.mp -= spell.mp_cost
        self.logger.on_cast_spell(attacker, targets, spell.name)
        if len(targets) > 0:
            for target in targets:
                self.magic_on_target(attacker, target, spell)
        else:
            self.magic_on_target(attacker, [], spell)

    def move(self, actor : Character):
        if actor.line == Character.FRONT_LINE:
            actor.line = Character.BACK_LINE
        else:
            actor.line = Character.FRONT_LINE
        self.logger.on_move(actor)

    def move_all_to_frontline(self, faction : int):
        for chr in self.characters:
            if chr.faction == faction:
                chr.line = Character.FRONT_LINE
                
    def processAction(self, action : Action):
        if action.type == Action.ACTION_WAIT:
            self.logger.on_wait(action.actor)
        elif action.type == Action.ACTION_ATTACK:
            self.attack(action.actor, action.targets)
        elif action.type == Action.ACTION_MAGIC:
            self.magic(action.actor, action.targets, action.spell_name)
        elif action.type == Action.ACTION_MOVE:
            self.move(action.actor)
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
            for i in range(current_character.sheet.attack_number):
                action = selector.select(current_character, self.characters, self.helper)
                self.processAction(action)
                if action.type == Action.ACTION_WAIT:
                    break
                if self.helper.is_frontline_empty(Character.BLUE_FACTION):
                    self.move_all_to_frontline(Character.BLUE_FACTION)
                if self.helper.is_frontline_empty(Character.RED_FACTION):
                    self.move_all_to_frontline(Character.RED_FACTION)
        self.current += 1
        if self.current >= len(self.characters):
            self.current = 0
    
    def ended(self):
        alive = [0, 0]
        for chr in self.characters:
            if chr.is_alive():
                if chr.faction == Character.BLUE_FACTION:
                    alive[0] += 1
                else:
                    alive[1] += 1
        if alive[0] == 0 or alive[1] == 0:
            return True
        return False
            
            
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

library = Library()
ai = AISelector()
console_selector = ConsoleSelector()
logger = ConsoleEventReceiver()

fight = Fight([character, character2, character3, character4], library, console_selector, ai, logger)

while fight.ended() == False:
    fight.turn()