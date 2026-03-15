from src.bit_array import BitArray

WORD_SIZE = 32
MAX_BITS_INDEX = WORD_SIZE - 1
DOUBLE_WORD_SIZE = 62

class IntegerArithmetic:
    def add_additional(self, array_a: BitArray, array_b: BitArray) -> BitArray:
        result_array = BitArray()
        carry_bit = 0
        for bit_index in range(MAX_BITS_INDEX, -1, -1):
            temp_sum = array_a.bits[bit_index] + array_b.bits[bit_index] + carry_bit
            result_array.bits[bit_index] = temp_sum % 2
            carry_bit = temp_sum // 2
        return result_array

    def subtract_additional(self, array_a: BitArray, array_b: BitArray) -> BitArray:
        negated_b = BitArray()
        for bit_index in range(WORD_SIZE):
            negated_b.bits[bit_index] = 1 - array_b.bits[bit_index]
            
        carry_bit = 1
        for bit_index in range(MAX_BITS_INDEX, -1, -1):
            temp_sum = negated_b.bits[bit_index] + carry_bit
            negated_b.bits[bit_index] = temp_sum % 2
            carry_bit = temp_sum // 2
            
        return self.add_additional(array_a, negated_b)

    def multiply_direct(self, array_a: BitArray, array_b: BitArray) -> BitArray:
        result_array = BitArray()
        result_array.bits[0] = array_a.bits[0] ^ array_b.bits[0]
        mantissa_a = array_a.bits[1:]
        mantissa_b = array_b.bits[1:]
        result_mantissa = [0] * DOUBLE_WORD_SIZE
        
        for index_b in range(MAX_BITS_INDEX - 1, -1, -1):
            if mantissa_b[index_b] == 1:
                carry_bit = 0
                for index_a in range(MAX_BITS_INDEX - 1, -1, -1):
                    target_index = index_b + index_a + 1
                    temp_sum = result_mantissa[target_index] + mantissa_a[index_a] + carry_bit
                    result_mantissa[target_index] = temp_sum % 2
                    carry_bit = temp_sum // 2
                result_mantissa[index_b] += carry_bit
                
        for bit_index in range(MAX_BITS_INDEX):
            result_array.bits[1 + bit_index] = result_mantissa[MAX_BITS_INDEX + bit_index]
            
        return result_array

    def divide_fixed(self, array_a: BitArray, array_b: BitArray) -> BitArray:
        result_array = BitArray()
        result_array.bits[0] = array_a.bits[0] ^ array_b.bits[0]
        mantissa_a = array_a.bits[1:] + [0] * 17
        mantissa_b = array_b.bits[1:]
        remainder_bits = [0] * MAX_BITS_INDEX
        quotient_bits = []
        
        for current_bit in mantissa_a:
            remainder_bits.pop(0)
            remainder_bits.append(current_bit)
            is_greater_or_equal = True
            
            for bit_index in range(MAX_BITS_INDEX):
                if remainder_bits[bit_index] > mantissa_b[bit_index]: 
                    break
                if remainder_bits[bit_index] < mantissa_b[bit_index]:
                    is_greater_or_equal = False
                    break
                    
            if is_greater_or_equal:
                quotient_bits.append(1)
                borrow_bit = 0
                for bit_index
