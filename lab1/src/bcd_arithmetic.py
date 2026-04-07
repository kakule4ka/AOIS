from .bit_array import BitArray

class Excess3BCDArithmetic:
    BIT_LIMIT = 32
    DIGIT_COUNT = 7
    BITS_PER_UNIT = 4
    OFFSET = 3

    def decimal_to_excess3(self, value: int) -> BitArray:
        result = BitArray()
        result.bits[0] = 1 if value < 0 else 0
        
        numeric_string = str(abs(value)).zfill(self.DIGIT_COUNT)
        bit_pointer = self.BIT_LIMIT - 1
        
        for char in reversed(numeric_string):
            digit_plus_offset = int(char) + self.OFFSET
            for _ in range(self.BITS_PER_UNIT):
                result.bits[bit_pointer] = digit_plus_offset % 2
                digit_plus_offset //= 2
                bit_pointer -= 1
                
        return result

    def excess3_to_decimal(self, bit_array: BitArray) -> int:
        digits_collector = ""
        start_bit = self.BIT_LIMIT - (self.DIGIT_COUNT * self.BITS_PER_UNIT)
        
        for index in range(self.BIT_LIMIT - 1, start_bit - 1, -self.BITS_PER_UNIT):
            group_base = index - self.BITS_PER_UNIT + 1
            bits_group = bit_array.bits[group_base : index + 1]
            
            value = 0
            for bit in bits_group:
                value = value * 2 + bit

            if value >= self.OFFSET:
                digits_collector = str(value - self.OFFSET) + digits_collector
                
        final_int = int(digits_collector) if digits_collector else 0
        return -final_int if bit_array.bits[0] == 1 else final_int

    def add(self, operand_a: BitArray, operand_b: BitArray) -> BitArray:
        result = BitArray()
        external_carry = 0
        
        correction_pos = [0, 0, 1, 1]
        correction_neg = [1, 1, 0, 1]
        
        limit_bit = self.BIT_LIMIT - (self.DIGIT_COUNT * self.BITS_PER_UNIT)
        
        for index in range(self.BIT_LIMIT - 1, limit_bit - 1, -self.BITS_PER_UNIT):
            base = index - self.BITS_PER_UNIT + 1
            slice_a = operand_a.bits[base : index + 1]
            slice_b = operand_b.bits[base : index + 1]
            
            inter_sum = [0] * self.BITS_PER_UNIT
            internal_carry = external_carry
            
            for j in range(self.BITS_PER_UNIT - 1, -1, -1):
                sum_bits = slice_a[j] + slice_b[j] + internal_carry
                inter_sum[j] = sum_bits % 2
                internal_carry = sum_bits // 2

            if internal_carry == 1:
                correction = correction_pos
                external_carry = 1
            else:
                correction = correction_neg
                external_carry = 0

            step_carry = 0
            for j in range(self.BITS_PER_UNIT - 1, -1, -1):
                final_bits_sum = inter_sum[j] + correction[j] + step_carry
                result.bits[base + j] = final_bits_sum % 2
                step_carry = final_bits_sum // 2
        
        result.bits[0] = operand_a.bits[0]
        return result