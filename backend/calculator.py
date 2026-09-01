"""Framework-free arithmetic operations for Hello Agent."""


class DivisionByZeroError(ZeroDivisionError):
    """Raised when division is requested with a zero divisor."""


def add(left: float, right: float) -> float:
    """Return the sum of two numbers."""
    return left + right


def subtract(left: float, right: float) -> float:
    """Return the result of subtracting right from left."""
    return left - right


def multiply(left: float, right: float) -> float:
    """Return the product of two numbers."""
    return left * right


def divide(left: float, right: float) -> float:
    """Return the quotient of two numbers or raise a clear division error."""
    if right == 0:
        raise DivisionByZeroError("Cannot divide by zero.")

    return left / right
