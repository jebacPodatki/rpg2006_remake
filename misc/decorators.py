import json

class fromJson(object):
    def __call__(self, cls):
        class Wrapped(cls):
            def __init__(self, filename, *args):
                f = open(filename, "r")
                source = json.load(f)
                super(Wrapped, self).__init__(source, *args)
        return Wrapped

class deserialize(object):
    def get_properties(self, cls):
        return [i for i in cls.__dict__.keys() if i[:1] != '_']
    def __call__(self, cls):
        properties = self.get_properties(cls)
        class Wrapped(cls):
            def __init__(self, source, *args):
                super(Wrapped, self).__init__(*args)
                for prop in properties:
                    self.__dict__[prop] = source[prop]
        return Wrapped
