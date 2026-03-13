from src.converters import NumberConverter
from src.integer_arithmetic import IntegerArithmetic
from src.float_arithmetic import IEEE754Arithmetic
from src.bcd_arithmetic import Excess3BCDArithmetic
from src.formatters import ResultFormatter

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

        try:
            if choice == '1':
                val = int(input("Введите целое число: "))
                direct = converter.decimal_to_direct(val)
                reverse = converter.decimal_to_reverse(val)
                additional = converter.decimal_to_additional(val)
                
                formatter.print_binary(direct, "Прямой код")
                formatter.print_binary(reverse, "Обратный код")
                formatter.print_binary(additional, "Дополнительный код")

            elif choice == '2':
                a = int(input("Введите первое слагаемое: "))
                b = int(input("Введите второе слагаемое: "))
                bit_a = converter.decimal_to_additional(a)
                bit_b = converter.decimal_to_additional(b)
                
                result = int_arithmetic.add_additional(bit_a, bit_b)
                dec_result = converter.additional_to_decimal(result)
                formatter.print_both(result, dec_result, "Результат сложения")

            elif choice == '3':
                a = int(input("Введите уменьшаемое: "))
                b = int(input("Введите вычитаемое: "))
                bit_a = converter.decimal_to_additional(a)
                bit_b = converter.decimal_to_additional(b)
                
                result = int_arithmetic.subtract_additional(bit_a, bit_b)
                dec_result = converter.additional_to_decimal(result)
                formatter.print_both(result, dec_result, "Результат вычитания")

            elif choice == '4':
                a = int(input("Введите первый множитель: "))
                b = int(input("Введите второй множитель: "))
                bit_a = converter.decimal_to_direct(a)
                bit_b = converter.decimal_to_direct(b)
                
                result = int_arithmetic.multiply_direct(bit_a, bit_b)
                formatter.print_binary(result, "Результат умножения (прямой код)")

            elif choice == '5':
                a = int(input("Введите делимое: "))
                b = int(input("Введите делитель: "))
                
                if b == 0:
                    print("Ошибка: деление на ноль.")
                    continue
                    
                bit_a = converter.decimal_to_direct(a)
                bit_b = converter.decimal_to_direct(b)
                
                result = int_arithmetic.divide_direct(bit_a, bit_b)
                formatter.print_binary(result, "Результат деления (прямой код)")

            elif choice == '6':
                a = float(input("Введите первое число: "))
                b = float(input("Введите второе число: "))
                op = input("Выберите операцию (+, -, *, /): ")
                
                if op == '/' and b == 0.0:
                    print("Ошибка: деление на ноль.")
                    continue
                    
                bit_a = float_arithmetic.float_to_bits(a)
                bit_b = float_arithmetic.float_to_bits(b)
                
                if op == '+':
                    result = float_arithmetic.add(bit_a, bit_b)
                elif op == '-':
                    result = float_arithmetic.subtract(bit_a, bit_b)
                elif op == '*':
                    result = float_arithmetic.multiply(bit_a, bit_b)
                elif op == '/':
                    result = float_arithmetic.divide(bit_a, bit_b)
                else:
                    print("Неизвестная операция.")
                    continue
                    
                dec_result = float_arithmetic.bits_to_float(result)
                formatter.print_both(result, dec_result, f"Результат IEEE-754 ({op})")

            elif choice == '7':
                a = int(input("Введите первое слагаемое: "))
                b = int(input("Введите второе слагаемое: "))
                
                bit_a = bcd_arithmetic.decimal_to_excess3(a)
                bit_b = bcd_arithmetic.decimal_to_excess3(b)
                
                result = bcd_arithmetic.add(bit_a, bit_b)
                dec_result = bcd_arithmetic.excess3_to_decimal(result)
                formatter.print_both(result, dec_result, "Результат сложения Excess-3")

            else:
                print("Неверный ввод, попробуйте снова.")

        except ValueError:
            print("Ошибка: введено некорректное значение. Пожалуйста, вводите числа.")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")

if __name__ == "__main__":
    main()