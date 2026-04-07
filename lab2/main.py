from src.expr_parser import ExpressionParser
from src.truth_table import TruthTable
from src.normal_forms import NormalForms
from src.zhegalkin import ZhegalkinPolynomial
from src.post_classes import PostClasses
from src.analyzer import BooleanAnalyzer
from src.minimizer import Minimizer

def display_menu():
    print("\n--- Главное меню ---")
    print("1. Таблица истинности")
    print("2. СДНФ и СКНФ (строковая и числовая формы)")
    print("3. Индексная форма")
    print("4. Классы Поста")
    print("5. Полином Жегалкина")
    print("6. Фиктивные переменные")
    print("7. Булева дифференциация")
    print("8. Расчетный метод минимизации")
    print("9. Расчетно-табличный метод минимизации")
    print("10. Табличный метод (карта Карно)")
    print("0. Выход")

def run_menu():
    parser = ExpressionParser()
    while True:
        expression_string = input("\nВведите логическую функцию: ")
        try:
            evaluator = parser.parse(expression_string)
            truth_table = TruthTable(evaluator)
            break
        except Exception as error:
            print(f"Ошибка ввода: {error}")

    while True:
        display_menu()
        choice = input("Выберите пункт: ")

        if choice == '1':
            print("\nТаблица истинности:")
            print(truth_table)
            
        elif choice == '2':
            normal_forms = NormalForms(truth_table)
            print("\nСДНФ:", normal_forms.get_sdnf())
            print("СКНФ:", normal_forms.get_sknf())
            print("СДНФ (числовая):", normal_forms.get_sdnf_numeric())
            print("СКНФ (числовая):", normal_forms.get_sknf_numeric())
            
        elif choice == '3':
            print("\nИндексная форма:", truth_table.get_index_form())
            
        elif choice == '4':
            zhegalkin_polynomial = ZhegalkinPolynomial(truth_table.get_index_form(), truth_table.variables)
            post_classes = PostClasses(truth_table, zhegalkin_polynomial)
            classes = post_classes.get_all_classes()
            print("\nКлассы Поста:")
            for class_name, is_member in classes.items():
                print(f"{class_name}: {'+' if is_member else '-'}")
                
        elif choice == '5':
            zhegalkin_polynomial = ZhegalkinPolynomial(truth_table.get_index_form(), truth_table.variables)
            print("\nПолином Жегалкина:", zhegalkin_polynomial.get_polynomial())
            
        elif choice == '6':
            analyzer = BooleanAnalyzer(evaluator, truth_table.variables)
            dummy_variables = analyzer.find_dummy_variables()
            if dummy_variables:
                print("\nФиктивные переменные:", ", ".join(dummy_variables))
            else:
                print("\nФиктивных переменных нет.")
                
        elif choice == '7':
            target_variable = input(f"Введите переменную для дифференцирования ({', '.join(truth_table.variables)}): ")
            analyzer = BooleanAnalyzer(evaluator, truth_table.variables)
            derivative_result = analyzer.get_derivative(target_variable)
            if derivative_result:
                print(f"\nПроизводная df/d{target_variable} (индексная форма): {derivative_result}")
            else:
                print("\nОшибка: такая переменная не найдена.")
                
        elif choice == '8':
            minimizer = Minimizer(truth_table)
            for is_sdnf, form_name in [(True, "ДНФ"), (False, "КНФ")]:
                print(f"\n--- Расчетный метод ({form_name}) ---")
                calculation_data = minimizer.get_calculation_method(for_sdnf=is_sdnf)
                for index, stage in enumerate(calculation_data["stages"]):
                    print(f"Этап {index+1}:", stage)
                print("Простые импликанты:", calculation_data["prime_implicants"])
                print(f"ИТОГ М{form_name}:", calculation_data["minimal_form"])
                
        elif choice == '9':
            minimizer = Minimizer(truth_table)
            for is_sdnf, form_name in [(True, "ДНФ"), (False, "КНФ")]:
                print(f"\n--- Расчетно-табличный метод ({form_name}) ---")
                tabular_data = minimizer.get_tabular_method(for_sdnf=is_sdnf)
                for index, stage in enumerate(tabular_data["stages"]):
                    print(f"Этап {index+1}:", stage)
                print("Таблица покрытия:")
                for implicant, minterms in tabular_data["table"].items():
                    print(f"Импликанта {implicant} покрывает: {', '.join(minterms)}")
                print(f"ИТОГ М{form_name}:", tabular_data["minimal_form"])
                
        elif choice == '10':
            minimizer = Minimizer(truth_table)
            karnaugh_map_data = minimizer.get_karnaugh_map()
            if isinstance(karnaugh_map_data, str):
                print(karnaugh_map_data)
            else:
                print(f"\nКарта Карно ({karnaugh_map_data['rows_vars']} \\ {karnaugh_map_data['cols_vars']}):")
                for row in karnaugh_map_data['map']:
                    print("\t".join(row))
            print("\nИТОГ МДНФ:", minimizer.get_calculation_method(for_sdnf=True)["minimal_form"])
            print("ИТОГ МКНФ:", minimizer.get_calculation_method(for_sdnf=False)["minimal_form"])
            
        elif choice == '0':
            break
            
        else:
            print("Неверный выбор.")

if __name__ == '__main__':
    run_menu()