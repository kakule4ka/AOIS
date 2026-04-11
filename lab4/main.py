from src.hash_table import HashTable

def print_menu() -> None:
    print("\n--- Меню управления хеш-таблицей ---")
    print("1. Добавить запись")
    print("2. Найти запись")
    print("3. Обновить запись")
    print("4. Удалить запись")
    print("5. Вывести хеш-таблицу на экран")

def main() -> None:
    ht = HashTable()

    while True:
        print_menu()
        choice = input("Выберите пункт меню: ")

        if choice == "1":
            key = input("Введите ключевое слово (фамилию): ")
            data = input("Введите данные: ")
            if ht.create(key, data):
                print("Запись успешно добавлена.")
            else:
                print("Ошибка: Запись с таким ключом уже существует.")

        elif choice == "2":
            key = input("Введите ключевое слово для поиска: ")
            result = ht.read(key)
            if result is not None:
                print(f"Данные по ключу '{key}': {result}")
            else:
                print("Запись не найдена.")

        elif choice == "3":
            key = input("Введите ключевое слово для обновления: ")
            new_data = input("Введите новые данные: ")
            if ht.update(key, new_data):
                print("Запись успешно обновлена.")
            else:
                print("Ошибка: Запись для обновления не найдена.")

        elif choice == "4":
            key = input("Введите ключевое слово для удаления: ")
            if ht.delete(key):
                print("Запись успешно удалена.")
            else:
                print("Ошибка: Запись для удаления не найдена.")

        elif choice == "5":
            print("\n=== Содержимое хеш-таблицы ===")
            ht.display()
            print(f"\nКоэффициент заполнения: {ht.load_factor()}")

        else:
            print("Некорректный ввод. Попробуйте снова.")

if __name__ == "__main__":
    main()