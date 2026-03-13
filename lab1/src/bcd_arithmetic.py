from src.bit_array import BitArray

class Excess3BCDArithmetic:
    def __init__(self):
        pass

    def decimal_to_excess3(self, val: int) -> BitArray:
        res = BitArray()
        val_str = str(abs(val))
        
        idx = 31
        for char in reversed(val_str):
            digit = int(char) + 3
            for _ in range(4):
                res.bits[idx] = digit % 2
                digit //= 2
                idx -= 1
                
        res.bits[0] = 1 if val < 0 else 0
        return res

    def excess3_to_decimal(self, bit_array: BitArray) -> int:
        val_str = ""
        for i in range(31, 3, -4):
            group = bit_array.bits[i-3:i+1]
            digit = group[0]*8 + group[1]*4 + group[2]*2 + group[3]
            if digit >= 3:
                val_str = str(digit - 3) + val_str
                
        if not val_str:
            return 0
            
        result = int(val_str)
        return -result if bit_array.bits[0] == 1 else result

    def add(self, a: BitArray, b: BitArray) -> BitArray:
        val_a = self.excess3_to_decimal(a)
        val_b = self.excess3_to_decimal(b)
        return self.decimal_to_excess3(val_a + val_b)