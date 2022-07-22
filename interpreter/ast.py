from dataclasses import dataclass
from typing import Callable, List

from interpreter.token import Token


#     program : compound_statement DOT
#
#     compound_statement : BEGIN statement_list END
#
#     statement_list : statement
#                    | statement SEMI statement_list
#
#     statement : compound_statement
#               | assignment_statement
#               | empty
#
#     assignment_statement : variable ASSIGN expr
#
#     empty :
#
#     expr: term ((PLUS | MINUS) term)*
#
#     term: factor ((MUL | DIV) factor)*
#
#     factor : PLUS factor
#            | MINUS factor
#            | INTEGER
#            | LPAREN expr RPAREN
#            | variable
#
#     variable: ID


class AST:
    pass


class NoOp(AST):
    pass


class Compound(AST):
    """Represents a 'BEGIN ... END' block"""

    def __init__(self):
        self.children: List[AST] = []


class Assign(AST):
    def __init__(self, left: AST, op: Token, right: AST):
        self.left = left
        self.token = op
        self.op = op
        self.right = right


class Var(AST):
    """The Var node is constructed out of ID token."""

    def __init__(self, token: Token):
        self.token = token
        self.value = token.value


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


class UnaryOp(AST):
    def __init__(self, op: Token, expr: AST):
        self.token = op
        self.op = op
        self.expr = expr


class NodeVisitor:
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor: Callable = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        msg = f"No visit_{type(node).__name__} method"
        raise InterpreterVisitorException(msg)
