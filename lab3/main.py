from src.expr_parser import ExpressionParser
from src.truth_table import TruthTable
from src.normal_forms import NormalForms
from src.zhegalkin import ZhegalkinPolynomial
from src.post_classes import PostClasses
from src.analyzer import BooleanAnalyzer
from src.minimizer import Minimizer
from src.lab3 import ODS3Synthesizer, FullBCDShiftSynthesizer, DownCounterSynthesizer

def display_menu():
    print("\n--- Главное меню (ЛР 2) ---")
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
    print("\n--- Синтез автоматов (ЛР 3) ---")
    print("11. Синтез ОДС-3 (СДНФ)")
    print("12. Синтез преобразователя 5421 BCD со смещением 6 (5 входов)")
    print("13. Синтез вычитающего двоичного счетчика (8 состояний, Т-триггер)")
    print("\n0. Выход")

def run_menu():
    parser = ExpressionParser()
    truth_table = None
    
    print("Для работы с пунктами 1-10 (ЛР 2) введите логическую функцию.")
    print("Для ЛР 3 (пункты 11-13) можно пропустить ввод, нажав Enter.")
    
    while True:
        expression_string = input("\nВведите логическую функцию (или Enter для пропуска): ")
        if not expression_string.strip():
            break
        try:
            evaluator = parser.parse(expression_string)
            truth_table = TruthTable(evaluator)
            break
        except Exception as error:
            print(f"Ошибка ввода: {error}")

    while True:
        display_menu()
        choice = input("Выберите пункт: ")

        if choice in [str(i) for i in range(1, 11)] and truth_table is None:
            print("\nОшибка: Для использования методов ЛР 2 необходимо ввести логическую функцию при запуске.")
            continue

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
            
        elif choice == '11':
            print("\n--- Синтез ОДС-3 ---")
            synthesizer = ODS3Synthesizer()
            results = synthesizer.synthesize()
            
            for func_name in ['sum', 'carry']:
                func_title = "Сумма (S)" if func_name == 'sum' else "Перенос (P)"
                print(f"\n--- Функция: {func_title} ---")
                print(results[func_name]['table'])
                print(f"СДНФ: {results[func_name]['sdnf']}")
                print(f"МДНФ: {results[func_name]['minimized']['minimal_form']}")

        elif choice == '12':
            print("\n--- Синтез преобразователя 5421 BCD (смещение n=6) ---")
            synthesizer = FullBCDShiftSynthesizer(shift=6)
            results = synthesizer.synthesize()
            
            for out_var in sorted(results.keys(), reverse=True):
                print(f"\n--- Выходная функция: {out_var} ---")
                print(results[out_var]['table'])
                print(f"СДНФ: {results[out_var]['sdnf']}")
                print(f"МДНФ: {results[out_var]['minimized']['minimal_form']}")

        elif choice == '13':
            print("\n--- Синтез вычитающего счетчика (8 состояний, Т-триггер) ---")
            synthesizer = DownCounterSynthesizer()
            results = synthesizer.synthesize()
            
            for t_var in sorted(results.keys(), reverse=True):
                print(f"\n--- Функция возбуждения: {t_var} ---")
                print(results[t_var]['table'])
                print(f"СДНФ: {results[t_var]['sdnf']}")
                print(f"МДНФ: {results[t_var]['minimized']['minimal_form']}")
                
        elif choice == '0':
            print("Выход из программы.")
            break
            
        else:
            print("Неверный выбор. Пожалуйста, выберите корректный пункт меню.")

if __name__ == '__main__':
    run_menu()