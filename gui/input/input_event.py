class InputEvent:
    NONE = 0
    DOWN_PRESSED = 1
    UP_PRESSED = 2
    SELECT_PRESSED = 3
    def __init__(self, event : int):
        self.event = event