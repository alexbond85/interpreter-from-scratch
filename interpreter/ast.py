from dataclasses import dataclass

from interpreter.token import Token


class AST:
    pass


@dataclass
class InterpreterVisitorException(Exception):
    error_msg: str


class BinOp(AST):
    def __init__(self, left: AST, op: Token, right: AST):
        self.left = left
        self.token: Token = op
        self.op: Token = op
        self.right = right


@dataclass
class Num(AST):
    token: Token

    def __post_init__(self):
        self.value = self.token.value


class NodeVisitor:
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        msg = f"No visit_{type(node).__name__} method"
        raise InterpreterVisitorException(msg)
