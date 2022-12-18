from system.core.action.action import *
from system.core.action.action_selector import *
from system.core.action.helper import *
from system.core.character import *
from gui.widgets.switching_menu import *

class InteractiveActionSelectorInterface(ActionSelectorInterface):
    def select_action(self, action : Action):
        pass

class ActionInvoker:
    def __init__(self, selector : InteractiveActionSelectorInterface, action : Action):
        self.selector = selector
        self.action = action

    def __call__(self):
        self.selector.select_action(self.action)

class InteractiveActionSelector(InteractiveActionSelectorInterface):
    def __init__(self, menu : SwitchingMenu):
        self.menu = menu
        self.selected_action = None
        self.menu_filled = False

    def select_action(self, action : Action):
        self.menu.set_root_node(None)
        self.selected_action = action
        self.menu_filled = False

    def target_group_to_string(self, target_group):
        if len(target_group) == 1:
            return target_group[0].sheet.name
        string = ''
        for target in target_group:
            string += target.sheet.name
            string += ', '
        return string[:len(string)-2]

    def populate_with_target_nodes(self, node : Node, character : Character, action_type, spell_name, helper):
        target_groups = helper.get_possible_targets(character, spell_name)
        if len(target_groups) > 0:
            for target_group in target_groups:
                node_name = self.target_group_to_string(target_group)
                node.add_leaf_child(node_name, ActionInvoker(self, Action(action_type, character, target_group, spell_name)))
        elif action_type == Action.ACTION_MAGIC:
            node.add_leaf_child('Cast without target', ActionInvoker(self, Action(action_type, character, [], spell_name)))
        node.add_returning_child()

    def populate_with_spell_nodes(self, node : Node, character : Character, helper):
        for spell in character.sheet.spells:
            if helper.can_use(character, spell):
                subnode = node.add_child(spell)
                self.populate_with_target_nodes(subnode, character, Action.ACTION_MAGIC, spell, helper)
        node.add_returning_child()

    def select(self, character : Character, helper):
        if self.selected_action != None:
            action = self.selected_action
            self.selected_action = None
            return action
        if self.menu_filled == False:
            root_node = RootNode(character.sheet.name)
            attack_node = root_node.add_child('Attack')
            self.populate_with_target_nodes(attack_node, character, Action.ACTION_ATTACK, '', helper)
            magic_enabled = len(character.sheet.spells) > 0
            magic_node = root_node.add_child('Magic', magic_enabled)
            self.populate_with_spell_nodes(magic_node, character, helper)
            move_enabled = helper.can_move(character)
            root_node.add_leaf_child('Move', ActionInvoker(self, Action(Action.ACTION_MOVE, character, [], '')), move_enabled)
            root_node.add_leaf_child('Wait', ActionInvoker(self, Action(Action.ACTION_WAIT, character, [], '')))
            self.menu.set_root_node(root_node)
            self.menu_filled = True
        return Action(Action.ACTION_NONE, None, [], '')