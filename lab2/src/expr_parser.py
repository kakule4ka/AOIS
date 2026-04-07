from .constants import ALLOWED_VARIABLES, OPERATORS, PRIORITIES, OR_ALIASES, AND_ALIASES, OP_OR, OP_AND, OP_IMPL, PAREN_L, PAREN_R, OP_NOT, OP_EQ

class Tokenizer:
    def __init__(self, expression: str):
        clean_expression = expression.replace(' ', '')
        for alias in OR_ALIASES:
            clean_expression = clean_expression.replace(alias, OP_OR)
        for alias in AND_ALIASES:
            clean_expression = clean_expression.replace(alias, OP_AND)
        self.expression = clean_expression

    def tokenize(self) -> list:
        tokens = []
        index = 0
        while index < len(self.expression):
            character = self.expression[index]
            
            if character.isalpha():
                if character not in ALLOWED_VARIABLES:
                    raise ValueError(f"Разрешены только переменные a, b, c, d, e. Найдена: '{character}'")
                if tokens and (tokens[-1].isalpha() or tokens[-1] == PAREN_R):
                    raise ValueError(f"Пропущен оператор перед переменной '{character}' на позиции {index+1}")
                tokens.append(character)
                index += 1
            elif character in OPERATORS:
                if character == PAREN_L and tokens and (tokens[-1].isalpha() or tokens[-1] == PAREN_R):
                     raise ValueError(f"Пропущен оператор перед скобкой '(' на позиции {index+1}")
                tokens.append(character)
                index += 1
            elif self.expression.startswith(OP_IMPL, index):
                tokens.append(OP_IMPL)
                index += 2
            else:
                raise ValueError(f"Неизвестный символ на позиции {index+1}: '{character}'")
                
        return tokens


class RPNConverter:
    def __init__(self, tokens: list):
        self.tokens = tokens

    def convert(self) -> list:
        output_queue = []
        operator_stack = []
        
        for token in self.tokens:
            if token.isalpha():
                output_queue.append(token)
            elif token == PAREN_L:
                operator_stack.append(token)
            elif token == PAREN_R:
                while operator_stack and operator_stack[-1] != PAREN_L:
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Пропущена левая скобка '('")
                operator_stack.pop()
            else:
                while (operator_stack and operator_stack[-1] != PAREN_L and 
                       PRIORITIES.get(operator_stack[-1], 0) >= PRIORITIES.get(token, 0)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
                
        while operator_stack:
            if operator_stack[-1] == PAREN_L:
                raise ValueError("Пропущена правая скобка ')'")
            output_queue.append(operator_stack.pop())
            
        return output_queue


class Evaluator:
    def __init__(self, rpn_tokens: list, variables: list):
        self.rpn_tokens = rpn_tokens
        self.variables = variables

    def evaluate(self, variable_values: dict) -> int:
        evaluation_stack = []
        for token in self.rpn_tokens:
            if token in self.variables:
                evaluation_stack.append(variable_values[token])
            elif token == OP_NOT:
                if not evaluation_stack: 
                    raise ValueError("Не хватает операнда для отрицания '!'")
                operand = evaluation_stack.pop()
                evaluation_stack.append(int(not operand))
            else:
                if len(evaluation_stack) < 2: 
                    raise ValueError(f"Не хватает операндов для оператора '{token}'")
                right_operand = evaluation_stack.pop()
                left_operand = evaluation_stack.pop()
                
                if token == OP_AND: 
                    evaluation_stack.append(left_operand & right_operand)
                elif token == OP_OR: 
                    evaluation_stack.append(left_operand | right_operand)
                elif token == OP_IMPL: 
                    evaluation_stack.append(int((not left_operand) or right_operand))
                elif token == OP_EQ: 
                    evaluation_stack.append(int(left_operand == right_operand))
                
        if len(evaluation_stack) != 1:
            raise ValueError("Синтаксическая ошибка: нарушен баланс переменных и операторов")
            
        return evaluation_stack[0]


class ExpressionParser:
    def parse(self, expression_string: str):
        if not expression_string.strip():
            raise ValueError("Введена пустая строка")
            
        tokenizer = Tokenizer(expression_string)
        tokens = tokenizer.tokenize()
        
        if not tokens:
            raise ValueError("Выражение не содержит допустимых символов")
            
        converter = RPNConverter(tokens)
        rpn_queue = converter.convert()
        
        unique_variables = sorted(list(set([token for token in tokens if token.isalpha()])))
        if not unique_variables:
            raise ValueError("Функция должна содержать хотя бы одну буквенную переменную")
            
        evaluator = Evaluator(rpn_queue, unique_variables)
        
        test_values = {variable: 0 for variable in unique_variables}
        try:
            evaluator.evaluate(test_values)
        except Exception as error:
            raise ValueError(str(error))
            
        return evaluator