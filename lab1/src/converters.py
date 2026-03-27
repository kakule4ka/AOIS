from src.bit_array import BitArray

class NumberConverter:
    def decimal_to_direct(self, decimal_value: int) -> BitArray:
        result = BitArray()
        result.bits[0] = 1 if decimal_value < 0 else 0
        absolute_value = abs(int(decimal_value))
        last_index = 31
        
        for i in range(last_index, 0, -1):
            result.bits[i] = absolute_value % 2
            absolute_value //= 2
            
        return result

    def decimal_to_reverse(self, decimal_value: int) -> BitArray:
        result = self.decimal_to_direct(decimal_value)
        total_bits = 32
        
        if decimal_value < 0:
            for i in range(1, total_bits):
                result.bits[i] = 1 - result.bits[i]
                
        return result

    def decimal_to_additional(self, decimal_value: int) -> BitArray:
        min_negative_value = -2147483648
        
        if decimal_value == min_negative_value:
            result = BitArray()
            result.bits[0] = 1
            return result
            
        result = self.decimal_to_reverse(decimal_value)
        last_index = 31
        
        if decimal_value < 0:
            carry = 1
            for i in range(last_index, 0, -1):
                current_sum = result.bits[i] + carry
                result.bits[i] = current_sum % 2
                carry = current_sum // 2
                
        return result

    def direct_to_decimal(self, bit_array: BitArray) -> int:
        decimal_value = 0
        total_bits = 32
        
        for i in range(1, total_bits):
            decimal_value = decimal_value * 2 + bit_array.bits[i]
            
        return -decimal_value if bit_array.bits[0] == 1 else decimal_value

    def additional_to_decimal(self, bit_array: BitArray) -> int:
        total_bits = 32
        last_index = 31
        min_negative_pattern = [1] + [0] * last_index
        min_negative_value = -2147483648
        
        if bit_array.bits == min_negative_pattern:
            return min_negative_value
            
        is_negative = bit_array.bits[0] == 1
        temp_bits = bit_array.bits.copy()
        
        if is_negative:
            borrow = 1
            for i in range(last_index, 0, -1):
                difference = temp_bits[i] - borrow
                if difference < 0:
                    temp_bits[i] = 1
                    borrow = 1
                else:
                    temp_bits[i] = difference
                    borrow = 0
            for i in range(1, total_bits):
                temp_bits[i] = 1 - temp_bits[i]
                
        decimal_value = 0
        for i in range(1, total_bits):
            decimal_value = decimal_value * 2 + temp_bits[i]
            
        return -decimal_value if is_negative else decimal_value

    def decimal_to_fixed(self, float_value: float) -> BitArray:
        result = BitArray()
        result.bits[0] = 1 if float_value < 0 else 0
        absolute_value = abs(float_value)
        
        integer_part = int(absolute_value)
        fractional_part = absolute_value - integer_part
        
        integer_bits_count = 14
        total_bits = 32
        fractional_start_index = integer_bits_count + 1
        
        for i in range(integer_bits_count, 0, -1):
            result.bits[i] = integer_part % 2
            integer_part //= 2
            
        for i in range(fractional_start_index, total_bits):
            fractional_part *= 2
            result.bits[i] = int(fractional_part)
            fractional_part -= int(fractional_part)
            
        return result

    def fixed_to_decimal(self, bit_array: BitArray) -> float:
        integer_part = 0
        integer_bits_count = 14
        total_bits = 32
        fractional_start_index = integer_bits_count + 1
        precision_digits = 5
        
        for i in range(1, integer_bits_count + 1):
            integer_part = integer_part * 2 + bit_array.bits[i]
            
        fractional_part = 0
        for i in range(fractional_start_index, total_bits):
            power = i - integer_bits_count
            fractional_part += bit_array.bits[i] * (2 ** -power)
            
        result_value = round(integer_part + fractional_part, precision_digits)
        return -result_value if bit_array.bits[0] == 1 else result_value