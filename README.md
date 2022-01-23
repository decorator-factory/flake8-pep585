# flake8-pep585

This plugin enforces the changes proposed by PEP 585.

```py
from typing import Callable
# PEA001: typing.Callable is deprecated, use collections.abc.Callable instead. See PEP 585 for details

import typing as ty
ty.Match
# PEA001: typing.Match is deprecated, use re.Match instead. See PEP 585 for details
```
