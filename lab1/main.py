from src.converters import NumberConverter
from src.integer_arithmetic import IntegerArithmetic
from src.float_arithmetic import IEEE754Arithmetic
from src.bcd_arithmetic import Excess3BCDArithmetic
from src.formatters import ResultFormatter

MIN_INT_VALUE = -2147483648
MAX_INT_VALUE = 2147483647
MIN_BCD_VALUE = -9999999
MAX_BCD_VALUE = 9999999

def get_int(prompt_message, minimum_value=MIN_INT_VALUE, maximum_value=MAX_INT_VALUE):
    while True:
        try:
            input_value = int(input(prompt_message))
            if input_value < minimum_value or input_value > maximum_value:
                print(f"Ошибка: число должно быть от {minimum_value} до {maximum_value}")
                continue
            return input_value
        except ValueError:
            print("Ошибка: введите целое число")

def get_float(prompt_message):
    while True:
        try:
            return float(input(prompt_message))
        except ValueError:
            print("Ошибка: введите вещественное число")

def print_menu():
    print("\nМеню")
    print("1. Перевод числа из 10-го в 2-ый (прямой, обратный, дополнительный)")
    print("2. Сложение в дополнительном коде")
    print("3. Вычитание в дополнительном коде (через сложение)")
    print("4. Умножение в прямом коде")
    print("5. Деление в прямом коде")
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
            input_value = get_int("Введите целое число: ")
            direct_code = converter.decimal_to_direct(input_value)
            reverse_code = converter.decimal_to_reverse(input_value)
            additional_code = converter.decimal_to_additional(input_value)
            formatter.print_binary(direct_code, "Прямой код")
            formatter.print_binary(reverse_code, "Обратный код")
            formatter.print_binary(additional_code, "Дополнительный код")

        elif choice == '2':
            first_operand = get_int("Введите первое слагаемое: ")
            second_operand = get_int("Введите второе слагаемое: ")
            first_bit_array = converter.decimal_to_additional(first_operand)
            second_bit_array = converter.decimal_to_additional(second_operand)
            result_array = int_arithmetic.add_additional(first_bit_array, second_bit_array)
            decimal_result = converter.additional_to_decimal(result_array)
            formatter.print_both(result_array, decimal_result, "Результат сложения")

        elif choice == '3':
            first_operand = get_int("Введите уменьшаемое: ")
            second_operand = get_int("Введите вычитаемое: ")
            first_bit_array = converter.decimal_to_additional(first_operand)
            second_bit_array = converter.decimal_to_additional(second_operand)
            result_array = int_arithmetic.subtract_additional(first_bit_array, second_bit_array)
            decimal_result = converter.additional_to_decimal(result_array)
            formatter.print_both(result_array, decimal_result, "Результат вычитания")

        elif choice == '4':
            first_operand = get_int("Введите первый множитель: ")
            second_operand = get_int("Введите второй множитель: ")
            first_bit_array = converter.decimal_to_direct(first_operand)
            second_bit_array = converter.decimal_to_direct(second_operand)
            result_array = int_arithmetic.multiply_direct(first_bit_array, second_bit_array)
            decimal_result = converter.direct_to_decimal(result_array)
            formatter.print_both(result_array, decimal_result, "Результат умножения")

        elif choice == '5':
            first_operand = get_float("Введите делимое: ")
            while True:
                second_operand = get_float("Введите делитель: ")
                if second_operand != 0:
                    break
                print("Ошибка: деление на ноль")
            first_bit_array = converter.decimal_to_fixed(first_operand)
            second_bit_array = converter.decimal_to_fixed(second_operand)
            result_array = int_arithmetic.divide_fixed(first_bit_array, second_bit_array)
            decimal_result = converter.fixed_to_decimal(result_array)
            formatter.print_both(result_array, decimal_result, "Результат деления")

        elif choice == '6':
            first_operand = get_float("Введите первое число: ")
            second_operand = get_float("Введите второе число: ")
            operator_symbol = input("Выберите операцию (+, -, *, /): ")
            
            if operator_symbol == '/' and second_operand == 0.0:
                print("Ошибка: деление на ноль")
                continue
            
            first_bit_array = float_arithmetic.float_to_bits(first_operand)
            second_bit_array = float_arithmetic.float_to_bits(second_operand)
            
            if operator_symbol == '+':
                result_array = float_arithmetic.add(first_bit_array, second_bit_array)
            elif operator_symbol == '-':
                result_array = float_arithmetic.subtract(first_bit_array, second_bit_array)
            elif operator_symbol == '*':
                result_array = float_arithmetic.multiply(first_bit_array, second_bit_array)
            elif operator_symbol == '/':
                result_array = float_arithmetic.divide(first_bit_array, second_bit_array)
            else:
                print("Неизвестная операция")
                continue
                
            decimal_result = float_arithmetic.bits_to_float(result_array)
            formatter.print_both(result_array, decimal_result, f"Результат IEEE-754 ({operator_symbol})")

        elif choice == '7':
            first_operand = get_int("Введите первое слагаемое: ", MIN_BCD_VALUE, MAX_BCD_VALUE)
            second_operand = get_int("Введите второе слагаемое: ", MIN_BCD_VALUE, MAX_BCD_VALUE)
            first_bit_array = bcd_arithmetic.decimal_to_excess3(first_operand)
            second_bit_array = bcd_arithmetic.decimal_to_excess3(second_operand)
            result_array = bcd_arithmetic.add(first_bit_array, second_bit_array)
            decimal_result = bcd_arithmetic.excess3_to_decimal(result_array)
            formatter.print_both(result_array, decimal_result, "Результат сложения Excess-3")

        else:
            print("Неверный ввод")

if __name__ == "__main__":
    main()
