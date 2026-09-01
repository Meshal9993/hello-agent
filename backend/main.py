"""FastAPI paths for the Hello Agent calculator."""

from fastapi import FastAPI, HTTPException, status

from calculator import DivisionByZeroError, add, divide, multiply, subtract

app = FastAPI(title="Hello Agent Calculator")


@app.get("/add")
def add_numbers(a: float, b: float) -> dict[str, float]:
    """Add the two query parameters."""
    return {"result": add(a, b)}


@app.get("/subtract")
def subtract_numbers(a: float, b: float) -> dict[str, float]:
    """Subtract b from a."""
    return {"result": subtract(a, b)}


@app.get("/multiply")
def multiply_numbers(a: float, b: float) -> dict[str, float]:
    """Multiply the two query parameters."""
    return {"result": multiply(a, b)}


@app.get("/divide")
def divide_numbers(a: float, b: float) -> dict[str, float]:
    """Divide a by b, returning a client error for a zero divisor."""
    try:
        return {"result": divide(a, b)}
    except DivisionByZeroError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error
