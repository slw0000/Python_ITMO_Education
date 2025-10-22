# Вариант дерева №4
# Root = 4; height = 4, left_leaf = root*4, right_leaf = root+1

def main():
    print('Построение бинарного дерева.')
    inp1 = input('Введите параметр height (или Enter для варианта по умолчанию): ')

    if inp1.strip() == '':
        print(gen_bin_tree())
        return
    inp2 = input('Введите параметр root: ')
    inp1, inp2 = par_is_corr(inp1), par_is_corr(inp2)
    print(gen_bin_tree(inp1, inp2))


def par_is_corr(par) -> int:
    """Проверяет, является ли введенный параметр целым числом. Взято из Лабораторной №2."""

    if type(par) == int:
        return int(par)
    elif type(par) == str:
        if par.lstrip("+-").isdigit():
            return int(par.lstrip("+"))
        if '.' in par and int(par.lstrip("+-").split('.')[1]) == 0:
            return int(float(par))
    elif type(par) == float:
        if par.is_integer():
            return int(par)
    raise TypeError('Неверный формат ввода.')


def gen_bin_tree(height: int = 4, root: int = 4, l_b=lambda x: x * 4,
                 r_b=lambda x: x + 1) -> dict:
    """
    Функция итеративно строит бинарное дерево, представляет его в виде словаря.

    :param height: Высота дерева;
    :param root: Корень ветки;
    :param l_b: Функция значения левой ветки;
    :param r_b: Функция значения правой ветки;

    :return: Бинарное дерево в формате dict (словарь, хэш-таблица).
    """

    height, root = par_is_corr(height), par_is_corr(root)

    if height < 0:
        raise ValueError('Высота (height) должна быть >= 0.')

    sp = [root]
    sp_cur = [root]

    # Генерация списка значений дерева
    for i in range(1, height + 1):
        sp_cur = []

        for j in range(-1, -(2 ** (i - 1) + 1), -1):
            sp_cur.append(l_b(sp[j]))
            sp_cur.append(r_b(sp[j]))

        sp += sp_cur[::-1]

    # преобразование значений списка в хэш-таблицы (dict)
    sp = list(map(lambda n: {str(n): []}, sp))

    # Соединение хэш-таблиц в одно дерево
    for i in range(height, 0, -1):
        sp_keys = []
        for k in range(- (2 ** i) - (2 ** (i - 1)), - (2 ** i)):
            sp_keys.append(k)

        for j in range(-1, -(2 ** i + 1), -2):
            key = list(sp[sp_keys[(j - 1) // 2]])[0]

            sp[sp_keys[(j - 1) // 2]][key].append(sp[j])
            sp[sp_keys[(j - 1) // 2]][key].append(sp[j - 1])

        sp = sp[:-(2 ** i)]

    return sp[0]





if __name__ == '__main__':
    main()

