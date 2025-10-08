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


def par_is_corr(par):
    """Проверяет, является ли введенный параметр целым числом."""

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


def left_branch(root:int, func=lambda x: x * 4)->int:
    """Вычисляет значение левой ветки."""
    return  func(root)


def right_branch(root:int, func=lambda x: x + 1)->int:
    """Вычисляет значение правой ветки."""
    return func(root)


def gen_bin_tree(height: int = 4, root: int = 4, l_b: callable = left_branch,
                 r_b: callable = right_branch, h: int = 0)->dict:
    """
    Функция рекурсивно строит бинарное дерево, представляет его в виде словаря.

    :param height: Высота дерева;
    :param root: Корень ветки (при рекурсии меняется);
    :param l_b: Функция значения левой ветки;
    :param r_b: Функция значения правой ветки;
    :param h: Номер текущего уровня/ветки (нужна для остановки рекурсии);

    :return: Бинарное дерево в формате dict (словарь, хэш-таблица).
    """

    height, root, h = par_is_corr(height), par_is_corr(root), par_is_corr(h)
    cur_bran = [l_b(root), r_b(root)]

    if height < 0:
        raise ValueError('Высота (height) должна быть >= 0.')
    if h > height:
        raise ValueError('Параметр h не может быть больше height.')

    if h < height:
        return {
            str(root): [gen_bin_tree(height=height, root=cur_bran[0], l_b=l_b, r_b=r_b, h=h+1),
                        gen_bin_tree(height=height, root=cur_bran[1], l_b=l_b, r_b=r_b, h=h+1)]
        }
    return {str(root): []}


if __name__ == '__main__':
    main()

