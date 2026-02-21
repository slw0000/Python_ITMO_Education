import math
import doctest
import pytest

from iter_2_threads import integrate_async as integrate
import integrate as integr


def test_integrate_doctests():
    doctest.testmod(m=integr, raise_on_error=True)

def test_cos_integral():
    result = integrate(math.cos, 0, math.pi / 2, n_iter=1000)
    assert abs(result - 1.0) < 0.01

def test_quadratic_function():
    result = integrate(lambda x: x ** 2, 0, 1, n_iter=10000)
    assert abs(result - 1/3) < 0.001

def test_linear_function():
    result = integrate(lambda x: x, 0, 1, n_iter=10000)
    assert abs(result - 0.5) < 0.001

def test_invalid_n_iter():
    with pytest.raises(ValueError):
        integrate(math.sin, 0, 1, n_iter=0)

def test_invalid_interval():
    with pytest.raises(ValueError):
        integrate(math.sin, 2, 1)