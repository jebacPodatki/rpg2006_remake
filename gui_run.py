import pygame
from gui.config import *
from gui.action_selector import *
from gui.event_receiver import *
from gui.widgets.battlearena import BattleArena
from gui.widgets.console import *
from gui.widgets.switching_menu import *
from gui.widgets.character_hud import *
from gui.widgets.character_portrait import *
from gui.widgets.character_portrait import *

from system.core.character import *
from system.core.library import Library
from system.core.fight import Fight
from system.ai.ai import *

class Attributes:
    barImg = 'pngs/bar.png'

class Drawable:
    def draw(screen):
        pass

class CharacterBars(Drawable):
    def __init__(self, atts : Attributes, x, y):
        self.x = x
        self.y = y
        self.red = 1.0
        self.blue = 1.0
        self.green = 1.0
        self.delta = 11
        self.img = pygame.image.load(atts.barImg)
        self.H = self.img.get_width()
        self.W = self.img.get_height()
    def update(self, red, green, blue):
        self.red = red
        self.blue = blue
        self.green = green
    def draw(self, screen):
        pygame.draw.rect(screen,(220, 0, 50),(self.x,self.y,self.red*self.H,self.W))
        pygame.draw.rect(screen,(50, 210, 50),(self.x,self.y+self.delta,self.green*self.H,self.W))
        pygame.draw.rect(screen,(50, 50, 200),(self.x,self.y+2*self.delta,self.blue*self.H,self.W))
        screen.blit(self.img, (self.x, self.y))
        screen.blit(self.img, (self.x, self.y + self.delta))
        screen.blit(self.img, (self.x, self.y + 2*self.delta))

def main():
    pygame.init()
    pygame.display.set_caption("RPG2006 Remake")

    config = Config('json/config.json')

    mode = (config.window_size[0], config.window_size[1])
    screen = pygame.display.set_mode(mode)
    running = True

    #
    attrs = Attributes()
    bar = CharacterBars(attrs, 550, 100)
    bar.update(0.8, 0.5, 0.2)

    #
    img1 = pygame.image.load('pngs/human.png')
    img2 = pygame.image.load('pngs/elf.png')
    img3 = pygame.image.load('pngs/dwarf.png')
    img4 = pygame.image.load('pngs/half-demon.png')
    img5 = pygame.image.load('pngs/necro.png')
    img6 = pygame.image.load('pngs/skeleton.png')
    X = 200
    Y = 100

    #
    console = Console(config)

    root_node = RootNode('L')
    sub_node = root_node.add_child('Attack')
    sub_node.add_child('Barsel')
    sub_node.add_child('Abzare')
    sub_node = root_node.add_child('Magic')
    subsub_node = sub_node.add_child('Magic bolt')
    subsub_node.add_child('Barsel')
    subsub_node.add_child('Abzare')
    sub_node.add_child('Fireball')
    root_node.add_child('Move')

    menu = SwitchingMenu(config)
    menu.set_root_node(root_node)

    library = Library('json/spells.json', 'json/sheets.json')
    character = Character(library.sheets['Barsel'], True, Character.RED_FACTION)
    character2 = Character(library.sheets['Abzare'], False, Character.BLUE_FACTION)
    character3 = Character(library.sheets['Cersil'], True, Character.RED_FACTION)
    character3.line = Character.BACK_LINE
    character4 = Character(library.sheets['Dalian'], False, Character.BLUE_FACTION)
    character4.line = Character.BACK_LINE

    ai = AIActionSelector()
    selector = InteractiveActionSelector(menu)
    logger = SystemEventReceiver(console)
    characters = [character, character2, character3, character4]
    fight = Fight(characters, library, selector, ai, logger)

    #
    hud_1 = CharacterHUD(config, character, (550, 300))
    hud_2 = CharacterHUD(config, character3, (550, 370))

    #
    portrait = CharacterPortrait(config, character, (550, 480))

    #
    arena = BattleArena(config, characters)

    objects = [console, menu, hud_1, hud_2, portrait, arena]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            menu.on_event(event)

        screen.fill((0, 0, 0))
        bar.draw(screen)

        for object in objects:
            object.draw(screen)

        if fight.ended() == False:
            fight.process()

        for object in objects:
            object.update()

        pygame.display.update()


if __name__=="__main__":
    main()