from src.bit_array import BitArray

EXPONENT_BIAS = 127
EXPONENT_BITS = 8
MANTISSA_BITS = 23
MAX_FRAC_ITERATIONS = 150
MANTISSA_START_INDEX = 9
WORD_SIZE = 32

class IEEE754Arithmetic:
    def float_to_bits(self, float_value: float) -> BitArray:
        result_array = BitArray()
        if float_value == 0.0:
            return result_array
            
        result_array.bits[0] = 1 if float_value < 0 else 0
        absolute_value = abs(float_value)
        
        integer_part = int(absolute_value)
        fractional_part = absolute_value - integer_part
        
        integer_bits = []
        while integer_part > 0:
            integer_bits.append(integer_part % 2)
            integer_part //= 2
        integer_bits.reverse()
        
        fractional_bits = []
        while fractional_part > 0 and len(fractional_bits) < MAX_FRAC_ITERATIONS:
            fractional_part *= 2
            bit_value = int(fractional_part)
            fractional_bits.append(bit_value)
            fractional_part -= bit_value
            
        if len(integer_bits) > 0:
            exponent = len(integer_bits) - 1
            mantissa = integer_bits[1:] + fractional_bits
        else:
            exponent = -1
            for bit_value in fractional_bits:
                if bit_value == 1:
                    break
                exponent -= 1
            start_index = -exponent
            mantissa = fractional_bits[start_index:] if start_index < len(fractional_bits) else []
            
        stored_exponent = exponent + EXPONENT_BIAS
        for bit_index in range(EXPONENT_BITS, 0, -1):
            result_array.bits[bit_index] = stored_exponent % 2
            stored_exponent //= 2
            
        for bit_index in range(min(MANTISSA_BITS, len(mantissa))):
            result_array.bits[MANTISSA_START_INDEX + bit_index] = mantissa[bit_index]
            
        return result_array

    def bits_to_float(self, bit_array: BitArray) -> float:
        sign_multiplier = -1 if bit_array.bits[0] == 1 else 1
        
        exponent = 0
        for bit_index in range(1, MANTISSA_START_INDEX):
            exponent = exponent * 2 + bit_array.bits[bit_index]
            
        if exponent == 0:
            return 0.0
            
        exponent -= EXPONENT_BIAS
        mantissa_value = 1.0
        power_fraction = 0.5
        
        for bit_index in range(MANTISSA_START_INDEX, WORD_SIZE):
            mantissa_value += bit_array.bits[bit_index] * power_fraction
            power_fraction /= 2.0
            
        return sign_multiplier * mantissa_value * (2 ** exponent)

    def _extract_components(self, bit_array: BitArray):
        sign = bit_array.bits[0]
        exponent = 0
        for bit_index in range(1, MANTISSA_START_INDEX):
            exponent = exponent * 2 + bit_array.bits[bit_index]
            
        mantissa = [1] + bit_array.bits[MANTISSA_START_INDEX:WORD_SIZE] if exponent > 0 else [0] + bit_array.bits[MANTISSA_START_INDEX:WORD_SIZE]
        return sign, exponent, mantissa

    def _pack_components(self, sign: int, exponent: int, mantissa: list) -> BitArray:
        result_array = BitArray()
        result_array.bits[0] = sign
        for bit_index in range(EXPONENT_BITS, 0, -1):
            result_array.bits[bit_index] = exponent % 2
            exponent //= 2
            
        for bit_index in range(MANTISSA_BITS):
            result_array.bits[MANTISSA_START_INDEX + bit_index] = mantissa[bit_index + 1] if bit_index + 1 < len(mantissa) else 0
            
        return result_array

    def add(self, array_a: BitArray, array_b: BitArray) -> BitArray:
        return self._add_or_subtract(array_a, array_b, is_subtraction=False)

    def subtract(self, array_a: BitArray, array_b: BitArray) -> BitArray:
        return self._add_or_subtract(array_a, array_b, is_subtraction=True)

    def _add_or_subtract(self, array_a: BitArray, array_b: BitArray, is_subtraction: bool) -> BitArray:
        sign_a, exponent_a, mantissa_a = self._extract_components(array_a)
        sign_b, exponent_b, mantissa_b = self._extract_components(array_b)
        
        if is_subtraction:
            sign_b = 1 - sign_b
            
        if exponent_a == 0:
            return self._pack_components(sign_b, exponent_b, mantissa_b)
        if exponent_b == 0:
            return self._pack_components(sign_a, exponent_a, mantissa_a)
            
        if exponent_a < exponent_b:
            sign_a, sign_b = sign_b, sign_a
            exponent_a, exponent_b = exponent_b, exponent_a
            mantissa_a, mantissa_b = mantissa_b, mantissa_a
            
        exponent_diff = exponent_a - exponent_b
        if exponent_diff > MANTISSA_BITS + 1:
            exponent_diff = MANTISSA_BITS + 1
            
        mantissa_b = [0] * exponent_diff + mantissa_b[:(MANTISSA_BITS + 1) - exponent_diff]
        
        result_exponent = exponent_a
        result_mantissa = [0] * (MANTISSA_BITS + 2)
        
        if sign_a == sign_b:
            result_sign = sign_a
            carry_bit = 0
            for bit_index in range(MANTISSA_BITS, -1, -1):
                temp_sum = mantissa_a[bit_index] + mantissa_b[bit_index] + carry_bit
                result_mantissa[bit_index + 1] = temp_sum % 2
                carry_bit = temp_sum // 2
            result_mantissa[0] = carry_bit
            
            if result_mantissa[0] == 1:
                result_exponent += 1
                final_mantissa = result_mantissa[0:MANTISSA_BITS + 1]
            else:
                final_mantissa = result_mantissa[1:MANTISSA_BITS + 2]
        else:
            borrow_bit = 0
            for bit_index in range(MANTISSA_BITS, -1, -1):
                difference = mantissa_a[bit_index] - mantissa_b[bit_index] - borrow_bit
                if difference < 0:
                    result_mantissa[bit_index + 1] = difference + 2
                    borrow_bit = 1
                else:
                    result_mantissa[bit_index + 1] = difference
                    borrow_bit = 0
            result_mantissa[0] = 0
            result_sign = sign_a
            
            if borrow_bit == 1:
                result_sign = sign_b
                carry_twos_comp = 1
                for bit_index in range(MANTISSA_BITS + 1, 0, -1):
                    temp_sum = 1 - result_mantissa[bit_index] + carry_twos_comp
                    result_mantissa[bit_index] = temp_sum % 2
                    carry_twos_comp = temp_sum // 2
                    
            first_one_index = -1
            for bit_index in range(1, MANTISSA_BITS + 2):
                if result_mantissa[bit_index] == 1:
                    first_one_index = bit_index
                    break
                    
            if first_one_index == -1:
                return BitArray()
                
            shift_amount = first_one_index - 1
            result_exponent -= shift_amount
            final_mantissa = result_mantissa[first_one_index:] + [0] * shift_amount
            
        return self._pack_components(result_sign, result_exponent, final_mantissa)

    def multiply(self, array_a: BitArray, array_b: BitArray) -> BitArray:
        sign_a, exponent_a, mantissa_a = self._extract_components(array_a)
        sign_b, exponent_b, mantissa_b = self._extract_components(array_b)
        
        result_sign = sign_a ^ sign_b
        if exponent_a == 0 or exponent_b == 0:
            return self._pack_components(result_sign, 0, [0] * (MANTISSA_BITS + 1))
            
        result_exponent = exponent_a + exponent_b - EXPONENT_BIAS
        result_mantissa = [0] * ((MANTISSA_BITS + 1) * 2)
        
        for index_b in range(MANTISSA_BITS, -1, -1):
            if mantissa_b[index_b] == 1:
                carry_bit = 0
                for index_a in range(MANTISSA_BITS, -1, -1):
                    target_index = index_b + index_a + 1
                    temp_sum = result_mantissa[target_index] + mantissa_a[index_a] + carry_bit
                    result_mantissa[target_index] = temp_sum % 2
                    carry_bit = temp_sum // 2
                result_mantissa[index_b] += carry_bit
                
        if result_mantissa[0] == 1:
            result_exponent += 1
            final_mantissa = result_mantissa[0:MANTISSA_BITS + 1]
        else:
            final_mantissa = result_mantissa[1:MANTISSA_BITS + 2]
            
        return self._pack_components(result_sign, result_exponent, final_mantissa)

    def divide(self, array_a: BitArray, array_b: BitArray) -> BitArray:
        sign_a, exponent_a, mantissa_a = self._extract_components(array_a)
        sign_b, exponent_b, mantissa_b = self._extract_components(array_b)
        
        result_sign = sign_a ^ sign_b
        if exponent_b == 0:
            return BitArray()
        if exponent_a == 0:
            return self._pack_components(result_sign, 0, [0] * (MANTISSA_BITS + 1))
            
        result_exponent = exponent_a - exponent_b + EXPONENT_BIAS
        remainder_bits = mantissa_a + [0] * (MANTISSA_BITS + 2)
        quotient_bits = []
        
        for _ in range(MANTISSA_BITS + 2):
            is_greater_or_equal = True
            for bit_index in range(MANTISSA_BITS + 1):
                if remainder_bits[bit_index] > mantissa_b[bit_index]:
                    break
                if remainder_bits[bit_index] < mantissa_b[bit_index]:
                    is_greater_or_equal = False
                    break
                    
            if is_greater_or_equal:
                quotient_bits.append(1)
                borrow_bit = 0
                for bit_index in range(MANTISSA_BITS, -1, -1):
                    difference = remainder_bits[bit_index] - mantissa_b[bit_index] - borrow_bit
                    if difference < 0:
                        remainder_bits[bit_index] = difference + 2
                        borrow_bit = 1
                    else:
                        remainder_bits[bit_index] = difference
                        borrow_bit = 0
            else:
                quotient_bits.append(0)
                
            remainder_bits.pop(0)
            remainder_bits.append(0)
            
        if quotient_bits[0] == 1:
            final_mantissa = quotient_bits[0:MANTISSA_BITS + 1]
        else:
            result_exponent -= 1
            final_mantissa = quotient_bits[1:MANTISSA_BITS + 2]
            
        return self._pack_components(result_sign, result_exponent, final_mantissa)
