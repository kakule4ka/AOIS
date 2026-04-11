from src.truth_table import TruthTable
from src.normal_forms import NormalForms
from src.minimizer import Minimizer

class CustomEvaluator:
    def __init__(self, variables, evaluate_logic):
        self.variables = variables
        self.evaluate_logic = evaluate_logic

    def evaluate(self, values):
        return self.evaluate_logic(values)

class ODS3Synthesizer:
    def __init__(self):
        self.variables = ['a', 'b', 'c']

    def _evaluate_sum(self, values):
        return values['a'] ^ values['b'] ^ values['c']

    def _evaluate_carry(self, values):
        a, b, c = values['a'], values['b'], values['c']
        return (a & b) | (a & c) | (b & c)

    def synthesize(self):
        sum_eval = CustomEvaluator(self.variables, self._evaluate_sum)
        carry_eval = CustomEvaluator(self.variables, self._evaluate_carry)
        
        st, ct = TruthTable(sum_eval), TruthTable(carry_eval)
        
        return {
            "sum": {"table": st, "sdnf": NormalForms(st).get_sdnf(), "minimized": Minimizer(st).get_calculation_method(True)},
            "carry": {"table": ct, "sdnf": NormalForms(ct).get_sdnf(), "minimized": Minimizer(ct).get_calculation_method(True)}
        }

class FullBCDShiftSynthesizer:
    def __init__(self, shift=6):
        self.variables = ['cin', 's5', 's4', 's2', 's1']
        self.shift = shift
        self.weights = [10, 5, 4, 2, 1]

    def _encode_5421(self, value):
        res = [0, 0, 0, 0]
        temp = value
        if temp >= 5:
            res[0] = 1
            temp -= 5
        if temp >= 4:
            res[1] = 1
            temp -= 4
        if temp >= 2:
            res[2] = 1
            temp -= 2
        if temp >= 1:
            res[3] = 1
        return tuple(res)

    def _create_evaluator(self, output_index):
        def evaluate_logic(values):
            v_in = (values['cin'] * 10 + values['s5'] * 5 + 
                    values['s4'] * 4 + values['s2'] * 2 + values['s1'] * 1)
            
            if v_in > 18: return 0
            
            res_val = v_in + self.shift
            tens, units = res_val // 10, res_val % 10
            
            bits = self._encode_5421(tens) + self._encode_5421(units)
            return bits[output_index]
            
        return CustomEvaluator(self.variables, evaluate_logic)

    def synthesize(self):
        results = {}
        for i in range(8):
            evaluator = self._create_evaluator(i)
            table = TruthTable(evaluator)
            results[f"y{7-i}"] = {
                "table": table,
                "sdnf": NormalForms(table).get_sdnf(),
                "minimized": Minimizer(table).get_calculation_method(True)
            }
        return results

class DownCounterSynthesizer:
    def __init__(self):
        self.variables = ['q2', 'q1', 'q0']

    def _create_t_evaluator(self, index):
        def evaluate_logic(values):
            q = (values['q2'], values['q1'], values['q0'])
            curr = (q[0] << 2) | (q[1] << 1) | q[2]
            nxt = (curr - 1) % 8
            nxt_b = ((nxt >> 2) & 1, (nxt >> 1) & 1, nxt & 1)
            return q[index] ^ nxt_b[index]
        return CustomEvaluator(self.variables, evaluate_logic)

    def synthesize(self):
        results = {}
        for i in range(3):
            table = TruthTable(self._create_t_evaluator(i))
            results[f"T{2-i}"] = {
                "table": table,
                "sdnf": NormalForms(table).get_sdnf(),
                "minimized": Minimizer(table).get_calculation_method(True)
            }
        return results