from interpreter.interpreter import Interpreter
from interpreter.lexer import Lexer
from interpreter.parser import Parser


def test_eat():
    text = "    5      + 2 "
    lexer = Lexer(text=text)
    parser = Parser(lexer=lexer)
    interpreter = Interpreter(parser=parser)
    interpreter.run()


def test_run():
    text = " 1  +   2 "
    interpreter = Interpreter(Parser(Lexer(text)))
    assert interpreter.run() == 3
    text = " 10  -   22 "
    interpreter = Interpreter(Parser(Lexer(text)))
    assert interpreter.run() == -12
    text = " 10  -   22 * 0"
    interpreter = Interpreter(Parser(Lexer(text)))
    assert interpreter.run() == 10
    text = " 10  -   1 * 2 * 3"
    interpreter = Interpreter(Parser(Lexer(text)))
    assert interpreter.run() == 4
    text = " (1 + 2) * 3"
    interpreter = Interpreter(Parser(Lexer(text)))
    assert interpreter.run() == 9
    text = " (1 - + - 2) * 3"
    interpreter = Interpreter(Parser(Lexer(text)))
    assert interpreter.run() == 9


def test_complex_expression():
    text = "10 + 11 + 12"
    interpreter = Interpreter(Parser(Lexer(text)))
    assert interpreter.run() == 33
