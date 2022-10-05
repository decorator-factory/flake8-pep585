from __future__ import annotations

import typing
import typing as ty, typing as ttt


def greet(greeter: typing.Callable[[str], None], name: str) -> None:
    greeter("Hello, {0}!".format(name))


def greet_all(names: ty.Iterable[ty.Union[str, bytes]]) -> None:
    for s in names:
        if isinstance(s, ttt.ByteString):
            greet(print, s.decode("utf-8"))
        else:
            greet(print, s)
