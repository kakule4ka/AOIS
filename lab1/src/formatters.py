from src.bit_array import BitArray

class ResultFormatter:
    def __init__(self):
        pass

    def print_binary(self, bit_array: BitArray, label: str = "Binary"):
        full_binary = ''.join(map(str, bit_array.bits))
        sign_bit = str(bit_array.bits[0])
        value_bits = bit_array.bits[1:]
        start_idx = -1
        
        for i in range(len(value_bits)):
            if value_bits[i] == 1:
                start_idx = i
                break
                
        if start_idx == -1:
            trimmed_str = "0"
        else:
            trimmed_str = ''.join(map(str, value_bits[start_idx:]))
            
        print(f"{label}: {sign_bit}{trimmed_str} ({full_binary})")

    def print_decimal(self, decimal_val: float, label: str = "Decimal"):
        print(f"{label}: {decimal_val}")

    def print_both(self, bit_array: BitArray, decimal_val: float, operation: str = "Result"):
        print(f"{operation}:")
        self.print_binary(bit_array)
        self.print_decimal(decimal_val)
        print()