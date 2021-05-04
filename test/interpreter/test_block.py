from interpreter.eva import Eva
from pprint import pprint
# blocks
eva = Eva()
block_x_y = ['begin',
 ['var', 'x', 10],
 ['var', 'y', 20],
 ['+', ['*', 'x', 'y'], 30]
]
assert eva.eval(block_x_y) == 230
pprint(eva.invironments)

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
print('--------------------------------')
assert eva.eval(block_block) == 10
pprint(eva.invironments)

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
