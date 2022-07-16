from dataclasses import dataclass
from typing import Callable, NoReturn


from interpreter.parser import Parser
from interpreter.ast import Num, BinOp
from interpreter.token import TokenType


@dataclass
class InterpreterError(Exception):
    error_msg: str


class NodeVisitor(object):
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor: Callable = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
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
        if node.op.type_ == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type_ == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type_ == TokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type_ == TokenType.DIV:
            return self.visit(node.left) / self.visit(node.right)
        self._error()

    def visit_Num(self, node: Num) -> int:
        return node.value

    def run(self) -> int:
        return self.visit(self.parser.expr())
