from dataclasses import dataclass
from typing import NoReturn

from interpreter.ast import AST, BinOp, Num
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
        if token.type_ == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token)
        elif token.type_ == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        self._error()

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

    def parse(self):
        self.expr()
