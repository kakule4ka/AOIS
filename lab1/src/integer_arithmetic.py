from .bit_array import BitArray

class IntegerArithmetic:
    def add_additional(self, operand_a: BitArray, operand_b: BitArray) -> BitArray:
        result = BitArray()
        carry = 0
        for index in range(31, -1, -1):
            total = operand_a.bits[index] + operand_b.bits[index] + carry
            result.bits[index] = total % 2
            carry = total // 2
        return result

    def subtract_additional(self, minuend: BitArray, subtrahend: BitArray) -> BitArray:
        negated_subtrahend = BitArray()
        for index in range(32):
            negated_subtrahend.bits[index] = 1 - subtrahend.bits[index]
        
        carry_unit = 1
        for index in range(31, -1, -1):
            total = negated_subtrahend.bits[index] + carry_unit
            negated_subtrahend.bits[index] = total % 2
            carry_unit = total // 2
            
        return self.add_additional(minuend, negated_subtrahend)

    def multiply_direct(self, factor_a: BitArray, factor_b: BitArray) -> BitArray:
        result = BitArray()
        result.bits[0] = factor_a.bits[0] ^ factor_b.bits[0]
        
        mantissa_a = factor_a.bits[1:]
        mantissa_b = factor_b.bits[1:]
        accumulation_buffer = [0] * 62
        
        for index_b in range(30, -1, -1):
            if mantissa_b[index_b] == 1:
                carry = 0
                for index_a in range(30, -1, -1):
                    position = index_b + index_a + 1
                    total = accumulation_buffer[position] + mantissa_a[index_a] + carry
                    accumulation_buffer[position] = total % 2
                    carry = total // 2
                accumulation_buffer[index_b] += carry
        
        for index in range(31):
            result.bits[1 + index] = accumulation_buffer[31 + index]
            
        return result

    def divide_fixed(self, dividend: BitArray, divisor: BitArray) -> BitArray:
        result = BitArray()
        result.bits[0] = dividend.bits[0] ^ divisor.bits[0]
        
        mantissa_dividend = dividend.bits[1:] + [0] * 17
        mantissa_divisor = divisor.bits[1:]
        remainder_register = [0] * 31
        quotient_collector = []
        
        for bit in mantissa_dividend:
            remainder_register.pop(0)
            remainder_register.append(bit)
            
            is_greater_or_equal = True
            for index in range(31):
                if remainder_register[index] > mantissa_divisor[index]:
                    break
                if remainder_register[index] < mantissa_divisor[index]:
                    is_greater_or_equal = False
                    break
            
            if is_greater_or_equal:
                quotient_collector.append(1)
                borrow = 0
                for index in range(30, -1, -1):
                    difference = remainder_register[index] - mantissa_divisor[index] - borrow
                    if difference < 0:
                        remainder_register[index] = difference + 2
                        borrow = 1
                    else:
                        remainder_register[index] = difference
                        borrow = 0
            else:
                quotient_collector.append(0)
                
        for index in range(31):
            offset = len(quotient_collector) - 31 + index
            if offset >= 0:
                result.bits[1 + index] = quotient_collector[offset]
                
        return result