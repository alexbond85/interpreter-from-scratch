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

    def __init__(self,
                 global_env: Environment = None):
        if global_env is None:
            global_env = Environment(record={
                     "null": None,
                     "true": True,
                     "false": False,
                     "VERSION": '0.1'
                 })
        self.global_env = global_env

    def eval(self, expr, environment: Environment = None):
        if environment is None:
            environment = self.global_env
        if is_number(expr):
            return expr
        if is_string(expr):
            return expr[1:-1]
        if expr[0] == '+':
            return self.eval(expr[1], environment) + self.eval(expr[2], environment)
        if expr[0] == '*':
            return self.eval(expr[1], environment) * self.eval(expr[2], environment)
        if expr[0] == 'var':
            _, name, value = expr
            return environment.define(name, self.eval(value, environment))
        if expr[0] == 'begin':
            block_env = Environment(None, parent=environment)
            return self._eval_block(expr, block_env)
        if expr[0] == 'set':
            _, name, value = expr
            return environment.assign(name, value)
        if is_variable_name(expr):
            return environment.lookup(expr)
        raise TypeError(f"Not implemented. Received expression: {expr}")

    def _eval_block(self, block, env):
        _tag, expressions = block[0], block[1:]
        result = None
        for expr in expressions:
            result = self.eval(expr, env)
        return result
