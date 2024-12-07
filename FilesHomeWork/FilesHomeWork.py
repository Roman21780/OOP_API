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
                raise ValueError("Не хватает строк для ингредиентов для блюда '{}', ожидается: {}".format(dish_name, ingredient_count))

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
