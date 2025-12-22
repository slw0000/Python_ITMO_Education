from libc.math cimport cos

def integrate_cy_cos(double a, double b, int n_iter=1000):
    """
    Вычисляет приближённое значение определённого интеграла функции `f`
    на отрезке [a, b] методом левых прямоугольников.

    Для функций с разрывами или сильными
    осцилляциями результат может быть неточным.

    Аргументы
        :param f: Интегрируемая функция одной переменной.
        :param a: Левая граница отрезка интегрирования.
        :param b: Правая граница отрезка интегрирования.
        :param n_iter: Количество итераций/прямоугольников.
            Чем больше значение, тем точнее приближение.

    Возвращает
        :return: Приближённое значение определённого интеграла в виде числа типа float.
    """
    if a > b:
        raise ValueError("a не может быть больше b")
    if n_iter <= 0:
        raise ValueError("n_iter должно быть положительным")

    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef double x

    cdef int i = 0
    while i < n_iter:
        x = a + i * step
        acc += cos(x) * step
        i += 1

    return acc