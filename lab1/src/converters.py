from src.bit_array import BitArray

class NumberConverter:
    def decimal_to_direct(self, val: int) -> BitArray:
        b = BitArray()
        b.bits[0] = 1 if val < 0 else 0
        temp = abs(int(val))
        for i in range(31, 0, -1):
            b.bits[i] = temp % 2
            temp //= 2
        return b

    def decimal_to_reverse(self, val: int) -> BitArray:
        b = self.decimal_to_direct(val)
        if val < 0:
            for i in range(1, 32):
                b.bits[i] = 1 - b.bits[i]
        return b

    def decimal_to_additional(self, val: int) -> BitArray:
        if val == -2147483648:
            b = BitArray()
            b.bits[0] = 1
            return b
            
        b = self.decimal_to_reverse(val)
        if val < 0:
            c = 1
            for i in range(31, 0, -1):
                t = b.bits[i] + c
                b.bits[i] = t % 2
                c = t // 2
        return b

    def direct_to_decimal(self, b: BitArray) -> int:
        val = 0
        for i in range(1, 32):
            val = val * 2 + b.bits[i]
        return -val if b.bits[0] == 1 else val

    def additional_to_decimal(self, b: BitArray) -> int:
        if b.bits == [1] + [0] * 31:
            return -2147483648
            
        is_n = b.bits[0] == 1
        t = b.bits.copy()
        
        if is_n:
            c = 1
            for i in range(31, 0, -1):
                diff = t[i] - c
                if diff < 0:
                    t[i] = 1
                    c = 1
                else:
                    t[i] = diff
                    c = 0
            for i in range(1, 32):
                t[i] = 1 - t[i]
                
        val = 0
        for i in range(1, 32):
            val = val * 2 + t[i]
        return -val if is_n else val

    def decimal_to_fixed(self, val: float) -> BitArray:
        b = BitArray()
        b.bits[0] = 1 if val < 0 else 0
        v = abs(val)
        i_part = int(v)
        f_part = v - i_part
        for i in range(14, 0, -1):
            b.bits[i] = i_part % 2
            i_part //= 2
        for i in range(15, 32):
            f_part *= 2
            b.bits[i] = int(f_part)
            f_part -= int(f_part)
        return b

    def fixed_to_decimal(self, b: BitArray) -> float:
        i_part = 0
        for i in range(1, 15):
            i_part = i_part * 2 + b.bits[i]
        f_part = 0
        for i in range(15, 32):
            f_part += b.bits[i] * (2 ** -(i - 14))
        res = round(i_part + f_part, 5)
        return -res if b.bits[0] == 1 else res