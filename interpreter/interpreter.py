from dataclasses import dataclass
from typing import Callable, NoReturn


from interpreter.parser import Parser
from interpreter.ast import Num, BinOp, UnaryOp
from interpreter.token import TokenType


@dataclass
class InterpreterError(Exception):
    error_msg: str


class NodeVisitor(object):
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor: Callable = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node) -> NoReturn:
        error_msg = f"No visit_{type(node).__name__} method"
        raise InterpreterError(error_msg)


class Interpreter(NodeVisitor):
    """
    Processes and executes the source program without
    translating it into machine language first.
    """

    def __init__(self, parser: Parser):
        self.parser = parser

    def _error(self) -> NoReturn:
        raise InterpreterError("Invalid syntax")

    def visit_BinOp(self, node: BinOp) -> int:
        ops_map = {
            TokenType.PLUS: lambda x, y: x + y,
            TokenType.MINUS: lambda x, y: x - y,
            TokenType.MUL: lambda x, y: x * y,
            TokenType.DIV: lambda x, y: x // y,
        }
        if node.op.type_ in ops_map:
            value_left = self.visit(node.left)
            value_right = self.visit(node.right)
            return ops_map[node.op.type_](value_left, value_right)
        self._error()

    def visit_Num(self, node: Num) -> int:
        return node.value

    def visit_UnaryOp(self, node: UnaryOp) -> int:
        op = node.op.type_
        if op == TokenType.PLUS:
            return +self.visit(node.expr)
        elif op == TokenType.MINUS:
            return -self.visit(node.expr)

    def run(self) -> int:
        return self.visit(self.parser.expr())
