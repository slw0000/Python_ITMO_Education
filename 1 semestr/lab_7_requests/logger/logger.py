import functools
import logging
import sys


def logByHandle(handle, message, level="INFO"):
    """
    Функция для логирования сообщений разными способами
    Args:
        handle: способ логирования
        message: сообщение для логирования
        level: уровень логирования
    """
    if isinstance(handle, logging.Logger):
        if level == "ERROR":
            handle.error(message)
        else:
            handle.info(message)

    else:
        try:
            handle.write(f"{level}: {message}\n")
        except:
            sys.stderr.write(f"[Unknown handle] {level}: {message}\n")



def logger(func=None, *, handle=sys.stdout):
    """
    Декоратор, с помощью которого логируются ошибки обёрнутой функции
    Args:
        func: функци которую требуется обернуть
        handle: способ логирования
    Returns:
        wrapper: обёрнутая функция func
    """
    if func is None:
        return lambda func: logger(func, handle=handle)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Запись о начале работы функции
        all_args = [repr(a) for a in args]
        all_kwargs = [f"{k}={repr(v)}" for k, v in kwargs.items()]
        all_args_kwargs = ", ".join(all_args + all_kwargs)
        start_msg = f"Вызов функции {func.__name__}({all_args_kwargs})"
        logByHandle(handle, start_msg)

        try:
            result = func(*args, **kwargs)
            # Запись о успешном выполнении работы
            res_msg = f"Функция {func.__name__} отработала успешно! Результат: {result}"
            logByHandle(handle, res_msg)
            return result

        except Exception as e:
            # Запись об ошибке
            err_msg = f"Ошибка в {func.__name__}: {type(e).__name__}: {e}"
            logByHandle(handle, err_msg, level="ERROR")

            raise

    return wrapper


