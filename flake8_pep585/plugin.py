from __future__ import annotations

import ast
import sys
from collections.abc import Iterator

from flake8_pep585 import rules
from flake8_pep585.flake_diagnostic import FlakeDiagnostic

rule_classes = (
    rules.DirectImport,
    rules.QualifiedImport,
)


class ImportVisitor(ast.NodeVisitor):
    """Import visitor."""

    enabled: bool

    def __init__(self) -> None:
        self.enabled = False

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:  # noqa: N802
        if (self.enabled or ("__future__" != node.module)):
            return

        for alias in node.names:
            if ("annotations" == alias.name):
                self.enabled = True
                return


class Pep585Plugin:
    name = "flake8-pep585"
    version = "0.1.5.1"
    activation = "auto"
    _enabled: bool

    @classmethod
    def add_options(cls, option_manager) -> None:
        option_manager.add_option("--pep585-activation", default="auto",
                                  action="store", parse_from_config=True,
                                  choices=("auto", "always", "never"), dest="pep585_activation",
                                  help="Activate plugin, auto checks for 'from __future__ import annotations' (default: auto)")

    @classmethod
    def parse_options(cls, options) -> None:
        if ((sys.version_info.major == 3) and (sys.version_info.minor < 7)):
            cls.activation = "never"
        elif ((sys.version_info.major == 3) and (sys.version_info.minor >= 9)):
            cls.activation = "always"
        else:
            cls.activation = options.pep585_activation

    def __init__(self, tree: ast.Module) -> None:
        self._tree = tree
        self._enabled = ("always" == self.activation)

    def __iter__(self) -> Iterator[FlakeDiagnostic]:
        if ((not self._enabled) and ("never" != self.activation)):
            import_visitor = ImportVisitor()
            import_visitor.visit(self._tree)
            self._enabled = import_visitor.enabled

        if (not self._enabled):
            return

        diagnostics: list[FlakeDiagnostic] = []
        report = diagnostics.append
        for rule_cls in rule_classes:
            rule_cls(report).visit(self._tree)
        yield from diagnostics
