import pygame
from gui.config import *
from gui.drawable import *
from gui.input_interface import *

class BaseNode:
    def __init__(self, name : str, parent, enabled = True):
        self.name = name
        self.__parent = parent
        self.__children = []
        self.enabled = enabled
    def get_children(self):
        return self.__children
    def get_parent(self):
        return self.__parent
    def is_callable(self):
        return False
    def is_backnode(self):
        return False

class LeafNode(BaseNode):
    def __init__(self, name : str, parent, functor = None, enabled = True):
        super(LeafNode, self).__init__(name, parent, enabled)
        self.__functor = functor
    def __call__(self):
        if self.__functor != None:
            self.__functor()
    def is_callable(self):
        return True

class BackNode(BaseNode):
    def __init__(self, parent):
        super(BackNode, self).__init__('<- Back', parent)
    def is_backnode(self):
        return True

class Node(BaseNode):
    def __init__(self, name : str, parent, enabled = True):
        super(Node, self).__init__(name, parent, enabled)
    def add_leaf_child(self, name : str, functor, enabled = True):
        child = LeafNode(name, self, functor, enabled)
        self.get_children().append(child)
        return child
    def add_returning_child(self):
        child = BackNode(self)
        self.get_children().append(child)
        return child
    def add_child(self, name : str, enabled = True):
        child = Node(name, self, enabled)
        self.get_children().append(child)
        return child

class RootNode(Node):
    def __init__(self, name : str):
        super(RootNode, self).__init__(name, None)

class SwitchingMenu(DrawableObjectInterface, InputInterface):
    def __init__(self, config : Config):
        self.config = config
        self.font = pygame.font.SysFont(config.menu_font, config.menu_font_size)
        self.color_selected = (config.menu_font_color_selected[0],
                               config.menu_font_color_selected[1],
                               config.menu_font_color_selected[2])
        self.color_unselected = (config.menu_font_color_unselected[0],
                                 config.menu_font_color_unselected[1],
                                 config.menu_font_color_unselected[2])
        self.color_disabled = (config.menu_font_color_disabled[0],
                               config.menu_font_color_disabled[1],
                               config.menu_font_color_disabled[2])
        self.color_root = (config.menu_font_color_root[0],
                            config.menu_font_color_root[1],
                            config.menu_font_color_root[2])
        self.content = []
        self.selected_index = 0
        self.root_node = RootNode('')
        self.root_line = ''
        self.current_node = None

    def __set_next_available_index(self, step : int):
        index = (self.selected_index + step) % len(self.current_node.get_children())
        while self.current_node.get_children()[index].enabled == False:
            index += step
            index = index % len(self.current_node.get_children())
            if index == self.selected_index:
                self.selected_index = -1
                return
        self.selected_index = index

    def __reset(self, lines):
        self.content = []
        for (line, enabled) in lines:
            if enabled:
                selected = self.font.render(line, 1, self.color_selected)
                unselected = self.font.render(line, 1, self.color_unselected)
                self.content.append([unselected, selected])
            else:
                disabled = self.font.render(line, 1, self.color_disabled)
                self.content.append([disabled])

    def __set_current_node(self, current_node):
        self.current_node = current_node
        self.selected_index = -1
        if current_node == None:
            self.content = []
            return
        names = []
        for node in current_node.get_children():
            names.append((node.name, node.enabled))
        self.__reset(names)
        self.root_line = self.font.render(self.current_node.name, 1, self.color_root)
        self.__set_next_available_index(1)

    def set_root_node(self, root_node : RootNode):
        self.root_node = root_node
        self.__set_current_node(self.root_node)

    def draw(self, screen : pygame.Surface):
        if self.root_node == None:
            return
        screen.blit(self.root_line, (self.config.menu_pos[0], self.config.menu_pos[1]))
        delta_y = self.config.menu_interline_size
        for i in range(len(self.content)):
            if i == self.selected_index:
                line = self.content[i][1]
            else:
                line = self.content[i][0]
            screen.blit(line, (self.config.menu_pos[0] + self.config.menu_indent, self.config.menu_pos[1] + delta_y))
            delta_y += self.config.menu_interline_size

    def on_up(self):
        if len(self.content) == 0:
            return
        self.__set_next_available_index(-1)

    def on_down(self):
        if len(self.content) == 0:
            return
        self.__set_next_available_index(1)

    def on_select(self):
        if len(self.content) == 0:
            return
        if self.current_node == None:
            return
        selected_node = self.current_node.get_children()[self.selected_index]
        if selected_node.is_backnode():
            self.__set_current_node(self.current_node.get_parent())
        elif selected_node.is_callable() == True:
            selected_node()
        else:
            self.__set_current_node(selected_node)