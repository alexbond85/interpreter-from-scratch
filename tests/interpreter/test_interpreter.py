from interpreter.interpreter import Interpreter
from interpreter.lexer import Lexer
from interpreter.parser import Parser


def test_visitors():
    text = " 1  +   2 "
    parser = Parser(Lexer(text))
    expr = parser.expr()
    assert Interpreter(None).visit(expr) == 3
    text = " 10  -   22 "
    parser = Parser(Lexer(text))
    expr = parser.expr()
    assert Interpreter(None).visit(expr) == -12
    text = " 10  -   22 * 0"
    parser = Parser(Lexer(text))
    expr = parser.expr()
    assert Interpreter(None).visit(expr) == 10
    text = " 10  -   1 * 2 * 3"
    parser = Parser(Lexer(text))
    expr = parser.expr()
    assert Interpreter(None).visit(expr) == 4
    text = " (1 + 2) * 3"
    parser = Parser(Lexer(text))
    expr = parser.expr()
    assert Interpreter(None).visit(expr) == 9
    text = " (1 - + - 2) * 3"
    parser = Parser(Lexer(text))
    expr = parser.expr()
    assert Interpreter(None).visit(expr) == 9


def test_complex_expression():
    text = "10 + 11 + 12"
    parser = Parser(Lexer(text))
    assert Interpreter(None).visit(parser.expr())


def test_global_scope():
    text = """\
    BEGIN
            BEGIN
            number := 2;
            a := number;
            b := 10 * a + 10 * number / 4;
            c := a - - b
        END;
            x := 11;
    END.
    """
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.run()
    expected_scope = {"number": 2, "a": 2, "b": 25, "c": 27, "x": 11}
    assert interpreter.GLOBAL_SCOPE == expected_scope
