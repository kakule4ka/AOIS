from src.converters import NumberConverter
from src.integer_arithmetic import IntegerArithmetic
from src.float_arithmetic import IEEE754Arithmetic
from src.bcd_arithmetic import Excess3BCDArithmetic
from src.formatters import ResultFormatter

INT32_MIN_LIMIT = -2147483648
INT32_MAX_LIMIT = 2147483647
BCD_DIGIT_LIMIT = 7
BCD_VALUE_MIN = -9999999
BCD_VALUE_MAX = 9999999

def get_validated_int(prompt_text, min_threshold=INT32_MIN_LIMIT, max_threshold=INT32_MAX_LIMIT):
    while True:
        try:
            input_value = int(input(prompt_text))
            if not (min_threshold <= input_value <= max_threshold):
                print(f"Ошибка: число должно быть в диапазоне от {min_threshold} до {max_threshold}.")
                continue
            return input_value
        except ValueError:
            print("Ошибка: введите целое число.")

def get_validated_float(prompt_text):
    while True:
        try:
            return float(input(prompt_text))
        except ValueError:
            print("Ошибка: введите вещественное число.")

def display_main_menu():
    print("\n--- Меню лабораторной работы №1 ---")
    print("1. Перевод числа (прямой, обратный, дополнительный)")
    print("2. Сложение в дополнительном коде")
    print("3. Вычитание в дополнительном коде")
    print("4. Умножение в прямом коде")
    print("5. Деление чисел с фиксированной точкой")
    print("6. Операции IEEE-754 (плавающая точка)")
    print("7. Сложение в BCD (Excess-3)")
    print("0. Выход")

def main():
    number_converter = NumberConverter()
    integer_processor = IntegerArithmetic()
    float_processor = IEEE754Arithmetic()
    bcd_processor = Excess3BCDArithmetic()
    result_formatter = ResultFormatter()

    while True:
        display_main_menu()
        user_selection = input("Выберите пункт: ")

        if user_selection == '0':
            break

        if user_selection == '1':
            decimal_value = get_validated_int("Введите число: ")
            direct_binary = number_converter.decimal_to_direct(decimal_value)
            reverse_binary = number_converter.decimal_to_reverse(decimal_value)
            additional_binary = number_converter.decimal_to_additional(decimal_value)
            result_formatter.print_binary(direct_binary, "Прямой код")
            result_formatter.print_binary(reverse_binary, "Обратный код")
            result_formatter.print_binary(additional_binary, "Дополнительный код")

        elif user_selection == '2':
            term_a = get_validated_int("Первое слагаемое: ")
            term_b = get_validated_int("Второе слагаемое: ")
            binary_a = number_converter.decimal_to_additional(term_a)
            binary_b = number_converter.decimal_to_additional(term_b)
            sum_binary = integer_processor.add_additional(binary_a, binary_b)
            sum_decimal = number_converter.additional_to_decimal(sum_binary)
            result_formatter.print_both(sum_binary, sum_decimal, "Сложение")

        elif user_selection == '3':
            minuend = get_validated_int("Уменьшаемое: ")
            subtrahend = get_validated_int("Вычитаемое: ")
            binary_a = number_converter.decimal_to_additional(minuend)
            binary_b = number_converter.decimal_to_additional(subtrahend)
            diff_binary = integer_processor.subtract_additional(binary_a, binary_b)
            diff_decimal = number_converter.additional_to_decimal(diff_binary)
            result_formatter.print_both(diff_binary, diff_decimal, "Вычитание")

        elif user_selection == '4':
            factor_a = get_validated_int("Множитель 1: ")
            factor_b = get_validated_int("Множитель 2: ")
            binary_a = number_converter.decimal_to_direct(factor_a)
            binary_b = number_converter.decimal_to_direct(factor_b)
            product_binary = integer_processor.multiply_direct(binary_a, binary_b)
            product_decimal = number_converter.direct_to_decimal(product_binary)
            result_formatter.print_both(product_binary, product_decimal, "Умножение")

        elif user_selection == '5':
            dividend = get_validated_float("Делимое: ")
            divisor = get_validated_float("Делитель: ")
            if divisor == 0:
                print("Ошибка: деление на ноль.")
                continue
            binary_a = number_converter.decimal_to_fixed(dividend)
            binary_b = number_converter.decimal_to_fixed(divisor)
            quotient_binary = integer_processor.divide_fixed(binary_a, binary_b)
            quotient_decimal = number_converter.fixed_to_decimal(quotient_binary)
            result_formatter.print_both(quotient_binary, quotient_decimal, "Деление")

        elif user_selection == '6':
            val_a = get_validated_float("Число A: ")
            val_b = get_validated_float("Число B: ")
            operation = input("Операция (+, -, *, /): ")
            
            bits_a = float_processor.float_to_bits(val_a)
            bits_b = float_processor.float_to_bits(val_b)
            
            result_bits = None
            if operation == '+':
                result_bits = float_processor.add(bits_a, bits_b)
            elif operation == '-':
                result_bits = float_processor.subtract(bits_a, bits_b)
            elif operation == '*':
                result_bits = float_processor.multiply(bits_a, bits_b)
            elif operation == '/':
                if val_b == 0:
                    print("Ошибка: деление на ноль.")
                    continue
                result_bits = float_processor.divide(bits_a, bits_b)
            
            if result_bits:
                result_decimal = float_processor.bits_to_float(result_bits)
                result_formatter.print_both(result_bits, result_decimal, f"IEEE-754 {operation}")

        elif user_selection == '7':
            bcd_a = get_validated_int("Число A: ", BCD_VALUE_MIN, BCD_VALUE_MAX)
            bcd_b = get_validated_int("Число B: ", BCD_VALUE_MIN, BCD_VALUE_MAX)
            bits_a = bcd_processor.decimal_to_excess3(bcd_a)
            bits_b = bcd_processor.decimal_to_excess3(bcd_b)
            res_bits = bcd_processor.add(bits_a, bits_b)
            res_decimal = bcd_processor.excess3_to_decimal(res_bits)
            result_formatter.print_both(res_bits, res_decimal, "BCD Excess-3")

if __name__ == "__main__":
    main()