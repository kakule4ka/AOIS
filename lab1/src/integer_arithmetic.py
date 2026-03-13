from src.bit_array import BitArray
from src.converters import NumberConverter

class IntegerArithmetic:
    def __init__(self):
        self.converter = NumberConverter()

    def add_additional(self, a: BitArray, b: BitArray) -> BitArray:
        result = BitArray()
        carry = 0
        for i in range(31, -1, -1):
            total = a.bits[i] + b.bits[i] + carry
            result.bits[i] = total % 2
            carry = total // 2
        return result

    def subtract_additional(self, a: BitArray, b: BitArray) -> BitArray:
        neg_b = BitArray()
        neg_b.bits[0] = 1 if b.bits[0] == 0 else 0
        for i in range(1, 32):
            neg_b.bits[i] = 1 if b.bits[i] == 0 else 0
        
        carry = 1
        for i in range(31, 0, -1):
            total = neg_b.bits[i] + carry
            neg_b.bits[i] = total % 2
            carry = total // 2

        return self.add_additional(a, neg_b)

    def multiply_direct(self, a: BitArray, b: BitArray) -> BitArray:
        result = BitArray()
        result.bits[0] = a.bits[0] ^ b.bits[0]
        
        for i in range(31, 0, -1):
            if b.bits[i] == 1:
                shift = 31 - i
                temp_add = BitArray()
                for j in range(31, shift, -1):
                    temp_add.bits[j - shift] = a.bits[j]
                
                carry = 0
                for k in range(31, 0, -1):
                    total = result.bits[k] + temp_add.bits[k] + carry
                    result.bits[k] = total % 2
                    carry = total // 2
                    
        return result

    def divide_direct(self, a: BitArray, b: BitArray) -> BitArray:
        result = BitArray()
        result.bits[0] = a.bits[0] ^ b.bits[0]
        
        div1 = 0
        div2 = 0
        for i in range(1, 32):
            div1 = div1 * 2 + a.bits[i]
            div2 = div2 * 2 + b.bits[i]

        if div2 == 0:
            return result

        quotient = div1 // div2
        remainder = div1 % div2
        
        q_bits = []
        while quotient > 0:
            q_bits.append(quotient % 2)
            quotient //= 2
            
        idx = 16
        for bit in q_bits:
            if idx > 0:
                result.bits[idx] = bit
                idx -= 1
                
        rem_idx = 17
        for _ in range(5):
            remainder *= 2
            result.bits[rem_idx] = remainder // div2
            remainder %= div2
            rem_idx += 1
            
        return result