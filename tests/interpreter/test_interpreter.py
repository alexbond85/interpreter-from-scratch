from interpreter.interpreter import Interpreter
from interpreter.token import Token, TokenType


def test_interpreter_moving_position():
    text = "1+2"
    interpreter = Interpreter(text)
    # init position is 0
    assert interpreter.pos == 0
    interpreter.get_next_token()
    assert interpreter.pos == 1
    interpreter.get_next_token()
    assert interpreter.pos == 2
    interpreter.get_next_token()
    assert interpreter.pos == 3
    # reaching end of text
    interpreter.get_next_token()
    assert interpreter.pos == 3
    interpreter.get_next_token()
    assert interpreter.pos == 3


def test_interpreter_get_next_token():
    text = "1+2"
    interpreter = Interpreter(text)
    token = interpreter.get_next_token()
    assert token == Token(TokenType.INTEGER, value=1)
    token = interpreter.get_next_token()
    assert token == Token(TokenType.PLUS, value="+")
    token = interpreter.get_next_token()
    assert token == Token(TokenType.INTEGER, value=2)
    token = interpreter.get_next_token()
    assert token == Token(TokenType.EOF, None)


def test_interpreter_eat():
    text = "1+2"
    interpreter = Interpreter(text)
    interpreter.current_token = interpreter.get_next_token()
    assert interpreter.current_token == Token(TokenType.INTEGER, 1)
    interpreter.eat(TokenType.INTEGER)
    assert interpreter.current_token == Token(TokenType.PLUS, "+")
    interpreter.eat(TokenType.PLUS)
    assert interpreter.current_token == Token(TokenType.INTEGER, 2)
    interpreter.eat(TokenType.INTEGER)
    assert interpreter.current_token == Token(TokenType.EOF, None)


def test_expr():
    text = " 1  +   2 "
    interpreter = Interpreter(text)
    assert interpreter.expr() == 3
    text = " 10  -   22 "
    interpreter = Interpreter(text)
    assert interpreter.expr() == -12


def test_advance():
    text = "1 + 2"
    interpreter = Interpreter(text)
    assert interpreter.current_char == "1"
    interpreter.advance()
    assert interpreter.current_char == " "
    interpreter.advance()
    assert interpreter.current_char == "+"
    interpreter.advance()
    assert interpreter.current_char == " "
    interpreter.advance()
    assert interpreter.current_char == "2"
    interpreter.advance()
    assert interpreter.current_char is None
    interpreter.advance()
    assert interpreter.current_char is None


def test_skip_whitespace():
    text = "1 + 2"
    interpreter = Interpreter(text)
    interpreter.skip_whitespace()
    assert interpreter.current_char == "1"
    text = "    1 + 2"
    interpreter = Interpreter(text)
    interpreter.skip_whitespace()
    assert interpreter.current_char == "1"


def test_integer():
    text = "12 + 24"
    interpreter = Interpreter(text)
    assert interpreter.integer() == 12


def test_term():
    text = "12 + 24"
    interpreter = Interpreter(text)
    interpreter.current_token = interpreter.get_next_token()
    assert interpreter.term() == 12
    assert interpreter.current_token == Token(TokenType.PLUS, '+')
    interpreter.current_token = interpreter.get_next_token()
    assert interpreter.term() == 24


def test_complex_expression():
    text = "10 + 11 + 12"
    interpreter = Interpreter(text)
    assert interpreter.expr() == 33


