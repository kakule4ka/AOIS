from .constants import (
    OPERATORS, PRIORITIES, OP_NOT, OP_AND, OP_OR, OP_IMPL, OP_EQ,
    PAREN_L, PAREN_R, OR_ALIASES
)

class Tokenizer:
    def __init__(self, expression: str):
        self.expression = expression.replace(' ', '')
        for alias in OR_ALIASES:
            self.expression = self.expression.replace(alias, OP_OR)

    def tokenize(self) -> list:
        tokens = []
        i = 0
        while i < len(self.expression):
            char = self.expression[i]
            if self.expression.startswith(OP_IMPL, i):
                tokens.append(OP_IMPL)
                i += len(OP_IMPL)
                continue
            tokens.append(char)
            i += 1
        return tokens

class RPNConverter:
    def convert(self, tokens: list) -> list:
        output = []
        stack = []
        for token in tokens:
            if token.isalpha() and token not in OR_ALIASES:
                output.append(token)
            elif token == PAREN_L:
                stack.append(token)
            elif token == PAREN_R:
                while stack and stack[-1] != PAREN_L:
                    output.append(stack.pop())
                if stack:
                    stack.pop()
            elif token in OPERATORS:
                while (stack and stack[-1] != PAREN_L and
                       PRIORITIES.get(stack[-1], -1) >= PRIORITIES.get(token, -1)):
                    output.append(stack.pop())
                stack.append(token)
        while stack:
            output.append(stack.pop())
        return output

class Evaluator:
    def __init__(self, rpn: list, variables: list):
        self.rpn = rpn
        self.variables = sorted(list(variables))

    def evaluate(self, values: dict) -> int:
        stack = []
        for token in self.rpn:
            if token in self.variables:
                stack.append(values[token])
            elif token == OP_NOT:
                val = stack.pop()
                stack.append(int(not val))
            elif token in OPERATORS:
                b = stack.pop()
                a = stack.pop()
                if token == OP_AND:
                    stack.append(a & b)
                elif token == OP_OR:
                    stack.append(a | b)
                elif token == OP_IMPL:
                    stack.append(int(not a or b))
                elif token == OP_EQ:
                    stack.append(int(a == b))
        return stack[0]

class ExpressionParser:
    def parse(self, expression: str) -> Evaluator:
        tokenizer = Tokenizer(expression)
        tokens = tokenizer.tokenize()
        converter = RPNConverter()
        rpn = converter.convert(tokens)
        variables = {t for t in tokens if t.isalpha() and t not in OPERATORS and t not in OR_ALIASES}
        return Evaluator(rpn, list(variables))