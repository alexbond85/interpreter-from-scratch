from dataclasses import dataclass
from enum import Enum, auto
from typing import Any

# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis

# The process of breaking the input string into tokens
# is called lexical analysis (lexer, scanner or tokenizer).

# A lexeme is a sequence of characters that form a token.


class TokenType(Enum):
    INTEGER = auto()
    PLUS = auto()
    EOF = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    LPAREN = auto()
    RPAREN = auto()


@dataclass
class Token(object):
    """
    A token is an object that has a type and a value.
    """

    type_: TokenType
    value: Any

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return "Token({type}, {value})".format(
            type=self.type_, value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()
