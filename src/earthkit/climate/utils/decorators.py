# SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

from collections.abc import Callable
from typing import Any

from earthkit.utils.decorators import format_handler


def _compose_decorators(
    *decorators: Callable[[Callable[..., Any]], Callable[..., Any]],
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Compose multiple decorators into a single decorator.

    Decorators are applied from right to left (innermost to outermost),
    matching Python's standard stacked decorator evaluation order.

    Parameters
    ----------
    *decorators : Callable[[Callable[..., Any]], Callable[..., Any]]
        Decorators to compose.

    Returns
    -------
    Callable[[Callable[..., Any]], Callable[..., Any]]
        A combined decorator function.
    """

    def composite(func: Callable[..., Any]) -> Callable[..., Any]:
        wrapped = func
        for dec in reversed(decorators):
            wrapped = dec(wrapped)
        return wrapped

    return composite


def wrap_indicator(
    func: Callable[..., Any] | None = None,
    extra_decorators: list[Callable[[Callable[..., Any]], Callable[..., Any]]] | None = None,
    **kwargs: Any,
) -> Callable[..., Any]:
    """
    Wrap a climate indicator function with standard Earthkit transformations.

    Applies input format and type handling to future-proof indicator wrappers,
    allowing future decorators (such as metadata handling, provenance, or unit
    transformations) to be composed transparently.

    Parameters
    ----------
    func : Callable[..., Any] | None, default=None
        The indicator function to decorate. If None, returns a decorator.
    extra_decorators : list[Callable[[Callable[..., Any]], Callable[..., Any]]] | None, default=None
        Optional list of additional decorators to apply to the indicator.
    **kwargs : Any
        Optional arguments forwarded to the underlying format handler or decorators.

    Returns
    -------
    Callable[..., Any]
        The wrapped indicator function or decorator.
    """
    chain: list[Callable[[Callable[..., Any]], Callable[..., Any]]] = [
        format_handler(**kwargs),
        *(extra_decorators or []),
    ]
    decorator = _compose_decorators(*chain)

    if func is not None:
        return decorator(func)
    return decorator
