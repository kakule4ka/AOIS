from .bit_array import BitArray

class IEEE754Arithmetic:
    EXPONENT_BIAS = 127
    EXPONENT_BITS = 8
    MANTISSA_BITS = 23
    MANTISSA_HIDDEN_LEN = 24
    MANTISSA_START = 9
    TOTAL_BITS = 32

    def float_to_bits(self, value: float) -> BitArray:
        result = BitArray()
        if value == 0.0:
            return result
            
        result.bits[0] = 1 if value < 0 else 0
        absolute_value = abs(value)
        
        integer_part = int(absolute_value)
        fractional_part = absolute_value - integer_part
        
        int_binary = []
        while integer_part > 0:
            int_binary.append(integer_part % 2)
            integer_part //= 2
        int_binary.reverse()
        
        frac_binary = []
        while fractional_part > 0 and len(frac_binary) < 150:
            fractional_part *= 2
            bit = int(fractional_part)
            frac_binary.append(bit)
            fractional_part -= bit
            
        if int_binary:
            exponent = len(int_binary) - 1
            combined_mantissa = int_binary[1:] + frac_binary
        else:
            exponent = -1
            for bit in frac_binary:
                if bit == 1:
                    break
                exponent -= 1
            normalization_shift = -exponent
            combined_mantissa = frac_binary[normalization_shift:] if normalization_shift < len(frac_binary) else []
            
        biased_exponent = exponent + self.EXPONENT_BIAS
        for index in range(self.EXPONENT_BITS, 0, -1):
            result.bits[index] = biased_exponent % 2
            biased_exponent //= 2
            
        for index in range(min(self.MANTISSA_BITS, len(combined_mantissa))):
            result.bits[self.MANTISSA_START + index] = combined_mantissa[index]
            
        return result

    def bits_to_float(self, bit_array: BitArray) -> float:
        sign_factor = -1 if bit_array.bits[0] == 1 else 1
        
        exponent_value = 0
        for index in range(1, self.EXPONENT_BITS + 1):
            exponent_value = exponent_value * 2 + bit_array.bits[index]
            
        if exponent_value == 0:
            return 0.0
            
        unbiased_exponent = exponent_value - self.EXPONENT_BIAS
        mantissa_sum = 1.0
        weight = 0.5
        for index in range(self.MANTISSA_START, self.TOTAL_BITS):
            mantissa_sum += bit_array.bits[index] * weight
            weight /= 2.0
            
        return sign_factor * mantissa_sum * (2 ** unbiased_exponent)

    def _extract_components(self, bit_array: BitArray):
        sign = bit_array.bits[0]
        exponent = 0
        for index in range(1, self.EXPONENT_BITS + 1):
            exponent = exponent * 2 + bit_array.bits[index]
        
        if exponent > 0:
            mantissa = [1] + bit_array.bits[self.MANTISSA_START:self.TOTAL_BITS]
        else:
            mantissa = [0] + bit_array.bits[self.MANTISSA_START:self.TOTAL_BITS]
            
        return sign, exponent, mantissa

    def _construct_bit_array(self, sign: int, exponent: int, mantissa: list) -> BitArray:
        result = BitArray()
        result.bits[0] = sign
        for index in range(self.EXPONENT_BITS, 0, -1):
            result.bits[index] = exponent % 2
            exponent //= 2
        for index in range(self.MANTISSA_BITS):
            if index + 1 < len(mantissa):
                result.bits[self.MANTISSA_START + index] = mantissa[index + 1]
        return result

    def add(self, operand_a: BitArray, operand_b: BitArray) -> BitArray:
        return self._perform_operation(operand_a, operand_b, False)

    def subtract(self, operand_a: BitArray, operand_b: BitArray) -> BitArray:
        return self._perform_operation(operand_a, operand_b, True)

    def _perform_operation(self, a: BitArray, b: BitArray, is_sub: bool) -> BitArray:
        s1, e1, m1 = self._extract_components(a)
        s2, e2, m2 = self._extract_components(b)
        
        if is_sub:
            s2 = 1 - s2
            
        if e1 == 0: 
            return self._construct_bit_array(s2, e2, m2)
        if e2 == 0: 
            return self._construct_bit_array(s1, e1, m1)
        
        if e1 < e2:
            s1, s2 = s2, s1
            e1, e2 = e2, e1
            m1, m2 = m2, m1
            
        diff = e1 - e2
        if diff > self.MANTISSA_HIDDEN_LEN:
            diff = self.MANTISSA_HIDDEN_LEN
            
        aligned_m2 = [0] * diff + m2[:self.MANTISSA_HIDDEN_LEN - diff]
        
        res_exponent = e1
        working_mantissa = [0] * (self.MANTISSA_HIDDEN_LEN + 1)
        
        if s1 == s2:
            res_sign = s1
            carry = 0
            for index in range(self.MANTISSA_HIDDEN_LEN - 1, -1, -1):
                total = m1[index] + aligned_m2[index] + carry
                working_mantissa[index + 1] = total % 2
                carry = total // 2
            working_mantissa[0] = carry
            
            if working_mantissa[0] == 1:
                res_exponent += 1
                final_mantissa = working_mantissa[0:self.MANTISSA_HIDDEN_LEN]
            else:
                final_mantissa = working_mantissa[1:self.MANTISSA_HIDDEN_LEN + 1]
        else:
            res_sign = s1
            borrow = 0
            for index in range(self.MANTISSA_HIDDEN_LEN - 1, -1, -1):
                delta = m1[index] - aligned_m2[index] - borrow
                if delta < 0:
                    working_mantissa[index + 1] = delta + 2
                    borrow = 1
                else:
                    working_mantissa[index + 1] = delta
                    borrow = 0
            
            first_bit = -1
            for index in range(1, self.MANTISSA_HIDDEN_LEN + 1):
                if working_mantissa[index] == 1:
                    first_bit = index
                    break
            
            if first_bit == -1: 
                return BitArray()
            
            shift = first_bit - 1
            res_exponent -= shift
            final_mantissa = working_mantissa[first_bit:] + [0] * shift
            
        return self._construct_bit_array(res_sign, res_exponent, final_mantissa)

    def multiply(self, a: BitArray, b: BitArray) -> BitArray:
        s1, e1, m1 = self._extract_components(a)
        s2, e2, m2 = self._extract_components(b)
        
        res_sign = s1 ^ s2
        if e1 == 0 or e2 == 0:
            return self._construct_bit_array(res_sign, 0, [0] * self.MANTISSA_HIDDEN_LEN)
            
        res_exponent = e1 + e2 - self.EXPONENT_BIAS
        buffer = [0] * (self.MANTISSA_HIDDEN_LEN * 2)
        
        for index_b in range(self.MANTISSA_HIDDEN_LEN - 1, -1, -1):
            if m2[index_b] == 1:
                carry = 0
                for index_a in range(self.MANTISSA_HIDDEN_LEN - 1, -1, -1):
                    pos = index_b + index_a + 1
                    total = buffer[pos] + m1[index_a] + carry
                    buffer[pos] = total % 2
                    carry = total // 2
                buffer[index_b] += carry
                
        if buffer[0] == 1:
            res_exponent += 1
            final_mantissa = buffer[0:self.MANTISSA_HIDDEN_LEN]
        else:
            final_mantissa = buffer[1:self.MANTISSA_HIDDEN_LEN + 1]
            
        return self._construct_bit_array(res_sign, res_exponent, final_mantissa)

    def divide(self, a: BitArray, b: BitArray) -> BitArray:
        s1, e1, m1 = self._extract_components(a)
        s2, e2, m2 = self._extract_components(b)
        
        res_sign = s1 ^ s2
        if e2 == 0: 
            return BitArray()
        if e1 == 0: 
            return self._construct_bit_array(res_sign, 0, [0] * self.MANTISSA_HIDDEN_LEN)
        
        res_exponent = e1 - e2 + self.EXPONENT_BIAS
        register_len = self.MANTISSA_HIDDEN_LEN + 1
        remainder = m1 + [0] * register_len
        quotient = []
        
        for _ in range(register_len):
            ge = True
            for index in range(self.MANTISSA_HIDDEN_LEN):
                if remainder[index] > m2[index]: 
                    break
                if remainder[index] < m2[index]:
                    ge = False
                    break
            
            if ge:
                quotient.append(1)
                borrow = 0
                for index in range(self.MANTISSA_HIDDEN_LEN - 1, -1, -1):
                    delta = remainder[index] - m2[index] - borrow
                    if delta < 0:
                        remainder[index] = delta + 2
                        borrow = 1
                    else:
                        remainder[index] = delta
                        borrow = 0
            else:
                quotient.append(0)
            remainder.pop(0)
            remainder.append(0)
            
        if quotient[0] == 1:
            final_mantissa = quotient[0:self.MANTISSA_HIDDEN_LEN]
        else:
            res_exponent -= 1
            final_mantissa = quotient[1:register_len]
            
        return self._construct_bit_array(res_sign, res_exponent, final_mantissa)