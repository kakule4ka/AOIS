MAX_VARIABLES = 5
ALLOWED_VARIABLES = {'a', 'b', 'c', 'd', 'e'}

OP_AND = '&'
OP_OR = '|'
OP_NOT = '!'
OP_IMPL = '->'
OP_EQ = '~'
OP_XOR = '^'

PAREN_L = '('
PAREN_R = ')'

AND_ALIASES = {'&&'}
OR_ALIASES = {'V', 'v', '||'}

OPERATORS = {OP_AND, OP_OR, OP_NOT, OP_IMPL, OP_EQ, OP_XOR, PAREN_L, PAREN_R}

PRIORITIES = {
    OP_NOT: 4,
    OP_AND: 3,
    OP_OR: 2,
    OP_IMPL: 1,
    OP_EQ: 0,
    OP_XOR: 0
}