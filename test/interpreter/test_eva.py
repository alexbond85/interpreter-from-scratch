from interpreter.environment import Environment
from interpreter.eva import Eva



# test
eva = Eva()
assert eva.eval(1) == 1
assert eva.eval(1.1) == 1.1
assert eva.eval("\"hello\"") == "hello"

# math
eva = Eva()
assert eva.eval(['+', 1, 4]) == 5
assert eva.eval(['+', ['+', 1, 3], 4]) == 8
assert eva.eval(['+', ['*', 2, 3], 4]) == 10

# variables
eva = Eva()
assert eva.eval(['var', 'x', 10]) == 10
assert eva.eval('x') == 10
assert eva.eval("true") is True
assert eva.eval(['var', 'x', "true"]) is True
assert eva.eval(['var', 'x', ['*', 2, 2]]) == 4

# blocks
eva = Eva()
block_x_y = ['begin',
 ['var', 'x', 10],
 ['var', 'y', 20],
 ['+', ['*', 'x', 'y'], 30]
 ]
assert eva.eval(block_x_y) == 230

eva = Eva()
block_block = [
    'begin',
        ['var', 'x', 10],
        ['begin',
            ['var', 'x', 20],
             'x'
        ],
        'x'
]
assert eva.eval(block_block) == 10
eva = Eva()
block_block_vars = [
    'begin',
        ['var', 'value', 10],
        ['var', 'result', ['begin',
                           ['var', 'x', ['+', 'value', 15]],
                            'x'
                          ]
        ],
         'result'
        ]
assert eva.eval(block_block_vars) == 25
# assignment
eva = Eva()
block_block_assign = [
    'begin',
        ['var', 'data', 10],
        ['begin',
          ['set', 'data', 100]
        ],
    'data'
]

assert eva.eval(block_block_assign) == 100
