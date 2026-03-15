from src.bit_array import BitArray

WORD_SIZE = 32
MAX_BITS_INDEX = WORD_SIZE - 1
MIN_INT32 = -2147483648
FIXED_INT_BITS = 14
FIXED_FRAC_START = 15

class NumberConverter:
    def decimal_to_direct(self, decimal_value: int) -> BitArray:
        result_array = BitArray()
        result_array.bits[0] = 1 if decimal_value < 0 else 0
        absolute_value = abs(int(decimal_value))
        
        for bit_index in range(MAX_BITS_INDEX, 0, -1):
            result_array.bits[bit_index] = absolute_value % 2
            absolute_value //= 2
            
        return result_array

    def decimal_to_reverse(self, decimal_value: int) -> BitArray:
        result_array = self.decimal_to_direct(decimal_value)
        if decimal_value < 0:
            for bit_index in range(1, WORD_SIZE):
                result_array.bits[bit_index] = 1 - result_array.bits[bit_index]
        return result_array

    def decimal_to_additional(self, decimal_value: int) -> BitArray:
        if decimal_value == MIN_INT32:
            result_array = BitArray()
            result_array.bits[0] = 1
            return result_array
            
        result_array = self.decimal_to_reverse(decimal_value)
        if decimal_value < 0:
            carry_bit = 1
            for bit_index in range(MAX_BITS_INDEX, 0, -1):
                temp_sum = result_array.bits[bit_index] + carry_bit
                result_array.bits[bit_index] = temp_sum % 2
                carry_bit = temp_sum // 2
        return result_array

    def direct_to_decimal(self, bit_array: BitArray) -> int:
        decimal_value = 0
        for bit_index in range(1, WORD_SIZE):
            decimal_value = decimal_value * 2 + bit_array.bits[bit_index]
        return -decimal_value if bit_array.bits[0] == 1 else decimal_value

    def additional_to_decimal(self, bit_array: BitArray) -> int:
        if bit_array.bits == [1] + [0] * MAX_BITS_INDEX:
            return MIN_INT32
            
        is_negative = bit_array.bits[0] == 1
        temp_bits = bit_array.bits.copy()
        
        if is_negative:
            borrow_bit = 1
            for bit_index in range(MAX_BITS_INDEX, 0, -1):
                difference = temp_bits[bit_index] - borrow_bit
                if difference < 0:
                    temp_bits[bit_index] = 1
                    borrow_bit = 1
                else:
                    temp_bits[bit_index] = difference
                    borrow_bit = 0
                    
            for bit_index in range(1, WORD_SIZE):
                temp_bits[bit_index] = 1 - temp_bits[bit_index]
                
        decimal_value = 0
        for bit_index in range(1, WORD_SIZE):
            decimal_value = decimal_value * 2 + temp_bits[bit_index]
        return -decimal_value if is_negative else decimal_value

    def decimal_to_fixed(self, float_value: float) -> BitArray:
        result_array = BitArray()
        result_array.bits[0] = 1 if float_value < 0 else 0
        absolute_value = abs(float_value)
        integer_part = int(absolute_value)
        fractional_part = absolute_value - integer_part
        
        for bit_index in range(FIXED_INT_BITS, 0, -1):
            result_array.bits[bit_index] = integer_part % 2
            integer_part //= 2
            
        for bit_index in range(FIXED_FRAC_START, WORD_SIZE):
            fractional_part *= 2
            result_array.bits[bit_index] = int(fractional_part)
            fractional_part -= int(fractional_part)
            
        return result_array

    def fixed_to_decimal(self, bit_array: BitArray) -> float:
        integer_part = 0
        for bit_index in range(1, FIXED_FRAC_START):
            integer_part = integer_part * 2 + bit_array.bits[bit_index]
            
        fractional_part = 0
        for bit_index in range(FIXED_FRAC_START, WORD_SIZE):
            fractional_part += bit_array.bits[bit_index] * (2 ** -(bit_index - FIXED_INT_BITS))
            
        final_result = round(integer_part + fractional_part, 5)
        return -final_result if bit_array.bits[0] == 1 else final_result
