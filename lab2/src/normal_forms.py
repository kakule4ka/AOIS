from .truth_table import TruthTable

class NormalForms:
    def __init__(self, truth_table: TruthTable):
        self.tt = truth_table
        self.variables = truth_table.variables
        self.on_set = truth_table.get_on_set()
        self.off_set = truth_table.get_off_set()

    def _format_term(self, row: tuple, is_sdnf: bool) -> str:
        terms = []
        for var, val in zip(self.variables, row):
            if is_sdnf:
                terms.append(var if val else f"!{var}")
            else:
                terms.append(f"!{var}" if val else var)
        join_op = "&" if is_sdnf else "|"
        return f"({join_op.join(terms)})"

    def get_sdnf(self) -> str:
        if not self.on_set:
            return "0"
        return " | ".join(self._format_term(row, True) for row in self.on_set)

    def get_sknf(self) -> str:
        if not self.off_set:
            return "1"
        return " & ".join(self._format_term(row, False) for row in self.off_set)

    def get_sdnf_numeric(self) -> list:
        return [int("".join(map(str, row)), 2) for row in self.on_set]

    def get_sknf_numeric(self) -> list:
        return [int("".join(map(str, row)), 2) for row in self.off_set]