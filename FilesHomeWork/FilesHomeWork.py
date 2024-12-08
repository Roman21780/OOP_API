def read_cookbook(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    cook_book = {}
    index = 0
    while index < len(lines):
        line = lines[index].strip()

        if line == "":
            index += 1
            continue

        dish_name = line
        index += 1

        # Проверяем, что следующая строка не пустая
        if index >= len(lines) or lines[index].strip() == "":
            raise ValueError("Ожидалось количество ингредиентов для блюда '{}', но строки нет.".format(dish_name))

        # Проверяем, можно ли преобразовать следующую строку в целое число
        try:
            ingredient_count = int(lines[index].strip())
        except ValueError:
            raise ValueError("Ожидалось целое число для количества ингредиентов, но получено: {}".format(lines[index]))

        index += 1
        ingredients = []

        for _ in range(ingredient_count):
            if index >= len(lines):
                raise ValueError("Не хватает строк для ингредиентов для блюда '{}', ожидается: {}".format(dish_name,
                                                                                                          ingredient_count))

            ingredient_info = lines[index].strip().split(' | ')
            if len(ingredient_info) != 3:
                raise ValueError("Некорректный формат строки ингредиента: {}".format(lines[index]))

            ingredient_name = ingredient_info[0]
            quantity = int(ingredient_info[1])
            measure = ingredient_info[2]

            ingredients.append({
                'ingredient_name': ingredient_name,
                'quantity': quantity,
                'measure': measure
            })
            index += 1

        cook_book[dish_name] = ingredients

    return cook_book


def get_shop_list_by_dishes(dishes, person_count):
    cook_book = read_cookbook(file_path)
    # Создадим пустой словарь для хранения итоговых ингредиентов
    shop_list = {}
    # Пройдемся по каждому блюду в списке и получим его ингредиенты из 'cook-book'
    for dish in dishes:
        if dish not in cook_book:
            raise ValueError(f"Блюдо '{dish}' не найдено в рецептах.")

        ingredients = cook_book[dish]

        for ingredient in ingredients:
            ingredient_name = ingredient['ingredient_name']
            # Умножим количество каждого ингредиента на количество персон
            quantity = ingredient['quantity'] * person_count
            measure = ingredient['measure']

            # Если ингредиент уже присутствует в итоговом словаре, просто обновим его количество
            if ingredient_name in shop_list:
                shop_list[ingredient_name]['quantity'] += quantity
            else:
                shop_list[ingredient_name] = {
                    'measure': measure,
                    'quantity': quantity
                }
    # Вернем итоговый словарь
    return shop_list


if __name__ == "__main__":
    file_path = r'C:\Python\pythonProject1\OOP_API\FilesHomeWork\recipes.txt'
    recipes = read_cookbook(file_path)
    print(recipes)

    # print("cook_book = {")
    # for dish, ingredients in recipes.items():
    #     print(f"'{dish}':")
    #     for ingredient in ingredients:
    #         print(f"ingredient_name: {ingredient['ingredient_name']}, quantity: {ingredient['quantity']}, measure: {ingredient['measure']}")
    #     print() # Пустая строка после каждого блюда

    result = get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2)
    print(result)

# Список файлов для объединения
file_names = [
    "1.txt",
    "2.txt",
    "3.txt"
]

# Список для хранения информации о файлах (имя файла и количество строк)
files_info = []

# Считываем количество строк в каждом файле и сохраняем информацию
for file_name in file_names:
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        line_count = len(lines)
        files_info.append((file_name, line_count, lines))

# Сортируем файлы по количеству строк
files_info.sort(key=lambda x: x[1])

# Путь к результирующему файлу
output_file = "merged_output.txt"

# Записываем содержимое в результирующий файл
with open(output_file, 'w', encoding='utf-8') as out_f:
    for file_name, line_count, lines in files_info:
        out_f.write(f"{file_name}\n")
        out_f.write(f"{line_count}\n")
        out_f.writelines(lines)

print(f"Содержимое файлов объединено и записано в '{output_file}'")

