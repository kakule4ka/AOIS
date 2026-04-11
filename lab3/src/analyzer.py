import itertools

class BooleanAnalyzer:
    def __init__(self, evaluator, variables):
        self.evaluator = evaluator
        self.variables = variables

    def find_dummy_variables(self) -> list:
        dummy_variables = []
        for variable in self.variables:
            derivative = self.get_derivative(variable)
            if all(character == '0' for character in derivative):
                dummy_variables.append(variable)
        return dummy_variables

    def get_derivative(self, target_variable: str) -> str:
        if target_variable not in self.variables:
            return ""
        
        other_variables = [variable for variable in self.variables if variable != target_variable]
        derivative_results = []
        
        for combination in itertools.product([0, 1], repeat=len(other_variables)):
            combination_values = list(combination)
            
            context_false = dict(zip(other_variables, combination_values))
            context_false[target_variable] = 0
            
            context_true = dict(zip(other_variables, combination_values))
            context_true[target_variable] = 1
            
            eval_context_false = {variable: context_false[variable] for variable in self.variables}
            eval_context_true = {variable: context_true[variable] for variable in self.variables}
            
            result_false = self.evaluator.evaluate(eval_context_false)
            result_true = self.evaluator.evaluate(eval_context_true)
            derivative_results.append(str(result_false ^ result_true))
            
        return "".join(derivative_results)