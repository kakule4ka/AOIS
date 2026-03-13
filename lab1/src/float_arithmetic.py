from src.bit_array import BitArray

class IEEE754Arithmetic:
    def __init__(self):
        pass

    def float_to_bits(self, val: float) -> BitArray:
        res = BitArray()
        if val == 0.0:
            return res
        
        res.bits[0] = 1 if val < 0 else 0
        val = abs(val)
        
        int_part = int(val)
        frac_part = val - int_part
        
        int_bits = []
        while int_part > 0:
            int_bits.append(int_part % 2)
            int_part //= 2
        int_bits.reverse()
        
        frac_bits = []
        while frac_part > 0 and len(frac_bits) < 150:
            frac_part *= 2
            bit = int(frac_part)
            frac_bits.append(bit)
            frac_part -= bit
            
        if len(int_bits) > 0:
            exp = len(int_bits) - 1
            mantissa = int_bits[1:] + frac_bits
        else:
            exp = -1
            for b in frac_bits:
                if b == 1:
                    break
                exp -= 1
            idx = -exp
            mantissa = frac_bits[idx:] if idx < len(frac_bits) else []
            
        exp_stored = exp + 127
        for i in range(8, 0, -1):
            res.bits[i] = exp_stored % 2
            exp_stored //= 2
            
        for i in range(min(23, len(mantissa))):
            res.bits[9 + i] = mantissa[i]
            
        return res

    def bits_to_float(self, bit_array: BitArray) -> float:
        sign = -1 if bit_array.bits[0] == 1 else 1
        
        exp = 0
        for i in range(1, 9):
            exp = exp * 2 + bit_array.bits[i]
            
        if exp == 0:
            return 0.0
            
        exp -= 127
        mantissa = 1.0
        power = 0.5
        for i in range(9, 32):
            mantissa += bit_array.bits[i] * power
            power /= 2.0
            
        return sign * mantissa * (2 ** exp)

    def add(self, a: BitArray, b: BitArray) -> BitArray:
        return self.float_to_bits(self.bits_to_float(a) + self.bits_to_float(b))

    def subtract(self, a: BitArray, b: BitArray) -> BitArray:
        return self.float_to_bits(self.bits_to_float(a) - self.bits_to_float(b))

    def multiply(self, a: BitArray, b: BitArray) -> BitArray:
        return self.float_to_bits(self.bits_to_float(a) * self.bits_to_float(b))

    def divide(self, a: BitArray, b: BitArray) -> BitArray:
        val_b = self.bits_to_float(b)
        if val_b == 0:
            return BitArray()
        return self.float_to_bits(self.bits_to_float(a) / val_b)