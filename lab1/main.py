from src.converters import NumberConverter
from src.integer_arithmetic import IntegerArithmetic
from src.float_arithmetic import IEEE754Arithmetic
from src.bcd_arithmetic import Excess3BCDArithmetic
from src.formatters import ResultFormatter

# Constants for input validation
INT32_MIN = -(2**31)
INT32_MAX = 2**31 - 1
BCD_MAX_DIGITS = 7
BCD_MIN_VAL = -(10**BCD_MAX_DIGITS - 1)
BCD_MAX_VAL = 10**BCD_MAX_DIGITS - 1

def get_int(prompt, min_val=INT32_MIN, max_val=INT32_MAX):
    while True:
        try:
            val = int(input(prompt))
            if not (min_val <= val <= max_val):
                print(f"Ошибка: число должно быть в диапазоне от {min_val} до {max_val}.")
                continue
            return val
        except ValueError:
            print("Ошибка: введите целое число.")

def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка: введите вещественное число.")

def print_menu():
    print("\nМеню")
    print("1. Перевод числа из 10-го в 2-ый (прямой, обратный, дополнительный)")
    print("2. Сложение в дополнительном коде")
    print("3. Вычитание в дополнительном коде (через сложение)")
    print("4. Умножение в прямом коде")
    print("5. Деление чисел с фиксированной точкой")
    print("6. Операции с плавающей точкой (IEEE-754)")
    print("7. Сложение в BCD (Excess-3)")
    print("0. Выход")

def main():
    converter = NumberConverter()
    int_arithmetic = IntegerArithmetic()
    float_arithmetic = IEEE754Arithmetic()
    bcd_arithmetic = Excess3BCDArithmetic()
    formatter = ResultFormatter()

    while True:
        print_menu()
        choice = input("Выберите пункт меню: ")

        if choice == '0':
            break

        if choice == '1':
            value = get_int("Введите целое число: ")
            direct_code = converter.decimal_to_direct(value)
            reverse_code = converter.decimal_to_reverse(value)
            additional_code = converter.decimal_to_additional(value)
            formatter.print_binary(direct_code, "Прямой код")
            formatter.print_binary(reverse_code, "Обратный код")
            formatter.print_binary(additional_code, "Дополнительный код")

        elif choice == '2':
            num_a = get_int("Введите первое слагаемое: ")
            num_b = get_int("Введите второе слагаемое: ")
            bits_a = converter.decimal_to_additional(num_a)
            bits_b = converter.decimal_to_additional(num_b)
            result_bits = int_arithmetic.add_additional(bits_a, bits_b)
            result_decimal = converter.additional_to_decimal(result_bits)
            formatter.print_both(result_bits, result_decimal, "Результат сложения")

        elif choice == '3':
            minuend = get_int("Введите уменьшаемое: ")
            subtrahend = get_int("Введите вычитаемое: ")
            bits_a = converter.decimal_to_additional(minuend)
            bits_b = converter.decimal_to_additional(subtrahend)
            result_bits = int_arithmetic.subtract_additional(bits_a, bits_b)
            result_decimal = converter.additional_to_decimal(result_bits)
            formatter.print_both(result_bits, result_decimal, "Результат вычитания")

        elif choice == '4':
            factor_a = get_int("Введите первый множитель: ")
            factor_b = get_int("Введите второй множитель: ")
            bits_a = converter.decimal_to_direct(factor_a)
            bits_b = converter.decimal_to_direct(factor_b)
            result_bits = int_arithmetic.multiply_direct(bits_a, bits_b)
            result_decimal = converter.direct_to_decimal(result_bits)
            formatter.print_both(result_bits, result_decimal, "Результат умножения")

        elif choice == '5':
            dividend = get_float("Введите делимое: ")
            while True:
                divisor = get_float("Введите делитель: ")
                if divisor != 0:
                    break
                print("Ошибка: деление на ноль.")
            bits_a = converter.decimal_to_fixed(dividend)
            bits_b = converter.decimal_to_fixed(divisor)
            result_bits = int_arithmetic.divide_fixed(bits_a, bits_b)
            result_decimal = converter.fixed_to_decimal(result_bits)
            formatter.print_both(result_bits, result_decimal, "Результат деления")

        elif choice == '6':
            num_a = get_float("Введите первое число: ")
            num_b = get_float("Введите второе число: ")
            operation = input("Выберите операцию (+, -, *, /): ")
            if operation == '/' and num_b == 0.0:
                print("Ошибка: деление на ноль.")
                continue
            
            bits_a = float_arithmetic.float_to_bits(num_a)
            bits_b = float_arithmetic.float_to_bits(num_b)
            
            result_bits = None
            if op == '+':
                result_bits = float_arithmetic.add(bits_a, bits_b)
            elif op == '-':
                result_bits = float_arithmetic.subtract(bits_a, bits_b)
            elif op == '*':
                result_bits = float_arithmetic.multiply(bits_a, bits_b)
            elif op == '/':
                result_bits = float_arithmetic.divide(bits_a, bits_b)
            else:
                print("Неизвестная операция.")
                continue
                
            result_decimal = float_arithmetic.bits_to_float(result_bits)
            formatter.print_both(result_bits, result_decimal, f"Результат IEEE-754 ({operation})")

        elif choice == '7':
            num_a = get_int("Введите первое слагаемое: ", BCD_MIN_VAL, BCD_MAX_VAL)
            num_b = get_int("Введите второе слагаемое: ", BCD_MIN_VAL, BCD_MAX_VAL)
            bits_a = bcd_arithmetic.decimal_to_excess3(num_a)
            bits_b = bcd_arithmetic.decimal_to_excess3(num_b)
            result_bits = bcd_arithmetic.add(bits_a, bits_b)
            result_decimal = bcd_arithmetic.excess3_to_decimal(result_bits)
            formatter.print_both(result_bits, result_decimal, "Результат сложения Excess-3")

        else:
            print("Неверный ввод.")

if __name__ == "__main__":
    main()