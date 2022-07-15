import pytest
from interpreter.interpreter import Interpreter, InterpreterError
from interpreter.lexer import Lexer
from interpreter.token import TokenType


def test_eat():
    text = "    5      + 2 "
    lexer = Lexer(text)
    parser = Interpreter(lexer=lexer)
    parser.eat(TokenType.INTEGER)
    with pytest.raises(InterpreterError):
        parser.eat(TokenType.MINUS)
    parser.eat(TokenType.PLUS)
    parser.eat(TokenType.INTEGER)


def test_expr():
    text = " 1  +   2 "
    interpreter = Interpreter(Lexer(text))
    assert interpreter.expr() == 3
    text = " 10  -   22 "
    interpreter = Interpreter(Lexer(text))
    assert interpreter.expr() == -12


def test_complex_expression():
    text = "10 + 11 + 12"
    interpreter = Interpreter(Lexer(text))
    assert interpreter.expr() == 33
