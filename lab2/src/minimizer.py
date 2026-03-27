from .truth_table import TruthTable

class Minimizer:
    def __init__(self, truth_table: TruthTable):
        self.tt = truth_table
        self.variables = truth_table.variables
        self.on_set = truth_table.get_on_set()

    def _to_bin_str(self, row: tuple) -> str:
        return "".join(map(str, row))

    def _differs_by_one(self, a: str, b: str) -> int:
        diff = 0
        idx = -1
        for i in range(len(a)):
            if a[i] != b[i]:
                diff += 1
                idx = i
        return idx if diff == 1 else -1

    def _glue_step(self, terms: set) -> tuple:
        new_terms = set()
        used = set()
        terms_list = list(terms)
        
        for i in range(len(terms_list)):
            for j in range(i + 1, len(terms_list)):
                idx = self._differs_by_one(terms_list[i], terms_list[j])
                if idx != -1:
                    glued = terms_list[i][:idx] + '-' + terms_list[i][idx+1:]
                    new_terms.add(glued)
                    used.add(terms_list[i])
                    used.add(terms_list[j])
                    
        uncovered = terms - used
        return new_terms, uncovered

    def get_calculation_method(self) -> dict:
        stages = []
        current_terms = {self._to_bin_str(row) for row in self.on_set}
        all_prime = set()
        
        stages.append(list(current_terms))
        
        while current_terms:
            new_terms, uncovered = self._glue_step(current_terms)
            all_prime.update(uncovered)
            if not new_terms:
                break
            stages.append(list(new_terms))
            current_terms = new_terms
            
        return {
            "stages": stages,
            "prime_implicants": list(all_prime)
        }

    def get_calculation_tabular_method(self) -> dict:
        calc_data = self.get_calculation_method()
        primes = calc_data["prime_implicants"]
        minterms = [self._to_bin_str(row) for row in self.on_set]
        
        table = {p: [] for p in primes}
        for p in primes:
            for m in minterms:
                match = True
                for i in range(len(p)):
                    if p[i] != '-' and p[i] != m[i]:
                        match = False
                        break
                if match:
                    table[p].append(m)
                    
        return {
            "stages": calc_data["stages"],
            "table": table
        }