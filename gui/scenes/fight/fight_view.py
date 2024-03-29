from gui.interfaces.abstract_view import *
from gui.scenes.fight.scene_properties import *
from gui.widgets.switching_menu import *
from gui.widgets.console import *
from gui.widgets.battlearena import *
from gui.widgets.battle_hud import *


class FightView(AbstractView):
    def __init__(self, properties_path : str, characters):
        super().__init__()
        properties = SceneProperties(properties_path)
        self.menu = SwitchingMenu(properties)
        self.add_object(self.menu)
        self.console = Console(properties)
        self.add_object(self.console)
        self.arena = BattleArena(properties, characters)
        self.add_object(self.arena)
        self.hud = BattleHUD(properties, characters)
        self.add_object(self.hud)