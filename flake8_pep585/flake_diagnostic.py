from typing import NamedTuple


class FlakeDiagnostic(NamedTuple):
    line: int
    col: int
    message: str

    unused: None = None
    # ^ exists for backwards compatibility with a really old version of flake8
