from src.bit_array import BitArray

class NumberConverter:
    BIT_LIMIT = 32
    SIGN_INDEX = 0
    INTEGER_PART_LIMIT = 14

    def decimal_to_direct(self, decimal_value: int) -> BitArray:
        result = BitArray()
        result.bits[self.SIGN_INDEX] = 1 if decimal_value < 0 else 0
        absolute_value = abs(int(decimal_value))
        
        for index in range(self.BIT_LIMIT - 1, 0, -1):
            result.bits[index] = absolute_value % 2
            absolute_value //= 2
            
        return result

    def decimal_to_reverse(self, decimal_value: int) -> BitArray:
        result = self.decimal_to_direct(decimal_value)
        
        if decimal_value < 0:
            for index in range(1, self.BIT_LIMIT):
                result.bits[index] = 1 - result.bits[index]
                
        return result

    def decimal_to_additional(self, decimal_value: int) -> BitArray:
        min_int_32 = -2147483648
        
        if decimal_value == min_int_32:
            result = BitArray()
            result.bits[self.SIGN_INDEX] = 1
            return result
            
        result = self.decimal_to_reverse(decimal_value)
        
        if decimal_value < 0:
            carry = 1
            for index in range(self.BIT_LIMIT - 1, 0, -1):
                current_sum = result.bits[index] + carry
                result.bits[index] = current_sum % 2
                carry = current_sum // 2
                
        return result

    def direct_to_decimal(self, bit_array: BitArray) -> int:
        decimal_magnitude = 0
        
        for index in range(1, self.BIT_LIMIT):
            decimal_magnitude = decimal_magnitude * 2 + bit_array.bits[index]
            
        return -decimal_magnitude if bit_array.bits[self.SIGN_INDEX] == 1 else decimal_magnitude

    def additional_to_decimal(self, bit_array: BitArray) -> int:
        min_pattern = [1] + [0] * 31
        if bit_array.bits == min_pattern:
            return -2147483648
            
        is_negative = bit_array.bits[self.SIGN_INDEX] == 1
        bits_working_copy = bit_array.bits.copy()
        
        if is_negative:
            borrow = 1
            for index in range(self.BIT_LIMIT - 1, 0, -1):
                difference = bits_working_copy[index] - borrow
                if difference < 0:
                    bits_working_copy[index] = 1
                    borrow = 1
                else:
                    bits_working_copy[index] = difference
                    borrow = 0
            for index in range(1, self.BIT_LIMIT):
                bits_working_copy[index] = 1 - bits_working_copy[index]
                
        decimal_value = 0
        for index in range(1, self.BIT_LIMIT):
            decimal_value = decimal_value * 2 + bits_working_copy[index]
            
        return -decimal_value if is_negative else decimal_value

    def decimal_to_fixed(self, float_value: float) -> BitArray:
        result = BitArray()
        result.bits[self.SIGN_INDEX] = 1 if float_value < 0 else 0
        absolute_value = abs(float_value)
        
        integer_part = int(absolute_value)
        fractional_part = absolute_value - integer_part
        
        fractional_start_index = self.INTEGER_PART_LIMIT + 1
        
        for index in range(self.INTEGER_PART_LIMIT, 0, -1):
            result.bits[index] = integer_part % 2
            integer_part //= 2
            
        for index in range(fractional_start_index, self.BIT_LIMIT):
            fractional_part *= 2
            result.bits[index] = int(fractional_part)
            fractional_part -= int(fractional_part)
            
        return result

    def fixed_to_decimal(self, bit_array: BitArray) -> float:
        integer_accumulator = 0
        fractional_accumulator = 0
        fractional_start_index = self.INTEGER_PART_LIMIT + 1
        
        for index in range(1, self.INTEGER_PART_LIMIT + 1):
            integer_accumulator = integer_accumulator * 2 + bit_array.bits[index]
            
        for index in range(fractional_start_index, self.BIT_LIMIT):
            exponent = index - self.INTEGER_PART_LIMIT
            fractional_accumulator += bit_array.bits[index] * (2 ** -exponent)
            
        result_value = round(integer_accumulator + fractional_accumulator, 5)
        return -result_value if bit_array.bits[self.SIGN_INDEX] == 1 else result_value