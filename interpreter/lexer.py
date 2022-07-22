from dataclasses import dataclass
from typing import Optional

from interpreter.token import Token, TokenType

RESERVED_KEYWORDS = {
    'BEGIN': Token(TokenType.BEGIN, 'BEGIN'),
    'END': Token(TokenType.END, 'END'),
}


@dataclass
class LexerError(Exception):
    error_msg: str


class Lexer:
    """Lexical analyzer (also known as scanner or tokenizer)

    This method is responsible for breaking a sentence
    apart into tokens. One token at a time.
    """

    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def _error(self):
        raise LexerError("Invalid character")

    def _advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def _skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self._advance()

    def _integer(self) -> int:
        """Return a (multidigit) integer consumed from the input."""
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self._advance()
        return int(result)

    def _id(self):
        """Handle identifiers and reserved keywords"""
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self._advance()

        token = RESERVED_KEYWORDS.get(result, Token(TokenType.ID, result))
        return token

    def _peek(self) -> Optional[str]:
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        return self.text[peek_pos]

    def get_next_token(self) -> Token:
        """Lexical analyzer (also known as scanner or tokenizer)
        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self._skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(TokenType.INTEGER, self._integer())

            if self.current_char == "*":
                self._advance()
                return Token(TokenType.MUL, "*")

            if self.current_char == "/":
                self._advance()
                return Token(TokenType.DIV, "/")

            if self.current_char == "+":
                self._advance()
                return Token(TokenType.PLUS, "+")

            if self.current_char == "-":
                self._advance()
                return Token(TokenType.MINUS, "-")

            if self.current_char == "(":
                self._advance()
                return Token(TokenType.LPAREN, "(")

            if self.current_char == ")":
                self._advance()
                return Token(TokenType.RPAREN, ")")

            if self.current_char.isalpha():
                return self._id()

            if self.current_char == ':' and self._peek() == '=':
                self._advance()
                self._advance()
                return Token(TokenType.ASSIGN, ':=')

            if self.current_char == ';':
                self._advance()
                return Token(TokenType.SEMI, ';')

            if self.current_char == '.':
                self._advance()
                return Token(TokenType.DOT, '.')

            self._error()

        return Token(TokenType.EOF, None)
