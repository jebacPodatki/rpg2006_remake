class InputEvent:
    NONE = 0
    DOWN = 1
    UP = 2
    SELECT = 3
    def __init__(self, event : int):
        self.event = event