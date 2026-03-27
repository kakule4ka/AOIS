class ZhegalkinPolynomial:
    def __init__(self, truth_table_results: list, variables: list):
        self.results = truth_table_results
        self.variables = variables
        self.coefficients = self._calculate_coefficients()

    def _calculate_coefficients(self) -> list:
        current_row = list(self.results)
        coeffs = [current_row[0]]
        for _ in range(len(current_row) - 1):
            next_row = []
            for i in range(len(current_row) - 1):
                next_row.append(current_row[i] ^ current_row[i+1])
            coeffs.append(next_row[0])
            current_row = next_row
        return coeffs

    def get_polynomial(self) -> str:
        terms = []
        n = len(self.variables)
        for i, coeff in enumerate(self.coefficients):
            if coeff:
                if i == 0:
                    terms.append("1")
                else:
                    bin_str = bin(i)[2:].zfill(n)
                    term_vars = [self.variables[j] for j, bit in enumerate(bin_str) if bit == '1']
                    terms.append("".join(term_vars))
        if not terms:
            return "0"
        return " ^ ".join(terms)
        
    def is_linear(self) -> bool:
        n = len(self.variables)
        for i, coeff in enumerate(self.coefficients):
            if coeff:
                bin_str = bin(i)[2:].zfill(n)
                if bin_str.count('1') > 1:
                    return False
        return True