import ast
from collections.abc import Iterator

from flake8_pep585 import rules
from flake8_pep585.flake_diagnostic import FlakeDiagnostic

rule_classes = (
    rules.DirectImport,
    rules.QualifiedImport,
)


class Pep585Plugin:
    name = "flake8-pep585"
    version = "0.1.5"

    def __init__(self, tree: ast.Module) -> None:
        self._tree = tree

    def __iter__(self) -> Iterator[FlakeDiagnostic]:
        diagnostics: list[FlakeDiagnostic] = []
        report = diagnostics.append
        for rule_cls in rule_classes:
            rule_cls(report).visit(self._tree)
        yield from diagnostics
