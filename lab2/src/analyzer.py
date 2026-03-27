from .truth_table import TruthTable

class BooleanAnalyzer:
    def __init__(self, truth_table: TruthTable):
        self.tt = truth_table
        self.variables = truth_table.variables
        self.results = truth_table.results

    def find_dummy_variables(self) -> list:
        dummies = []
        n = len(self.variables)
        for i in range(n):
            is_dummy = True
            step = 1 << (n - 1 - i)
            for j in range(0, 1 << n, step * 2):
                for k in range(step):
                    if self.results[j + k] != self.results[j + k + step]:
                        is_dummy = False
                        break
                if not is_dummy:
                    break
            if is_dummy:
                dummies.append(self.variables[i])
        return dummies

    def get_partial_derivative(self, var_name: str) -> list:
        if var_name not in self.variables:
            return []
        var_index = self.variables.index(var_name)
        n = len(self.variables)
        derivative = [0] * (1 << n)
        step = 1 << (n - 1 - var_index)
        
        for j in range(0, 1 << n, step * 2):
            for k in range(step):
                val0 = self.results[j + k]
                val1 = self.results[j + k + step]
                diff = val0 ^ val1
                derivative[j + k] = diff
                derivative[j + k + step] = diff
        return derivative

    def get_mixed_derivative(self, var_names: list) -> list:
        current_results = list(self.results)
        n = len(self.variables)
        
        for var_name in var_names:
            if var_name not in self.variables:
                continue
            var_index = self.variables.index(var_name)
            next_results = [0] * (1 << n)
            step = 1 << (n - 1 - var_index)
            
            for j in range(0, 1 << n, step * 2):
                for k in range(step):
                    val0 = current_results[j + k]
                    val1 = current_results[j + k + step]
                    diff = val0 ^ val1
                    next_results[j + k] = diff
                    next_results[j + k + step] = diff
            current_results = next_results
        return current_results