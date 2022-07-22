from dataclasses import dataclass
from typing import List, NoReturn

from interpreter.ast import (
    AST,
    Assign,
    BinOp,
    Compound,
    NoOp,
    Num,
    UnaryOp,
    Var,
)
from interpreter.lexer import Lexer
from interpreter.token import Token, TokenType


@dataclass
class InterpreterParserError(Exception):
    error_msg: str


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token: Token = self.lexer.get_next_token()

    def _error(self) -> NoReturn:
        raise InterpreterParserError("Invalid syntax")

    def eat(self, token_type: TokenType) -> None:
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type_ == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self._error()

    def factor(self) -> AST:
        """factor : INTEGER | LPAREN expr RPAREN"""
        token = self.current_token
        if token.type_ == TokenType.PLUS:
            self.eat(TokenType.PLUS)
            unary_node_plus = UnaryOp(token, self.factor())
            return unary_node_plus
        elif token.type_ == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            unary_node_minus = UnaryOp(token, self.factor())
            return unary_node_minus
        if token.type_ == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token)
        elif token.type_ == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node_expr: AST = self.expr()
            self.eat(TokenType.RPAREN)
            return node_expr
        else:
            node_variable = self.variable()
            return node_variable

    def term(self) -> AST:
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()

        while self.current_token.type_ in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            if token.type_ == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token.type_ == TokenType.DIV:
                self.eat(TokenType.DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self) -> AST:
        """
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER | LPAREN expr RPAREN
        """
        node = self.term()

        while self.current_token.type_ in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type_ == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type_ == TokenType.MINUS:
                self.eat(TokenType.MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def program(self):
        """program : compound_statement DOT"""
        node = self.compound_statement()
        self.eat(TokenType.DOT)
        return node

    def statement(self):
        """
        statement : compound_statement
                  | assignment_statement
                  | empty
        """
        if self.current_token.type_ == TokenType.BEGIN:
            node = self.compound_statement()
        elif self.current_token.type_ == TokenType.ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node

    def statement_list(self) -> List[AST]:
        """
        statement_list : statement
                       | statement SEMI statement_list
        """
        node = self.statement()

        results = [node]

        while self.current_token.type_ == TokenType.SEMI:
            self.eat(TokenType.SEMI)
            results.append(self.statement())

        if self.current_token.type_ == TokenType.ID:
            self._error()

        return results

    def assignment_statement(self) -> AST:
        """
        assignment_statement : variable ASSIGN expr
        """
        left = self.variable()
        token = self.current_token
        self.eat(TokenType.ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def variable(self) -> AST:
        """
        variable : ID
        """
        node = Var(self.current_token)
        self.eat(TokenType.ID)
        return node

    def empty(self) -> AST:
        """An empty production"""
        return NoOp()

    def compound_statement(self) -> AST:
        """
        compound_statement: BEGIN statement_list END
        """
        self.eat(TokenType.BEGIN)
        nodes = self.statement_list()
        self.eat(TokenType.END)

        root = Compound()
        for node in nodes:
            root.children.append(node)
        return root

    def parse(self) -> AST:
        node = self.program()
        if self.current_token.type_ != TokenType.EOF:
            self._error()
        return node
