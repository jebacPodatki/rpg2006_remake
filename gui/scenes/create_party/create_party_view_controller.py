from gui.scenes.create_party.create_party_view import *
from gui.interfaces.scene_controller_interface import *
from gui.widgets.controllers.switching_menu_controller import *
from gui.input.input_event import *

from gameplay.party import *

class CreatePartyViewController(SceneControllerInterface):
    def __init__(self, view : CreatePartyView):
        self.view = view
        self.menu_controller = SwitchingMenuController(view.menu)
        self.create_character_functors = []
        self.delete_character_functors = []
        self.start_functor = None
        self.exit_functor = None

    def on_event(self, event : InputEvent):
        self.menu_controller.on_event(event)

    def update_menu_partially(self, party : Party):
        party_size = party.size()
        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
        line = ['frontline', 'backline']
        root_node = RootNode('')
        for i in range(len(positions)):
            x = positions[i][0]
            y = positions[i][1]
            if party.characters[x][y] == None:
                active = party_size < Party.CHARACTER_LIMIT
                root_node.add_leaf_child('Create character (empty ' + line[x] +' slot)', self.create_character_functors[i], active)
            else:
                character_name = party.characters[x][y].name
                root_node.add_leaf_child('Delete character (' + character_name + ')', self.delete_character_functors[i])
        root_node.add_leaf_child('Start journey', self.start_functor, party_size > 0)
        root_node.add_leaf_child('Exit', self.exit_functor)
        self.view.menu.set_root_node(root_node, True)

    def update_menu(self, party : Party, create_character_functors, delete_character_functors, start_functor, exit_functor):
        self.create_character_functors = create_character_functors
        self.delete_character_functors = delete_character_functors
        self.start_functor = start_functor
        self.exit_functor = exit_functor
        self.update_menu_partially(party)

    def update_sheets(self, party : Party):
        n = 0
        for character_line in party.characters:
            for character in character_line:
                self.view.character_sheets[n].set_character(character)
                n += 1