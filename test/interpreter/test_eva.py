from interpreter.eva import Eva

eva = Eva()

# test
assert eva.eval(1) == 1
assert eva.eval(1.1) == 1.1
assert eva.eval("\"hello\"") == "hello"

# math
assert eva.eval(['+', 1, 4]) == 5
assert eva.eval(['+', ['+', 1, 3], 4]) == 8
assert eva.eval(['+', ['*', 2, 3], 4]) == 10

# variables

assert eva.eval(['var', 'x', 10]) == 10

assert eva.eval('x') == 10

assert eva.eval("true") is True

assert eva.eval(['var', 'x', "true"]) is True

assert eva.eval(['var', 'x', ['*', 2, 2]]) == 4
