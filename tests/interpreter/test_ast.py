from interpreter.ast import BinOp, Num
from interpreter.token import Token, TokenType


def test_ast():
    mul_token = Token(TokenType.MUL, "*")
    plus_token = Token(TokenType.PLUS, "+")
    mul_node = BinOp(
        left=Num(Token(TokenType.INTEGER, 2)),
        op=mul_token,
        right=Num(Token(TokenType.INTEGER, 7)),
    )
    add_node = BinOp(
        left=mul_node, op=plus_token, right=Num(Token(TokenType.INTEGER, 3))
    )
    assert add_node.right == Num(Token(TokenType.INTEGER, 3))
