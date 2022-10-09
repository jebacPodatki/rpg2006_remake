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