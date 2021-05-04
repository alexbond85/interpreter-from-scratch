from interpreter.eva import Eva

# math
eva = Eva()
assert eva.eval(['+', 1, 4]) == 5
assert eva.eval(['+', ['+', 1, 3], 4]) == 8
assert eva.eval(['+', ['*', 2, 3], 4]) == 10

