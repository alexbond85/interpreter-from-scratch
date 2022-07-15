from dataclasses import dataclass
from typing import Any, NoReturn, Optional

from interpreter.token import Token, TokenType


@dataclass
class InterpreterError(Exception):
    error_msg: str


class Interpreter(object):
    """
    Processes and executes the source program without
    translating it into machine language first.
    """

    def __init__(self, text: str):
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token: Optional[Token] = None
        self.current_char: Optional[str] = self.text[self.pos]

    def advance(self) -> None:
        """Advance the 'pos' pointer and set the 'current_char' variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self) -> int:
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def error(self) -> NoReturn:
        raise InterpreterError("Error parsing input")

    def get_next_token(self) -> Token:
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """

        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(TokenType.INTEGER, self.integer())

            if self.current_char == "+":
                self.advance()
                return Token(TokenType.PLUS, "+")

            if self.current_char == "-":
                self.advance()
                return Token(TokenType.MINUS, "-")
            self.error()
        return Token(TokenType.EOF, None)

    def eat(self, token_type: TokenType) -> None:
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        # current_token: Token = self.current_token
        if self.current_token and self.current_token.type_ == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def term(self) -> Any:
        token = self.current_token
        self.eat(TokenType.INTEGER)
        return token.value

    def expr(self) -> int:
        """expr -> INTEGER PLUS INTEGER
        Two steps: parsing and interpreting.
        - Parsing is the process of finding the structure in the stream of tokens,
          or put differently, the process of recognizing a phrase in the
          stream of tokens.
        - Interpreting: performs addition/subtraction.

        A syntax diagram is a graphical representation of a programming
        language’s syntax rules.

        Syntax diagrams serve two main purposes:
        - They graphically represent the specification (grammar) of
          a programming language.
        - They can be used to help you write your parser - you can
          map a diagram to code by following simple rules.
        """
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()
        result = self.term()
        arithmethic_ops = (TokenType.PLUS, TokenType.MINUS)
        while self.current_token and self.current_token.type_ in arithmethic_ops:
            token = self.current_token
            if token.type_ == TokenType.PLUS:
                self.eat(TokenType.PLUS)
                result = result + self.term()
            elif token.type_ == TokenType.MINUS:
                self.eat(TokenType.MINUS)
                result = result - self.term()
        return result
