import pygame

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
        
class CharacterStats:
    dmgMin = 10
    dmgMax = 20
    hp = 100
    
class Character:
    def __init__(stats : CharacterStats, controlled : bool, faction):
        self.baseStats = copy.deepcopy(stats)
        self.stats = copy.deepcopy(stats)
        self.controlled = controlled
        self.faction = faction
    def reset():
        self.stats = copy.deepcopy(self.baseStats)


ACTION_NONE = 0
ACTION_ATTACK = 1
ACTION_MAGIC = 2
ACTION_WAIT = 3
        
class Action:
    def __init(type, target : Character, skill):
        self.type = type
        self.target = target
        self.skill = skill
        
class ActionSelector:
    def select(character : Character, characterList):
        return Action(ACTION_NONE, None, 0)
    
class AISelector(ActionSelector):
    def select(character : Character, characterList):
        for chr in characterList:
            if chr.faction != character.faction:
                return Action(ACTION_ATTACK, chr, 0)
        

def main():    
    pygame.init()    
    pygame.display.set_caption("RPG2006 Remake")
     
    screen = pygame.display.set_mode((800,600))     
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
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False                     
            
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
        pygame.display.update()
     

if __name__=="__main__":
    main()