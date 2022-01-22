import ast
from collections.abc import Iterator

from flake8_pep585.flake_diagnostic import FlakeDiagnostic
from flake8_pep585.visitor import ImportVisitor


class Pep585Plugin:
    name = "flake8-pep585"
    version = "0.1.3"

    def __init__(self, tree: ast.Module) -> None:
        self._tree = tree

    def __iter__(self) -> Iterator[FlakeDiagnostic]:
        diagnostics: list[FlakeDiagnostic] = []
        ImportVisitor(diagnostics.append).visit(self._tree)
        yield from diagnostics
