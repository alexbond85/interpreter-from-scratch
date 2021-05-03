import numbers
from interpreter.environment import Environment
import re


def is_number(expr) -> bool:
    return isinstance(expr, numbers.Number)


def is_string(expr) -> bool:
    return (isinstance(expr, str)
            and expr.startswith("\"")
            and expr.endswith("\"")
            )


def is_variable_name(expr) -> bool:
    if isinstance(expr, str):
        matched_substring = re.match(r"^[a-z][a-zA-Z0-9_]*", expr).group()
        return len(expr) == len(matched_substring)
    return False


class Eva:

    def __init__(self, global_env: Environment = Environment()):
        self.global_env = global_env

    def eval(self, expr, environment: Environment = None):
        if environment is None:
            environment = self.global_env
        if is_number(expr):
            return expr
        elif is_string(expr):
            return expr[1:-1]
        elif expr[0] == '+':
            return self.eval(expr[1]) + self.eval(expr[2])
        elif expr[0] == '*':
            return self.eval(expr[1]) * self.eval(expr[2])
        elif expr[0] == 'var':
            _, name, value = expr
            return environment.define(name, value)
        elif is_variable_name(expr):
            return environment.lookup(expr)
        else:
            raise TypeError(f"Not implemented. Received expression: {expr}")
