import pygame
from gui.config import *
from gui.action_selector import *
from gui.event_receiver import *
from gui.widgets.console import *
from gui.widgets.switching_menu import *

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
    bar = CharacterBars(attrs, 200, 530)
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
    console = GUIConsole(config)
    kkk = 0
    console.print_on('console test' + str(kkk))

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
    logger = GUIEventReceiver()
    fight = Fight([character, character2, character3, character4], library, selector, ai, logger)

    objects = [console, menu]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    console.print_on('ABCDEFGHIJKLMNOPSRTWIZDUERHUU' + str(kkk))
                    kkk += 1
            menu.on_event(event)

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (20, 20, 20), (X - 10, Y - 10, 330, 400), 2)
        bar.draw(screen)
        screen.blit(img1, (X, Y + 300))
        screen.blit(img2, (X + 80, Y + 300))
        screen.blit(img3, (X + 160, Y + 300))
        screen.blit(img4, (X + 240, Y + 300))
        screen.blit(img5, (X + 120, Y))
        screen.blit(img6, (X, Y + 100))
        screen.blit(img6, (X + 80, Y + 100))
        screen.blit(img6, (X + 160, Y + 100))
        screen.blit(img6, (X + 240, Y + 100))

        for object in objects:
            object.draw(screen)

        if fight.ended() == False:
            fight.process()

        pygame.display.update()


if __name__=="__main__":
    main()