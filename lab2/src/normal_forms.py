class NormalForms:
    def __init__(self, truth_table):
        self.truth_table = truth_table
        self.variables = truth_table.variables

    def get_sdnf(self) -> str:
        truth_set = self.truth_table.get_on_set()
        if not truth_set:
            return "0"
        minterms = []
        for row in truth_set:
            minterm_parts = []
            for index, value in enumerate(row):
                minterm_parts.append(self.variables[index] if value == 1 else f"!{self.variables[index]}")
            
            if len(minterm_parts) == 1:
                minterms.append(minterm_parts[0])
            else:
                minterms.append("(" + " & ".join(minterm_parts) + ")")
                
        return " | ".join(minterms)

    def get_sknf(self) -> str:
        false_set = self.truth_table.get_off_set()
        if not false_set:
            return "1"
        maxterms = []
        for row in false_set:
            maxterm_parts = []
            for index, value in enumerate(row):
                maxterm_parts.append(f"!{self.variables[index]}" if value == 1 else self.variables[index])
                
            if len(maxterm_parts) == 1:
                maxterms.append(maxterm_parts[0])
            else:
                maxterms.append("(" + " | ".join(maxterm_parts) + ")")
                
        return " & ".join(maxterms)

    def get_sdnf_numeric(self) -> str:
        truth_set = self.truth_table.get_on_set()
        numeric_values = [int("".join(map(str, row)), 2) for row in truth_set]
        return str(numeric_values)

    def get_sknf_numeric(self) -> str:
        false_set = self.truth_table.get_off_set()
        numeric_values = [int("".join(map(str, row)), 2) for row in false_set]
        return str(numeric_values)