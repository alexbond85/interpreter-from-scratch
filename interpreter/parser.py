from dataclasses import dataclass
from typing import NoReturn

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

    def factor(self) -> None:
        """Parse integer.
        factor : INTEGER
        """
        self.eat(TokenType.INTEGER)

    def expr(self):
        """Arithmetic expression parser.
        Grammar:
        expr   : factor ((MUL | DIV) factor)*
        factor : INTEGER
        """
        self.factor()

        while self.current_token.type_ in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            if token.type_ == TokenType.MUL:
                self.eat(TokenType.MUL)
                self.factor()
            elif token.type_ == TokenType.DIV:
                self.eat(TokenType.DIV)
                self.factor()

    def parse(self):
        self.expr()
