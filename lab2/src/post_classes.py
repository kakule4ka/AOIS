from .truth_table import TruthTable
from .zhegalkin import ZhegalkinPolynomial

class PostClasses:
    def __init__(self, truth_table: TruthTable, zhegalkin: ZhegalkinPolynomial):
        self.tt = truth_table
        self.zh = zhegalkin
        self.results = truth_table.results
        self.rows = truth_table.rows

    def is_T0(self) -> bool:
        return self.results[0] == 0

    def is_T1(self) -> bool:
        return self.results[-1] == 1

    def is_S(self) -> bool:
        n = len(self.results)
        for i in range(n // 2):
            if self.results[i] == self.results[n - 1 - i]:
                return False
        return True

    def is_M(self) -> bool:
        for i in range(len(self.rows)):
            for j in range(i + 1, len(self.rows)):
                if self._is_less_or_equal(self.rows[i], self.rows[j]):
                    if self.results[i] > self.results[j]:
                        return False
        return True

    def _is_less_or_equal(self, row1: tuple, row2: tuple) -> bool:
        for b1, b2 in zip(row1, row2):
            if b1 > b2:
                return False
        return True

    def is_L(self) -> bool:
        return self.zh.is_linear()

    def get_all_classes(self) -> dict:
        return {
            "T0": self.is_T0(),
            "T1": self.is_T1(),
            "S": self.is_S(),
            "M": self.is_M(),
            "L": self.is_L()
        }