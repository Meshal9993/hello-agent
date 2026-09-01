import pytest

from calculator import DivisionByZeroError, add, divide, multiply, subtract


def test_add() -> None:
    assert add(2, 3) == 5


def test_subtract() -> None:
    assert subtract(7, 4) == 3


def test_multiply() -> None:
    assert multiply(6, 5) == 30


def test_multiply_with_negative_decimal() -> None:
    assert multiply(-2.5, 4) == -10


def test_divide() -> None:
    assert divide(9, 3) == 3


def test_divide_by_zero_raises_intentional_error() -> None:
    with pytest.raises(DivisionByZeroError, match="Cannot divide by zero"):
        divide(1, 0)
