def main():
    d_start = input('Введите начало диапазона (целое число): ')
    d_end = input('Введите конец диапазона (включительно): ')
    target = input('Введите число, которое нужно найти (целое число): ')
    print()
    alg_type = input('Введите тип алгоритма: "seq", если алгоритм медленного перебора,\n'
                     '"bin", если алгоритм бинарного поиска: ')
    print()

    while alg_type not in ['seq', 'bin']:
        print('Неверный формат ввода типа алгоритма, повторите ввод.')
        alg_type = input('Введите тип алгоритма: "seq", если алгоритм медленного перебора,\n'
                         '"bin", если алгоритм бинарного поиска: ')
        print()

    res = guess_number(list_generator(d_start, d_end), target, alg_type)
    print('Число', res[0],
          'угадано. Потребовалось шагов:', res[1])



def list_generator(st, fin) -> list[int]:
    """Функция list_generator()
    Принимает на вход два параметра - границы диапазона, переводит их в формат int.
    Возвращает list, который содержит все числа из заданного диапазона.

    :param st: Первая граница диапазона;
    :param fin: Вторая граница диапазона;
    :return: List, содержащий все целые числа находящиеся в диапазоне.
    """
    st, fin = par_is_corr(st), par_is_corr(fin)
    return list(range(min(st, fin), max(st, fin)+1))



def par_is_corr(par):
    """Функция par_is_corr()
    Проверяет, является ли введенный параметр целым числом.
    Т.е. является ли число int, или str, которое можно преобразовать в int,
    или float с нулевой дробной частью.
    Если параметр подходит, то преобразует его в int. Иначе, вызывает TypeError.

    :param par: Переменная любого типа данных;
    :return: par в формате int или TypeError.
    """

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
    raise TypeError('Неверный формат числа для поиска.')



def guess_number(diap: list, target, alg_type: str ='seq') -> tuple[int, int]:
    """Функция guess_number()
    Получает на вход список чисел, число для поиска и тип алгоритма, по которому нужно искать число.
    Содержит проверки на правильность ввода параметров.

    :param diap: список диапазона целых чисел;
    :param target: целое число, которое нужно найти;
    :param alg_type: тип алгоритма: последовательный (seq) или бинарный (bin);
    :return: кортеж из числа, которое нужно было найти, и количество проверок в ходе поиска.
    """
    target = par_is_corr(target)
    if type(diap) != list:
        raise TypeError('Неверный формат ввода диапазона.')
    if len(diap) == 0:
        raise ValueError('Передан пустой список диапазона.')
    if alg_type not in ['seq', 'bin']:
        raise ValueError('Введён неверный тип алгоритма.')
    if target not in diap:
        raise ValueError('Введённое для поиска число находится вне данного диапазона.')

    for i in range(len(diap)):
        diap[i] = par_is_corr(diap[i])

    diap.sort()
    if alg_type == 'seq':
        steps = 0

        for i in diap:
            steps += 1
            if i == target:
                return (i, steps)

    elif alg_type == 'bin':
        steps = 1
        low = 0
        high = len(diap) - 1
        mid = len(diap) // 2

        while diap[mid] != target and low <= high:
            steps += 1
            if target > diap[mid]:
                low = mid + 1
            else:
                high = mid - 1
            mid = (low + high) // 2

        return (target, steps)



if __name__ == '__main__':
    main()
