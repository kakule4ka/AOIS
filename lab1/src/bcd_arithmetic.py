from src.bit_array import BitArray

WORD_SIZE = 32
BCD_GROUP_SIZE = 4
EXCESS_OFFSET = 3
MAX_BITS_INDEX = WORD_SIZE - 1
MAX_VALUE_ZFILL = 7

class Excess3BCDArithmetic:
    def decimal_to_excess3(self, decimal_value: int) -> BitArray:
        result_array = BitArray()
        result_array.bits[0] = 1 if decimal_value < 0 else 0
        value_string = str(abs(decimal_value)).zfill(MAX_VALUE_ZFILL)
        bit_index = MAX_BITS_INDEX
        
        for char in reversed(value_string):
            digit_value = int(char) + EXCESS_OFFSET
            for _ in range(BCD_GROUP_SIZE):
                result_array.bits[bit_index] = digit_value % 2
                digit_value //= 2
                bit_index -= 1
                
        return result_array

    def excess3_to_decimal(self, bit_array: BitArray) -> int:
        value_string = ""
        for group_end in range(MAX_BITS_INDEX, EXCESS_OFFSET, -BCD_GROUP_SIZE):
            group_start = group_end - EXCESS_OFFSET
            bit_group = bit_array.bits[group_start:group_end + 1]
            digit_value = bit_group[0] * 8 + bit_group[1] * 4 + bit_group[2] * 2 + bit_group[3]
            
            if digit_value >= EXCESS_OFFSET:
                value_string = str(digit_value - EXCESS_OFFSET) + value_string
                
        parsed_result = int(value_string) if value_string else 0
        return -parsed_result if bit_array.bits[0] == 1 else parsed_result

    def add(self, array_a: BitArray, array_b: BitArray) -> BitArray:
        result_array = BitArray()
        carry_bit = 0
        
        for group_end in range(MAX_BITS_INDEX, EXCESS_OFFSET, -BCD_GROUP_SIZE):
            group_start = group_end - EXCESS_OFFSET
            group_a = array_a.bits[group_start:group_end + 1]
            group_b = array_b.bits[group_start:group_end + 1]
            sum_bits = [0] * BCD_GROUP_SIZE
            local_carry = carry_bit
            
            for bit_index in range(3, -1, -1):
                temp_sum = group_a[bit_index] + group_b[bit_index] + local_carry
                sum_bits[bit_index] = temp_sum % 2
                local_carry = temp_sum // 2
                
            if local_carry == 1:
                correction_array = [0, 0, 1, 1]
                correction_carry = 0
                for bit_index in range(3, -1, -1):
                    temp_sum = sum_bits[bit_index] + correction_array[bit_index] + correction_carry
                    result_array.bits[group_start + bit_index] = temp_sum % 2
                    correction_carry = temp_sum // 2
                carry_bit = 1
            else:
                correction_array = [1, 1, 0, 1]
                correction_carry = 0
                for bit_index in range(3, -1, -1):
                    temp_sum = sum_bits[bit_index] + correction_array[bit_index] + correction_carry
                    result_array.bits[group_start + bit_index] = temp_sum % 2
                    correction_carry = temp_sum // 2
                carry_bit = 0
                
        result_array.bits[0] = array_a.bits[0]
        return result_array
