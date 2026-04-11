from .constants import MAX_VARIABLES, OP_NOT, OP_AND, OP_OR, PAREN_L, PAREN_R

class Minimizer:
    def __init__(self, truth_table):
        self.variables = truth_table.variables
        self.truth_table = truth_table

    def _get_difference_index(self, term_a, term_b):
        differing_indices = [index for index in range(len(term_a)) if term_a[index] != term_b[index]]
        return differing_indices[0] if len(differing_indices) == 1 else -1

    def _is_covering(self, prime_implicant, minterm):
        return all(prime_implicant[index] == '-' or prime_implicant[index] == minterm[index] for index in range(len(prime_implicant)))

    def format_result(self, prime_implicants, is_sdnf):
        if not prime_implicants:
            return "0" if is_sdnf else "1"
        formatted_terms = []
        for implicant in prime_implicants:
            term_parts = []
            for index, character in enumerate(implicant):
                if character == '-':
                    continue
                is_inverted = (character == '0' if is_sdnf else character == '1')
                term_parts.append(f"{OP_NOT if is_inverted else ''}{self.variables[index]}")
            
            inner_separator = f" {OP_AND} " if is_sdnf else f" {OP_OR} "
            term_string = inner_separator.join(term_parts)
            
            if len(term_parts) > 1:
                term_string = f"{PAREN_L}{term_string}{PAREN_R}"
            formatted_terms.append(term_string)
            
        outer_separator = f" {OP_OR} " if is_sdnf else f" {OP_AND} "
        return outer_separator.join(formatted_terms)

    def get_minimal_dnf(self, prime_implicants, target_minterms):
        essential_implicants = []
        uncovered_minterms = set(target_minterms)
        
        for minterm in target_minterms:
            covering_implicants = [implicant for implicant in prime_implicants if self._is_covering(implicant, minterm)]
            if len(covering_implicants) == 1:
                essential_prime = covering_implicants[0]
                if essential_prime not in essential_implicants:
                    essential_implicants.append(essential_prime)
                    uncovered_minterms = {uncovered for uncovered in uncovered_minterms if not self._is_covering(essential_prime, uncovered)}
                    
        while uncovered_minterms:
            minterm = next(iter(uncovered_minterms))
            best_implicant = max(prime_implicants, key=lambda implicant: len([uncovered for uncovered in uncovered_minterms if self._is_covering(implicant, uncovered)]))
            essential_implicants.append(best_implicant)
            uncovered_minterms = {uncovered for uncovered in uncovered_minterms if not self._is_covering(best_implicant, uncovered)}
            
        return essential_implicants

    def get_calculation_method(self, for_sdnf=True):
        target_dataset = self.truth_table.get_on_set() if for_sdnf else self.truth_table.get_off_set()
        target_minterms = ["".join(map(str, row)) for row in target_dataset]
        
        if not target_minterms:
            return {"stages": [], "prime_implicants": [], "minimal_form": "0" if for_sdnf else "1"}

        minimization_stages = [list(set(target_minterms))]
        all_prime_implicants = set()
        
        while minimization_stages[-1]:
            next_stage_implicants = set()
            used_implicants = set()
            current_stage_implicants = minimization_stages[-1]
            
            for index_a in range(len(current_stage_implicants)):
                for index_b in range(index_a + 1, len(current_stage_implicants)):
                    diff_index = self._get_difference_index(current_stage_implicants[index_a], current_stage_implicants[index_b])
                    if diff_index != -1:
                        new_implicant = current_stage_implicants[index_a][:diff_index] + '-' + current_stage_implicants[index_a][diff_index+1:]
                        next_stage_implicants.add(new_implicant)
                        used_implicants.update([current_stage_implicants[index_a], current_stage_implicants[index_b]])
                        
            all_prime_implicants.update(set(current_stage_implicants) - used_implicants)
            if not next_stage_implicants:
                break
            minimization_stages.append(list(next_stage_implicants))

        prime_implicants_list = list(all_prime_implicants)
        minimal_raw_form = self.get_minimal_dnf(prime_implicants_list, target_minterms)
        formatted_result = self.format_result(minimal_raw_form, for_sdnf)

        return {
            "stages": minimization_stages,
            "prime_implicants": prime_implicants_list,
            "minimal_form": formatted_result
        }

    def get_tabular_method(self, for_sdnf=True):
        calculation_result = self.get_calculation_method(for_sdnf)
        prime_implicants = calculation_result["prime_implicants"]
        
        target_dataset = self.truth_table.get_on_set() if for_sdnf else self.truth_table.get_off_set()
        minterms = ["".join(map(str, row)) for row in target_dataset]
        
        coverage_table = {implicant: [minterm for minterm in minterms if self._is_covering(implicant, minterm)] for implicant in prime_implicants}
        
        return {
            "stages": calculation_result["stages"], 
            "table": coverage_table, 
            "minimal_form": calculation_result["minimal_form"]
        }

    def get_karnaugh_map(self):
        variable_count = len(self.variables)
        if variable_count < 2 or variable_count > MAX_VARIABLES:
            return f"Карта Карно поддерживается для 2-{MAX_VARIABLES} переменных."
        
        if variable_count == 2:
            row_variables, col_variables = [self.variables[0]], [self.variables[1]]
            row_sequence, col_sequence = ['0', '1'], ['0', '1']
        elif variable_count == 3:
            row_variables, col_variables = [self.variables[0]], [self.variables[1], self.variables[2]]
            row_sequence, col_sequence = ['0', '1'], ['00', '01', '11', '10']
        elif variable_count == 4:
            row_variables, col_variables = [self.variables[0], self.variables[1]], [self.variables[2], self.variables[3]]
            row_sequence, col_sequence = ['00', '01', '11', '10'], ['00', '01', '11', '10']
        else:
            row_variables, col_variables = [self.variables[0], self.variables[1]], [self.variables[2], self.variables[3], self.variables[4]]
            row_sequence, col_sequence = ['00', '01', '11', '10'], ['000', '001', '011', '010', '110', '111', '101', '100']

        result_map = [[""] + col_sequence]
        for row_val in row_sequence:
            current_row = [row_val]
            for col_val in col_sequence:
                binary_string = row_val + col_val
                value_dictionary = dict(zip(self.variables, [int(bit) for bit in binary_string]))
                evaluation_result = self.truth_table.evaluator.evaluate(value_dictionary)
                current_row.append(str(evaluation_result))
            result_map.append(current_row)
        
        return {
            "rows_vars": "".join(row_variables),
            "cols_vars": "".join(col_variables),
            "map": result_map
        }