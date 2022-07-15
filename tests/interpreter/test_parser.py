import pytest

from interpreter.lexer import Lexer
from interpreter.parser import InterpreterParserError, Parser
from interpreter.token import Token, TokenType


def test_factor():
    text = "    1      "
    lexer = Lexer(text)
    parser = Parser(lexer=lexer)
    parser.factor()
    assert lexer.get_next_token() == Token(TokenType.EOF, None)


def test_eat():
    text = "    5      + 2 "
    lexer = Lexer(text)
    parser = Parser(lexer=lexer)
    parser.eat(TokenType.INTEGER)
    with pytest.raises(InterpreterParserError):
        parser.eat(TokenType.MINUS)
    parser.eat(TokenType.PLUS)
    parser.eat(TokenType.INTEGER)
