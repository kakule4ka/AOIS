from src.bit_array import BitArray

class ResultFormatter:
    def print_binary(self, bit_array: BitArray, label: str = "Binary"):
        full_binary_string = ''.join(map(str, bit_array.bits))
        sign_bit = str(bit_array.bits[0])
        value_bits = bit_array.bits[1:]
        first_one_index = -1
        
        for bit_index in range(len(value_bits)):
            if value_bits[bit_index] == 1:
                first_one_index = bit_index
                break
                
        if first_one_index == -1:
            trimmed_value_string = "0"
        else:
            trimmed_value_string = ''.join(map(str, value_bits[first_one_index:]))
            
        print(f"{label}: {sign_bit}{trimmed_value_string} ({full_binary_string})")

    def print_decimal(self, decimal_value: float, label: str = "Decimal"):
        print(f"{label}: {decimal_value}")

    def print_both(self, bit_array: BitArray, decimal_value: float, operation_name: str = "Result"):
        print(f"{operation_name}:")
        self.print_binary(bit_array)
        self.print_decimal(decimal_value)
        print()
