# flake8-pep585

This plugin enforces the changes proposed by [PEP 585](https://peps.python.org/pep-0585/).

## What does PEP 585 change?

Before PEP 585, you had to import stuff from `typing` to annotate some objects from the standard library:

- For context managers, you'd import `typing.ContextManager`
- For lists, you'd import `typing.List`
- For callables, you'd import `typing.Callable`
- ...and so on

With PEP 585, you can now use classes already present in the standard library. For example:
- For a context manager giving an `int`, use `contextlib.AbstractContextManager[int]`
- For a `list` of `dict`s mapping `str`s to `int`s, use `list[dict[str, int]]`
- For a callable taking a `float` and returning an `int`, use `collections.abc.Callable[[float], int]`

`typing.List`, `typing.Callable` etc. are now deprecated. This is pretty hard to discover, since these
imports don't cause a deprecation warning. IDEs don't help either: the "auto-import" feature often suggests
importing a deprecated item.

This plugin lets you find these deprecated imports.

## Examples

### Direct import
```py
from typing import Callable
```
```
PEA001 typing.Callable is deprecated, use collections.abc.Callable instead. See PEP 585 for details
```

### Qualified import
```py
from datetime import time
import typing as ty

def construct_time(match: ty.Match) -> time:
    return time(
        hour=int(match["hour"]),
        minute=int(match["minute"]),
    )
```
```
PEA001 typing.Match is deprecated, use re.Match instead. See PEP 585 for details
```

# Installation

1. Make sure you have `flake8` installed
2. Run `pip install flake8-pep585`
3. Run `flake8` on your code

# Configuration

Via your `setup.cfg` file:
```toml
[flake8]
pep585-activation = always  # "always", "auto" or "never"

# Symbols that you're okay with being imported from `typing`
pep585-whitelisted-symbols =
    Callable
    Match
    Pattern
```

Via the CLI:
```
python -m flake8 --pep585-activation=always your_project/file.py
```

This only changes how the plugin behaves on Python 3.7.x and Python 3.8.x. By default ("auto"), it will be enabled
if a `from __future__ import annotations` line is found.
