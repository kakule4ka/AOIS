from src.bit_array import BitArray

class IEEE754Arithmetic:
    EXPONENT_BIAS = 127
    EXPONENT_LENGTH = 8
    MANTISSA_LENGTH = 23
    MANTISSA_FULL_LENGTH = 24
    MANTISSA_START_IDX = 9
    TOTAL_BITS = 32
    MAX_FRACTION_BITS = 150

    def float_to_bits(self, value: float) -> BitArray:
        result = BitArray()
        if value == 0.0:
            return result
            
        result.bits[0] = 1 if value < 0 else 0
        value = abs(value)
        
        integer_part = int(value)
        fractional_part = value - integer_part
        
        integer_bits = []
        while integer_part > 0:
            integer_bits.append(integer_part % 2)
            integer_part //= 2
        integer_bits.reverse()
        
        fractional_bits = []
        while fractional_part > 0 and len(fractional_bits) < self.MAX_FRACTION_BITS:
            fractional_part *= 2
            bit = int(fractional_part)
            fractional_bits.append(bit)
            fractional_part -= bit
            
        if len(integer_bits) > 0:
            exponent = len(integer_bits) - 1
            mantissa = integer_bits[1:] + fractional_bits
        else:
            exponent = -1
            for b in fractional_bits:
                if b == 1:
                    break
                exponent -= 1
            first_one_index = -exponent
            mantissa = fractional_bits[first_one_index:] if first_one_index < len(fractional_bits) else []
            
        stored_exponent = exponent + self.EXPONENT_BIAS
        for i in range(self.EXPONENT_LENGTH, 0, -1):
            result.bits[i] = stored_exponent % 2
            stored_exponent //= 2
            
        for i in range(min(self.MANTISSA_LENGTH, len(mantissa))):
            result.bits[self.MANTISSA_START_IDX + i] = mantissa[i]
            
        return result

    def bits_to_float(self, bit_array: BitArray) -> float:
        sign = -1 if bit_array.bits[0] == 1 else 1
        
        exponent = 0
        for i in range(1, self.EXPONENT_LENGTH + 1):
            exponent = exponent * 2 + bit_array.bits[i]
            
        if exponent == 0:
            return 0.0
            
        exponent -= self.EXPONENT_BIAS
        mantissa = 1.0
        power = 0.5
        for i in range(self.MANTISSA_START_IDX, self.TOTAL_BITS):
            mantissa += bit_array.bits[i] * power
            power /= 2.0
            
        return sign * mantissa * (2 ** exponent)

    def _extract(self, bit_array: BitArray):
        sign = bit_array.bits[0]
        exponent = 0
        for i in range(1, self.EXPONENT_LENGTH + 1):
            exponent = exponent * 2 + bit_array.bits[i]
        mantissa = [1] + bit_array.bits[self.MANTISSA_START_IDX:self.TOTAL_BITS] if exponent > 0 else [0] + bit_array.bits[self.MANTISSA_START_IDX:self.TOTAL_BITS]
        return sign, exponent, mantissa

    def _pack(self, sign: int, exponent: int, mantissa: list) -> BitArray:
        result = BitArray()
        result.bits[0] = sign
        for i in range(self.EXPONENT_LENGTH, 0, -1):
            result.bits[i] = exponent % 2
            exponent //= 2
        for i in range(self.MANTISSA_LENGTH):
            result.bits[self.MANTISSA_START_IDX + i] = mantissa[i + 1] if i + 1 < len(mantissa) else 0
        return result

    def add(self, a: BitArray, b: BitArray) -> BitArray:
        return self._add_sub(a, b, False)

    def subtract(self, a: BitArray, b: BitArray) -> BitArray:
        return self._add_sub(a, b, True)

    def _add_sub(self, a: BitArray, b: BitArray, is_subtract: bool) -> BitArray:
        sign1, exponent1, mantissa1 = self._extract(a)
        sign2, exponent2, mantissa2 = self._extract(b)
        
        if is_subtract:
            sign2 = 1 - sign2
            
        if exponent1 == 0:
            return self._pack(sign2, exponent2, mantissa2)
        if exponent2 == 0:
            return self._pack(sign1, exponent1, mantissa1)
            
        if exponent1 < exponent2:
            sign1, sign2 = sign2, sign1
            exponent1, exponent2 = exponent2, exponent1
            mantissa1, mantissa2 = mantissa2, mantissa1
            
        exponent_diff = exponent1 - exponent2
        if exponent_diff > self.MANTISSA_FULL_LENGTH:
            exponent_diff = self.MANTISSA_FULL_LENGTH
        mantissa2 = [0] * exponent_diff + mantissa2[:self.MANTISSA_FULL_LENGTH - exponent_diff]
        
        result_exponent = exponent1
        result_mantissa_buffer = [0] * (self.MANTISSA_FULL_LENGTH + 1)
        
        if sign1 == sign2:
            result_sign = sign1
            carry = 0
            for i in range(self.MANTISSA_LENGTH, -1, -1):
                bit_sum = mantissa1[i] + mantissa2[i] + carry
                result_mantissa_buffer[i + 1] = bit_sum % 2
                carry = bit_sum // 2
            result_mantissa_buffer[0] = carry
            
            if result_mantissa_buffer[0] == 1:
                result_exponent += 1
                result_mantissa = result_mantissa_buffer[0:self.MANTISSA_FULL_LENGTH]
            else:
                result_mantissa = result_mantissa_buffer[1:self.MANTISSA_FULL_LENGTH + 1]
        else:
            borrow = 0
            for i in range(self.MANTISSA_LENGTH, -1, -1):
                bit_diff = mantissa1[i] - mantissa2[i] - borrow
                if bit_diff < 0:
                    result_mantissa_buffer[i + 1] = bit_diff + 2
                    borrow = 1
                else:
                    result_mantissa_buffer[i + 1] = bit_diff
                    borrow = 0
            result_mantissa_buffer[0] = 0
            result_sign = sign1
            
            if borrow == 1:
                result_sign = sign2
                twos_complement_carry = 1
                for i in range(self.MANTISSA_FULL_LENGTH, 0, -1):
                    bit_sum = 1 - result_mantissa_buffer[i] + twos_complement_carry
                    result_mantissa_buffer[i] = bit_sum % 2
                    twos_complement_carry = bit_sum // 2
                    
            first_one_index = -1
            for i in range(1, self.MANTISSA_FULL_LENGTH + 1):
                if result_mantissa_buffer[i] == 1:
                    first_one_index = i
                    break
                    
            if first_one_index == -1:
                return BitArray()
                
            shift_amount = first_one_index - 1
            result_exponent -= shift_amount
            result_mantissa = result_mantissa_buffer[first_one_index:] + [0] * shift_amount
            
        return self._pack(result_sign, result_exponent, result_mantissa)

    def multiply(self, a: BitArray, b: BitArray) -> BitArray:
        sign1, exponent1, mantissa1 = self._extract(a)
        sign2, exponent2, mantissa2 = self._extract(b)
        
        result_sign = sign1 ^ sign2
        if exponent1 == 0 or exponent2 == 0:
            return self._pack(result_sign, 0, [0] * self.MANTISSA_FULL_LENGTH)
            
        result_exponent = exponent1 + exponent2 - self.EXPONENT_BIAS
        result_mantissa_buffer = [0] * (self.MANTISSA_FULL_LENGTH * 2)
        
        for i in range(self.MANTISSA_LENGTH, -1, -1):
            if mantissa2[i] == 1:
                carry = 0
                for j in range(self.MANTISSA_LENGTH, -1, -1):
                    bit_sum = result_mantissa_buffer[i + j + 1] + mantissa1[j] + carry
                    result_mantissa_buffer[i + j + 1] = bit_sum % 2
                    carry = bit_sum // 2
                result_mantissa_buffer[i] += carry
                
        if result_mantissa_buffer[0] == 1:
            result_exponent += 1
            result_mantissa = result_mantissa_buffer[0:self.MANTISSA_FULL_LENGTH]
        else:
            result_mantissa = result_mantissa_buffer[1:self.MANTISSA_FULL_LENGTH + 1]
            
        return self._pack(result_sign, result_exponent, result_mantissa)

    def divide(self, a: BitArray, b: BitArray) -> BitArray:
        sign1, exponent1, mantissa1 = self._extract(a)
        sign2, exponent2, mantissa2 = self._extract(b)
        
        result_sign = sign1 ^ sign2
        if exponent2 == 0:
            return BitArray()
        if exponent1 == 0:
            return self._pack(result_sign, 0, [0] * self.MANTISSA_FULL_LENGTH)
            
        result_exponent = exponent1 - exponent2 + self.EXPONENT_BIAS
        buffer_length = self.MANTISSA_FULL_LENGTH + 1
        remainder = mantissa1 + [0] * buffer_length
        quotient_bits = []
        
        for _ in range(buffer_length):
            is_greater_or_equal = True
            for i in range(self.MANTISSA_FULL_LENGTH):
                if remainder[i] > mantissa2[i]:
                    break
                if remainder[i] < mantissa2[i]:
                    is_greater_or_equal = False
                    break
                    
            if is_greater_or_equal:
                quotient_bits.append(1)
                borrow = 0
                for i in range(self.MANTISSA_LENGTH, -1, -1):
                    bit_diff = remainder[i] - mantissa2[i] - borrow
                    if bit_diff < 0:
                        remainder[i] = bit_diff + 2
                        borrow = 1
                    else:
                        remainder[i] = bit_diff
                        borrow = 0
            else:
                quotient_bits.append(0)
            remainder.pop(0)
            remainder.append(0)
            
        if quotient_bits[0] == 1:
            result_mantissa = quotient_bits[0:self.MANTISSA_FULL_LENGTH]
        else:
            result_exponent -= 1
            result_mantissa = quotient_bits[1:buffer_length]
            
        return self._pack(result_sign, result_exponent, result_mantissa)