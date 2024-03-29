class Environment:

    def __init__(self, record=None, parent=None):
        if record is None:
            record = {}
        self.record = record
        self.parent = parent

    def define(self, name, value):
        self.record[name] = value
        return value

    def assign(self, name, value):
        self.resolve(name).record[name] = value
        return value

    def lookup(self, expr):
        return self.resolve(expr).record[expr]

    def resolve(self, name):
        if name in self.record:
            return self
        if self.parent is None:
            raise ValueError(f"Variable {name} is not defined.")
        return self.parent.resolve(name)
