from interpreter.environment import Environment
from interpreter.eva import Eva



# self-eval
eva = Eva()
assert eva.eval(1) == 1
assert eva.eval(1.1) == 1.1
assert eva.eval("\"hello\"") == "hello"
