class ZhegalkinPolynomial:
    def __init__(self, function_results, variables: list):
        self.function_results = function_results
        self.variables = variables
        self.coefficients = self._calculate(function_results)

    def _calculate(self, raw_results) -> list:
        current_row = [int(value) for value in raw_results]
        calculated_coefficients = [current_row[0]]
        for _ in range(len(current_row) - 1):
            next_calculated_row = [current_row[index] ^ current_row[index+1] for index in range(len(current_row) - 1)]
            calculated_coefficients.append(next_calculated_row[0])
            current_row = next_calculated_row
        return calculated_coefficients

    def get_polynomial(self) -> str:
        polynomial_terms = []
        variable_count = len(self.variables)
        for index, coefficient in enumerate(self.coefficients):
            if coefficient:
                if index == 0:
                    polynomial_terms.append("1")
                else:
                    binary_representation = bin(index)[2:].zfill(variable_count)
                    included_variables = [self.variables[bit_index] for bit_index, bit in enumerate(binary_representation) if bit == '1']
                    polynomial_terms.append("".join(included_variables))
        if not polynomial_terms:
            return "0"
        return " ^ ".join(polynomial_terms)

    def is_linear(self) -> bool:
        for index, coefficient in enumerate(self.coefficients):
            if coefficient and bin(index).count('1') > 1:
                return False
        return True