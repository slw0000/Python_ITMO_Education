from timeit import repeat
from tabulate import tabulate
from integrate import integrate
from iter_2_threads import integrate_async
from iter_3_processes import integrate_async_processes
from iter_4_cython.iter_4_cython import integrate_cy
from iter_4_2_cython_w_cos.iter_4_2_cython_w_cos import integrate_cy_cos
from iter_5_noGIL_multiThreading import integrate_cy_noGIL_multi

import math

def benchmark():
    a, b = 0, 10000
    n_iter = 10_000_000

    def timed_run(func, *args, **kwargs):
        times = repeat(lambda: func(*args, **kwargs), number=1, repeat=5)
        return round(min(times), 6)

    t_seq = timed_run(integrate, math.cos, a, b, n_iter=n_iter)
    t_par2 = timed_run(integrate_async, math.cos, a, b, n_jobs=2, n_iter=n_iter)
    t_par4 = timed_run(integrate_async, math.cos, a, b, n_jobs=4, n_iter=n_iter)
    t_par8 = timed_run(integrate_async, math.cos, a, b, n_jobs=8, n_iter=n_iter)
    t_proc2 = timed_run(integrate_async_processes, math.cos, a, b, n_jobs=2, n_iter=n_iter)
    t_proc4 = timed_run(integrate_async_processes, math.cos, a, b, n_jobs=4, n_iter=n_iter)
    t_proc8 = timed_run(integrate_async_processes, math.cos, a, b, n_jobs=8, n_iter=n_iter)
    t_cy = timed_run(integrate_cy, math.cos, a, b, n_iter=n_iter)
    t_cy_cos = timed_run(integrate_cy_cos, a, b, n_iter=n_iter)
    t_noGIL2 = timed_run(integrate_cy_noGIL_multi, a, b, n_jobs=2, n_iter=n_iter)
    t_noGIL4 = timed_run(integrate_cy_noGIL_multi, a, b, n_jobs=4, n_iter=n_iter)
    t_noGIL8 = timed_run(integrate_cy_noGIL_multi, a, b, n_jobs=8, n_iter=n_iter)

    data = [
        ["integrate (последовательно)", t_seq, "---", "---", "---"],
        ["integrate_async (многопоточность)", "---", t_par2, t_par4, t_par8],
        ["integrate_async_processes (многопроцессорность)", "---", t_proc2, t_proc4, t_proc8],
        ["integrate_cy (Cython)", t_cy, "---", "---", "---"],
        ["integrate_cy_w_cos (Cython со встроенной ф-ей косинуса)", t_cy_cos, "---", "---", "---"],
        ["integrate_cy_noGIL (многопоточность + noGIL + Cython)", "---", t_noGIL2, t_noGIL4, t_noGIL8]
    ]

    print(f"\n=== Интеграл функции math.cos на интервале от {a} до {b} c шагом n_iter = {n_iter} ===\n")
    print(tabulate(data, headers=["Метод", "Время (секунды)", "2 потока", "4 потока", "8 потоков"], tablefmt="fancy_grid", floatfmt=".4f"))

if __name__ == "__main__":
    benchmark()




