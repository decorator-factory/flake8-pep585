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
    "AsyncContextManager": "contextlib.AbstractAsyncContextManager",
    "Pattern": "re.Pattern",
    "Match": "re.Match",
})


_MESSAGE = "PEA001 typing.{0} is deprecated, use {1} instead. See PEP 585 for details"


ReportCallback = Callable[[FlakeDiagnostic], None]


def _report_if_deprecated(
    node: ast.AST,
    imported_name: str,
    report: ReportCallback,
) -> None:
    replacement = _NAME_REPLACEMENTS.get(imported_name)
    if replacement is None:
        return
    message = _MESSAGE.format(imported_name, replacement)
    report(FlakeDiagnostic(node.lineno, node.col_offset, message))


class DirectImport(ast.NodeVisitor):
    def __init__(self, report_diagnostic: ReportCallback):
        self._report_diagnostic = report_diagnostic

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:  # noqa: N802
        if node.module != "typing":
            return

        for alias in node.names:
            _report_if_deprecated(node, alias.name, self._report_diagnostic)


class QualifiedImport(ast.NodeVisitor):
    def __init__(self, report_diagnostic: ReportCallback):
        self._report_diagnostic = report_diagnostic
        self._typing_aliases: set[str] = set()

    def visit_Import(self, node: ast.Import) -> None:  # noqa: N802
        for alias in node.names:
            if alias.name == "typing":
                self._typing_aliases.add(alias.asname or "typing")

    def visit_Attribute(self, node: ast.Attribute) -> None:  # noqa: N802
        if not isinstance(node.value, ast.Name):
            return

        if node.value.id not in self._typing_aliases:
            return

        _report_if_deprecated(node, node.attr, self._report_diagnostic)
