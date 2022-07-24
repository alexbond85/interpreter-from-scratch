from interpreter.lexer import Lexer
from interpreter.token import Token, TokenType


def test_advance():
    text = "1 + 2"
    lexer = Lexer(text)
    # init position is 0
    assert lexer.pos == 0
    assert lexer.current_char == "1"
    lexer._advance()
    assert lexer.pos == 1
    assert lexer.current_char == " "
    lexer._advance()
    assert lexer.pos == 2
    assert lexer.current_char == "+"
    lexer._advance()
    assert lexer.pos == 3
    assert lexer.current_char == " "
    lexer._advance()
    assert lexer.pos == 4
    assert lexer.current_char == "2"
    lexer._advance()
    assert lexer.pos == 5
    assert lexer.current_char is None
    lexer._advance()
    assert lexer.pos == 6
    assert lexer.current_char is None


def test_skip_whitespace():
    text = "1 + 2"
    lexer = Lexer(text)
    lexer._skip_whitespace()
    assert lexer.current_char == "1"
    text = "    1 + 2"
    lexer = Lexer(text)
    lexer._skip_whitespace()
    assert lexer.current_char == "1"


def test_integer():
    text = "12 + 24"
    lexer = Lexer(text)
    assert lexer._number() == Token(TokenType.INTEGER_CONST, 12)


def test_get_next_token():
    text = "1   +  2  - "
    lexer = Lexer(text)
    token = lexer.get_next_token()
    assert token == Token(TokenType.INTEGER_CONST, value=1)
    token = lexer.get_next_token()
    assert token == Token(TokenType.PLUS, value="+")
    token = lexer.get_next_token()
    assert token == Token(TokenType.INTEGER_CONST, value=2)
    token = lexer.get_next_token()
    assert token == Token(TokenType.MINUS, value="-")
    token = lexer.get_next_token()
    assert token == Token(TokenType.EOF, None)
    lexer = Lexer("BEGIN a := 2; END.")
    assert lexer.get_next_token() == Token(TokenType.BEGIN, "BEGIN")
    assert lexer.get_next_token() == Token(TokenType.ID, "a")
    assert lexer.get_next_token() == Token(TokenType.ASSIGN, ":=")
    assert lexer.get_next_token() == Token(TokenType.INTEGER_CONST, 2)
    assert lexer.get_next_token() == Token(TokenType.SEMI, ";")
    assert lexer.get_next_token() == Token(TokenType.END, "END")
    assert lexer.get_next_token() == Token(TokenType.DOT, ".")
