from src.bit_array import BitArray

class Excess3BCDArithmetic:
    TOTAL_BITS = 32
    NUM_DIGITS = 7
    BITS_PER_DIGIT = 4
    EXCESS = 3
    
    # 1 sign bit, 3 unused bits, 7 digits * 4 bits/digit = 28 bits.
    # Total = 1 + 3 + 28 = 32.
    LAST_BIT_INDEX = TOTAL_BITS - 1
    FIRST_DIGIT_BIT_INDEX = TOTAL_BITS - (NUM_DIGITS * BITS_PER_DIGIT)

    def decimal_to_excess3(self, value: int) -> BitArray:
        result = BitArray()
        result.bits[0] = 1 if value < 0 else 0
        
        value_string = str(abs(value)).zfill(self.NUM_DIGITS)
        current_bit_index = self.LAST_BIT_INDEX
        
        for digit_char in reversed(value_string):
            digit = int(digit_char) + self.EXCESS
            for _ in range(self.BITS_PER_DIGIT):
                result.bits[current_bit_index] = digit % 2
                digit //= 2
                current_bit_index -= 1
                
        return result

    def excess3_to_decimal(self, bcd_array: BitArray) -> int:
        decimal_string = ""
        for i in range(self.LAST_BIT_INDEX, self.FIRST_DIGIT_BIT_INDEX - 1, -self.BITS_PER_DIGIT):
            group_start_index = i - self.BITS_PER_DIGIT + 1
            digit_group = bcd_array.bits[group_start_index : i + 1]
            
            digit_value = 0
            for bit in digit_group:
                digit_value = digit_value * 2 + bit

            if digit_value >= self.EXCESS:
                decimal_string = str(digit_value - self.EXCESS) + decimal_string
                
        result_value = int(decimal_string) if decimal_string else 0
        is_negative = bcd_array.bits[0] == 1
        return -result_value if is_negative else result_value

    def add(self, a: BitArray, b: BitArray) -> BitArray:
        # This implementation assumes addition of two positive numbers.
        # The sign is just copied from the first operand.
        result = BitArray()
        inter_digit_carry = 0
        
        correction_add = [0, 0, 1, 1]  # Binary for +3
        correction_subtract = [1, 1, 0, 1] # Binary for -3 (via +13 in 4-bit)
        
        for i in range(self.LAST_BIT_INDEX, self.FIRST_DIGIT_BIT_INDEX - 1, -self.BITS_PER_DIGIT):
            group_start_index = i - self.BITS_PER_DIGIT + 1
            group_a = a.bits[group_start_index : i + 1]
            group_b = b.bits[group_start_index : i + 1]
            
            sum_group = [0] * self.BITS_PER_DIGIT
            intra_digit_carry = inter_digit_carry
            
            # Add the two 4-bit groups
            for j in range(self.BITS_PER_DIGIT - 1, -1, -1):
                bit_sum = group_a[j] + group_b[j] + intra_digit_carry
                sum_group[j] = bit_sum % 2
                intra_digit_carry = bit_sum // 2
            
            # Apply correction based on carry-out
            correction_carry = 0
            if intra_digit_carry == 1:
                correction = correction_add
                inter_digit_carry = 1
            else:
                correction = correction_subtract
                inter_digit_carry = 0

            for j in range(self.BITS_PER_DIGIT - 1, -1, -1):
                bit_sum = sum_group[j] + correction[j] + correction_carry
                result.bits[group_start_index + j] = bit_sum % 2
                correction_carry = bit_sum // 2
        
        result.bits[0] = a.bits[0]
        return result