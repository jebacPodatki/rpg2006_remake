import json

class fromJson(object):
    def __call__(self, cls):
        class Wrapped(cls):
            def __init__(self, filename, *args):
                f = open(filename, "r")
                source = json.load(f)
                super().__init__(source, *args)
        return Wrapped

class deserialize(object):
    def __call__(self, cls):
        class Wrapped(cls):
            def __init__(self, source = None, *args):
                super().__init__(*args)
                if source == None:
                    return
                properties = [i for i in super().__dict__.keys() if i[:1] != '_']
                for prop in properties:
                    self.__dict__[prop] = source[prop]
        return Wrapped
