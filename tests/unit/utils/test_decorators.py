# SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

from collections.abc import Callable
from typing import Any

from earthkit.climate.utils.decorators import compose_decorators, wrap_indicator


def test_wrap_indicator_without_parentheses() -> None:
    """
    Test decorating a function using wrap_indicator without parentheses.

    Ensures that wrap_indicator works as a direct decorator when used without
    parentheses, preserving execution and returning the expected result.

    Returns
    -------
    None
        Does not return any value.
    """

    @wrap_indicator
    def add(a: int, b: int) -> int:
        return a + b

    assert add(1, 2) == 3


def test_wrap_indicator_with_parentheses() -> None:
    """
    Test decorating a function using wrap_indicator with empty parentheses.

    Ensures that wrap_indicator behaves as a decorator factory returning a
    callable decorator that wraps the target function.

    Returns
    -------
    None
        Does not return any value.
    """

    @wrap_indicator()
    def multiply(a: int, b: int) -> int:
        return a * b

    assert multiply(2, 3) == 6


def test_wrap_indicator_with_kwargs() -> None:
    """
    Test decorating a function using wrap_indicator with additional kwargs.

    Ensures that keyword arguments passed to wrap_indicator are forwarded to
    the underlying format_handler.

    Returns
    -------
    None
        Does not return any value.
    """

    @wrap_indicator(kwarg_types={"a": int})
    def custom_func(a: Any) -> Any:
        return a

    assert custom_func(42) == 42


def test_wrap_indicator_direct_call() -> None:
    """
    Test wrapping a function by directly calling wrap_indicator.

    Ensures that wrap_indicator can be invoked directly as a wrapper function
    around another callable.

    Returns
    -------
    None
        Does not return any value.
    """

    def identity(x: str) -> str:
        return x

    wrapped = wrap_indicator(identity)
    assert wrapped("hello") == "hello"


def test_compose_decorators_execution_order() -> None:
    """
    Test that compose_decorators evaluates in Python stacked order.

    Ensures that decorators are applied in innermost-to-outermost order,
    matching standard Python decorator stacking behavior.

    Returns
    -------
    None
        Does not return any value.
    """
    log: list[str] = []

    def dec1(f: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            log.append("dec1_before")
            res = f(*args, **kwargs)
            log.append("dec1_after")
            return res

        return wrapper

    def dec2(f: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            log.append("dec2_before")
            res = f(*args, **kwargs)
            log.append("dec2_after")
            return res

        return wrapper

    composite = compose_decorators(dec1, dec2)

    @composite
    def sample() -> str:
        log.append("func")
        return "ok"

    assert sample() == "ok"
    assert log == ["dec1_before", "dec2_before", "func", "dec2_after", "dec1_after"]


def test_wrap_indicator_with_extra_decorators() -> None:
    """
    Test wrap_indicator with additional decorators passed in.

    Ensures that extra_decorators are composed alongside format_handler.

    Returns
    -------
    None
        Does not return any value.
    """
    called: list[str] = []

    def tracking_decorator(f: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            called.append("tracked")
            return f(*args, **kwargs)

        return wrapper

    @wrap_indicator(extra_decorators=[tracking_decorator])
    def compute(val: int) -> int:
        return val * 10

    assert compute(5) == 50
    assert called == ["tracked"]
