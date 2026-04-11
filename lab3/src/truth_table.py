import itertools

class TruthTable:
    def __init__(self, evaluator):
        self.evaluator = evaluator
        self.variables = evaluator.variables
        self.table = self._generate()

    def _generate(self):
        generated_table = []
        variable_count = len(self.variables)
        for combination in itertools.product([0, 1], repeat=variable_count):
            value_dictionary = dict(zip(self.variables, combination))
            evaluation_result = self.evaluator.evaluate(value_dictionary)
            generated_table.append((list(combination), evaluation_result))
        return generated_table

    def get_on_set(self):
        return [row[0] for row in self.table if row[1] == 1]

    def get_off_set(self):
        return [row[0] for row in self.table if row[1] == 0]

    def get_index_form(self):
        return "".join(str(row[1]) for row in self.table)

    def __str__(self):
        header = "\t".join(self.variables) + "\t| f"
        lines = [header, "-" * len(header.expandtabs(8))]
        for row, evaluation_result in self.table:
            formatted_line = "\t".join(map(str, row)) + f"\t| {evaluation_result}"
            lines.append(formatted_line)
        return "\n".join(lines)