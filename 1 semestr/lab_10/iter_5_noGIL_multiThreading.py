from iter_5_noGIL.iter_5_noGIL import integrate_cy_noGIL

from functools import partial
import concurrent.futures as ftres

def integrate_cy_noGIL_multi(a: float, b: float, *, n_jobs: int = 2, n_iter: int = 1000) -> float:
    """
    Вычисляет приближённое значение определённого интеграла функции `f`
    на отрезке [a, b] методом левых прямоугольников с использованием
    параллельных вычислений (многопоточности).

    Отрезок [a, b] разбивается на `n_jobs` подотрезков, каждый из которых
    интегрируется независимо в отдельном потоке с использованием
    функции `integrate`. Общее количество итераций (`n_iter`) равномерно
    распределяется между потоками.

    Аргументы
        :param f: Интегрируемая функция одной переменной.
        :param a: Левая граница отрезка интегрирования.
        :param b: Правая граница отрезка интегрирования.
        :param n_jobs: Количество потоков (параллельных задач). Должно быть положительным.
        :param n_iter: Общее количество прямоугольников (итераций) для приближения интеграла.
            Это число равномерно делится между всеми потоками.

    Вывод
        :return: Приближённое значение определённого интеграла,
            полученное как сумма результатов параллельных подвычислений.
    """
    if n_jobs <= 0 or n_iter <= 0:
        raise ValueError("n_jobs и n_iter должны быть положительными")

    executor = ftres.ThreadPoolExecutor(max_workers=n_jobs) # создаваемый пул тредов будет размера n_jobs
    spawn = partial(executor.submit, integrate_cy_noGIL, n_iter = n_iter // n_jobs)

    step = (b - a) / n_jobs
    fs = [spawn(a + i * step, a + (i + 1) * step) for i in range(n_jobs)]    # создаем потоки с помощью генератора

    return sum(list(f.result() for f in ftres.as_completed(fs)))


