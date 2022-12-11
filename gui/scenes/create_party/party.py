class Party:
    CHARACTER_IN_LINE_LIMIT = 2
    CHARACTER_LIMIT = 3
    def __init__(self):
        self.characters = [[None, None], [None, None]]
    def size(self):
        n = 0
        for characters in self.characters:
            for character in characters:
                if character != None:
                    n += 1
        return n