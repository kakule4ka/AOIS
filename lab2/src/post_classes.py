class PostClasses:
    def __init__(self, truth_table, zhegalkin_polynomial):
        self.truth_table = truth_table
        self.zhegalkin_polynomial = zhegalkin_polynomial
        self.variables = truth_table.variables
        self.function_results = [row[1] for row in truth_table.table]

    def is_T0(self):
        return self.function_results[0] == 0

    def is_T1(self):
        return self.function_results[-1] == 1

    def is_S(self):
        total_results = len(self.function_results)
        for index in range(total_results // 2):
            if self.function_results[index] == self.function_results[total_results - 1 - index]:
                return False
        return True

    def is_M(self):
        table_data = self.truth_table.table
        for index_a in range(len(table_data)):
            for index_b in range(index_a + 1, len(table_data)):
                row_a, result_a = table_data[index_a]
                row_b, result_b = table_data[index_b]
                
                is_less_or_equal = True
                for bit_index in range(len(row_a)):
                    if row_a[bit_index] > row_b[bit_index]:
                        is_less_or_equal = False
                        break
                
                if is_less_or_equal and result_a > result_b:
                    return False
        return True

    def is_L(self):
        return self.zhegalkin_polynomial.is_linear()

    def get_all_classes(self):
        return {
            "T0": self.is_T0(),
            "T1": self.is_T1(),
            "S": self.is_S(),
            "M": self.is_M(),
            "L": self.is_L()
        }