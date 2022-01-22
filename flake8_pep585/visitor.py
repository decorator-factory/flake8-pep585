import ast
from collections.abc import Callable
from types import MappingProxyType

from flake8_pep585.flake_diagnostic import FlakeDiagnostic

_NAME_REPLACEMENTS = MappingProxyType({
    "Tuple": "tuple",
    "List": "list",
    "Dict": "dict",
    "Set": "set",
    "FrozenSet": "frozenset",
    "Type": "type",
    "Deque": "collections.deque",
    "DefaultDict": "collections.defaultdict",
    "OrderedDict": "collections.OrderedDict",
    "Counter": "collections.Counter",
    "ChainMap": "collections.ChainMap",
    "Awaitable": "collections.abc.Awaitable",
    "Coroutine": "collections.abc.Coroutine",
    "AsyncIterable": "collections.abc.AsyncIterable",
    "AsyncIterator": "collections.abc.AsyncIterator",
    "AsyncGenerator": "collections.abc.AsyncGenerator",
    "Iterable": "collections.abc.Iterable",
    "Iterator": "collections.abc.Iterator",
    "Generator": "collections.abc.Generator",
    "Reversible": "collections.abc.Reversible",
    "Container": "collections.abc.Container",
    "Collection": "collections.abc.Collection",
    "Callable": "collections.abc.Callable",
    "AbstractSet": "collections.abc.Set",
    "MutableSet": "collections.abc.MutableSet",
    "Mapping": "collections.abc.Mapping",
    "MutableMapping": "collections.abc.MutableMapping",
    "Sequence": "collections.abc.Sequence",
    "MutableSequence": "collections.abc.MutableSequence",
    "ByteString": "collections.abc.ByteString",
    "MappingView": "collections.abc.MappingView",
    "KeysView": "collections.abc.KeysView",
    "ItemsView": "collections.abc.ItemsView",
    "ValuesView": "collections.abc.ValuesView",
    "ContextManager": "contextlib.AbstractContextManager",
    "Pattern": "re.Pattern",
    "Match": "re.Match",
})


_MESSAGE = "PEA001: typing.{0} is deprecated, use {1} instead. See PEP 585 for details"


class ImportVisitor(ast.NodeVisitor):
    def __init__(self, report_diagnostic: Callable[[FlakeDiagnostic], None]):
        self._report_diagnostic = report_diagnostic

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:  # noqa: N802
        if node.module != "typing":
            return

        for alias in node.names:
            source = alias.name
            replacement = _NAME_REPLACEMENTS.get(source)
            if replacement is None:
                continue
            message = _MESSAGE.format(source, replacement)
            diagnostic = FlakeDiagnostic(node.lineno, node.col_offset, message)
            self._report_diagnostic(diagnostic)
