class Environment:

    def __init__(self, record=None):
        if record is None:
            self.record = {}
        else:
            self.record = record

    def define(self, name, value):
        self.record[name] = value
        return value

    def lookup(self, expr):
        try:
            return self.record[expr]
        except KeyError:
            raise ValueError(f"Variable {expr} is not defined.")