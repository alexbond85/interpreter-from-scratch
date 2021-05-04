from interpreter.environment import Environment
from interpreter.eva import Eva

# variables
eva = Eva()
assert eva.eval(['var', 'x', 10]) == 10
assert eva.eval('x') == 10
assert eva.eval("true") is True
assert eva.eval(['var', 'x', "true"]) is True
assert eva.eval(['var', 'x', ['*', 2, 2]]) == 4

