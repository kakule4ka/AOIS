from .expr_parser import ExpressionParser
from .truth_table import TruthTable
from .normal_forms import NormalForms
from .zhegalkin import ZhegalkinPolynomial
from .post_classes import PostClasses
from .analyzer import BooleanAnalyzer
from .minimizer import Minimizer

def display_menu():
    print("\n--- Меню ---")
    print("1. Ввести логическую функцию")
    print("2. Вывести таблицу истинности и индексную форму")
    print("3. Вывести СДНФ и СКНФ (строковые и числовые формы)")
    print("4. Вывести классы Поста")
    print("5. Построить полином Жегалкина")
    print("6. Найти фиктивные переменные")
    print("7. Минимизация функции (расчетный метод)")
    print("0. Выход")

def run_menu():
    parser = ExpressionParser()
    evaluator = None
    tt = None

    while True:
        display_menu()
        choice = input("Выберите пункт: ")

        if choice == '0':
            break

        if choice == '1':
            expr = input("Введите функцию (например, !(!a->!b)|c): ")
            try:
                evaluator = parser.parse(expr)
                tt = TruthTable(evaluator)
                print("Функция успешно обработана.")
            except Exception:
                print("Ошибка при разборе функции.")
            continue

        if tt is None:
            print("Сначала введите функцию (пункт 1).")
            continue

        if choice == '2':
            print("\nИндексная форма:", tt.get_index_form())
            print("Переменные:", " ".join(tt.variables), "| Результат")
            for row, res in zip(tt.rows, tt.results):
                row_str = " ".join(map(str, row))
                print(f"{row_str} | {res}")

        elif choice == '3':
            nf = NormalForms(tt)
            print("\nСДНФ:", nf.get_sdnf())
            print("СДНФ (числовая):", nf.get_sdnf_numeric())
            print("СКНФ:", nf.get_sknf())
            print("СКНФ (числовая):", nf.get_sknf_numeric())

        elif choice == '4':
            zh = ZhegalkinPolynomial(tt.results, tt.variables)
            post = PostClasses(tt, zh)
            print("\nКлассы Поста:")
            for cls_name, is_in_class in post.get_all_classes().items():
                print(f"{cls_name}: {'Да' if is_in_class else 'Нет'}")

        elif choice == '5':
            zh = ZhegalkinPolynomial(tt.results, tt.variables)
            print("\nПолином Жегалкина:", zh.get_polynomial())

        elif choice == '6':
            analyzer = BooleanAnalyzer(tt)
            dummies = analyzer.find_dummy_variables()
            print("\nФиктивные переменные:", dummies if dummies else "Нет")

        elif choice == '7':
            minimizer = Minimizer(tt)
            calc_data = minimizer.get_calculation_method()
            print("\nСтадии склеивания:")
            for i, stage in enumerate(calc_data["stages"]):
                print(f"Этап {i}: {stage}")
            print("Простые импликанты:", calc_data["prime_implicants"])
            
        else:
            print("Неверный пункт меню.")

def main():
    run_menu()

if __name__ == "__main__":
    main()