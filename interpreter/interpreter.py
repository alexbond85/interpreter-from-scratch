from dataclasses import dataclass
from typing import NoReturn

from interpreter.lexer import Lexer
from interpreter.token import Token, TokenType


@dataclass
class InterpreterError(Exception):
    error_msg: str


class Interpreter(object):
    """
    Processes and executes the source program without
    translating it into machine language first.
    """

    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token: Token = lexer.get_next_token()

    def error(self) -> NoReturn:
        raise InterpreterError("Error parsing input")

    def eat(self, token_type: TokenType) -> None:
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        # current_token: Token = self.current_token
        if self.current_token and self.current_token.type_ == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """factor : INTEGER | LPAREN expr RPAREN"""
        token = self.current_token
        if token.type_ == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return token.value
        elif token.type_ == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            result = self.expr()
            self.eat(TokenType.RPAREN)
            return result

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        result = self.factor()

        while self.current_token.type_ in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            if token.type_ == TokenType.MUL:
                self.eat(TokenType.MUL)
                result = result * self.factor()
            elif token.type_ == TokenType.DIV:
                self.eat(TokenType.DIV)
                result = result // self.factor()

        return result

    def expr(self) -> int:
        """Arithmetic expression parser / interpreter.
        calc>  14 + 2 * 3 - 6 / 2
        17
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER
        """
        result = self.term()

        while self.current_token.type_ in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type_ == TokenType.PLUS:
                self.eat(TokenType.PLUS)
                result = result + self.term()
            elif token.type_ == TokenType.MINUS:
                self.eat(TokenType.MINUS)
                result = result - self.term()

        return result
