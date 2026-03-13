from src.bit_array import BitArray

class NumberConverter:
    def __init__(self):
        pass

    def decimal_to_direct(self, decimal_val: int) -> BitArray:
        bit_array = BitArray()
        bit_array.bits[0] = 1 if decimal_val < 0 else 0
        temp_numb = abs(decimal_val)
        
        for i in range(31, 0, -1):
            bit_array.bits[i] = temp_numb % 2
            temp_numb //= 2
            
        return bit_array

    def decimal_to_reverse(self, decimal_val: int) -> BitArray:
        bit_array = self.decimal_to_direct(decimal_val)
        
        if decimal_val < 0:
            for i in range(1, 32):
                bit_array.bits[i] = 1 if bit_array.bits[i] == 0 else 0
                
        return bit_array

    def decimal_to_additional(self, decimal_val: int) -> BitArray:
        bit_array = self.decimal_to_reverse(decimal_val)
        
        if decimal_val < 0:
            for i in range(31, 0, -1):
                bit_array.bits[i] += 1
                if bit_array.bits[i] == 2:
                    bit_array.bits[i] = 0
                else:
                    break
                    
        return bit_array

    def additional_to_decimal(self, bit_array: BitArray) -> int:
        is_negative = bit_array.bits[0] == 1
        temp_bits = bit_array.bits.copy()
        
        if is_negative:
            for i in range(31, 0, -1):
                temp_bits[i] -= 1
                if temp_bits[i] == -1:
                    temp_bits[i] = 1
                else:
                    break
            for i in range(1, 32):
                temp_bits[i] = 1 if temp_bits[i] == 0 else 0

        val = 0
        for i in range(1, 32):
            val = val * 2 + temp_bits[i]
            
        return -val if is_negative else val