import itertools
from .expr_parser import Evaluator

class TruthTable:
    def __init__(self, evaluator: Evaluator):
        self.evaluator = evaluator
        self.variables = evaluator.variables
        self.rows = []
        self.results = []
        self._generate()

    def _generate(self):
        n = len(self.variables)
        combinations = list(itertools.product([0, 1], repeat=n))
        for combo in combinations:
            val_dict = dict(zip(self.variables, combo))
            res = self.evaluator.evaluate(val_dict)
            self.rows.append(combo)
            self.results.append(res)

    def get_table(self) -> tuple:
        return self.variables, self.rows, self.results

    def get_on_set(self) -> list:
        return [row for row, res in zip(self.rows, self.results) if res == 1]

    def get_off_set(self) -> list:
        return [row for row, res in zip(self.rows, self.results) if res == 0]
    
    def get_index_form(self) -> str:
        return "".join(map(str, self.results))