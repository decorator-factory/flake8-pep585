# flake8-pep585

This plugin enforces the changes proposed by PEP 585.
Currently, it only works for direct imports from the `typing` module.

```py
from typing import Callable
# PEA001: typing.Callable is deprecated, use collections.abc.Callable instead. See PEP 585 for details
```
