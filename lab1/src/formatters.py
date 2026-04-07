from .bit_array import BitArray

class ResultFormatter:
    def print_binary(self, bit_array: BitArray, label: str = "Binary"):
        full_binary_string = ''.join(map(str, bit_array.bits))
        sign_bit = str(bit_array.bits[0])
        payload_bits = bit_array.bits[1:]
        
        first_unit_index = -1
        for i in range(len(payload_bits)):
            if payload_bits[i] == 1:
                first_unit_index = i
                break
                
        if first_unit_index == -1:
            trimmed_binary = "0"
        else:
            trimmed_binary = ''.join(map(str, payload_bits[first_unit_index:]))
            
        print(f"{label}: {sign_bit}{trimmed_binary} ({full_binary_string})")

    def print_decimal(self, decimal_value: float, label: str = "Decimal"):
        print(f"{label}: {decimal_value}")

    def print_both(self, bit_array: BitArray, decimal_value: float, operation_name: str = "Result"):
        print(f"--- {operation_name} ---")
        self.print_binary(bit_array)
        self.print_decimal(decimal_value)
        print()