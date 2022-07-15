from interpreter.token import Token, TokenType


def test_token():
    t = Token(type_=TokenType.INTEGER, value=3)
    print(t)
    assert t.type_ == TokenType.INTEGER
    assert t.value == 3
