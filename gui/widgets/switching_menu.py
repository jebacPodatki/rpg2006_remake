import pygame
from gui.config import *
from gui.drawable import *

class BaseNode:
    def __init__(self, name : str, parent = None):
        self.name = name
        self.__parent = parent
        self.__children = []
    def get_children(self):
        return self.__children
    def get_parent(self):
        return self.__parent
    def is_callable(self):
        return False

class LeafNode(BaseNode):
    def __init__(self, name : str, functor = None, parent = None):
        super(LeafNode, self).__init__(name, parent)
        self.__functor = functor
    def __call__(self):
        if self.__functor != None:
            self.__functor()
    def is_callable(self):
        return True

class Node(BaseNode):
    def __init__(self, name : str, parent = None):
        super(Node, self).__init__(name, parent)
    def add_leaf_child(self, name : str, functor):
        child = LeafNode(name, functor, self)
        self.get_children().append(child)
        return child
    def add_child(self, name : str):
        child = Node(name, self)
        self.get_children().append(child)
        return child

class RootNode(Node):
    def __init__(self, name : str):
        super(RootNode, self).__init__(name, None)

class SwitchingMenu(DrawableObjectInterface):
    def __init__(self, config : Config):
        self.config = config
        self.font = pygame.font.SysFont(config.menu_font, config.menu_font_size)
        self.color_selected = (config.menu_font_color_selected[0],
                               config.menu_font_color_selected[1],
                               config.menu_font_color_selected[2])
        self.color_unselected = (config.menu_font_color_unselected[0],
                                 config.menu_font_color_unselected[1],
                                 config.menu_font_color_unselected[2])
        self.content = []
        self.selected_index = 0
        self.root_node = RootNode('')
        self.current_node = None

    def __reset(self, lines):
        self.content = []
        for line in lines:
            selected = self.font.render(line, 1, self.color_selected)
            unselected = self.font.render(line, 1, self.color_unselected)
            self.content.append([unselected, selected])

    def __set_current_node(self, current_node):
        self.current_node = current_node
        self.selected_index = 0
        if current_node == None:
            self.content = []
            return
        names = []
        for node in current_node.get_children():
            names.append(node.name)
        if current_node.get_parent() != None:
            names.append('<- Back')
        self.__reset(names)

    def set_root_node(self, root_node : RootNode):
        self.root_node = root_node
        self.__set_current_node(self.root_node)

    def draw(self, screen : pygame.Surface):
        delta_y = 0
        for i in range(len(self.content)):
            if i == self.selected_index:
                line = self.content[i][1]
            else:
                line = self.content[i][0]
            screen.blit(line, (self.config.menu_pos[0], self.config.menu_pos[1] + delta_y))
            delta_y += self.config.menu_interline_size

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if len(self.content) == 0:
                return
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.selected_index = (self.selected_index - 1) % len(self.content)
            if keys[pygame.K_DOWN] :
                self.selected_index = (self.selected_index + 1) % len(self.content)
            if keys[pygame.K_RETURN] :
                if self.current_node == None:
                    return
                if self.selected_index == len(self.content) - 1:
                    self.__set_current_node(self.current_node.get_parent())
                else:
                    selected_node = self.current_node.get_children()[self.selected_index]
                    if selected_node.is_callable() == True:
                        selected_node()
                    else:
                        self.__set_current_node(selected_node)