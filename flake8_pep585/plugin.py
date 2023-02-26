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
    def __init__(self) -> None:
        self._found_import = False

    def found_pep563_import(self) -> bool:
        return self._found_import

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:  # noqa: N802
        if self._found_import or node.module != "__future__":
            return

        if "annotations" in {alias.name for alias in node.names}:
            self._found_import = True


class Pep585Plugin:
    name = "flake8-pep585"
    version = "0.1.7"
    _activation = "auto"
    _whitelisted: "frozenset[str]" = frozenset()

    def __init__(self, tree: ast.Module) -> None:
        self._tree = tree

    @classmethod
    def add_options(cls, option_manager) -> None:
        option_manager.add_option(
            "--pep585-activation",
            default="auto",
            action="store",
            parse_from_config=True,
            choices=("auto", "always", "never"),
            dest="pep585_activation",
            help=(
                "Whether to enable plugin on Python 3.7 and 3.8 (always), only "
                + "enable if 'from __future__ import annotations' is present (auto, "
                + "default) or disable (never)"
            ),
        )

        option_manager.add_option(
            "--pep585-whitelisted-symbols",
            default="",
            action="store",
            parse_from_config=True,
            dest="pep585_whitelisted_symbols",
            help="Symbols from `typing` to whitelist from PEP585 checks",
        )

    @classmethod
    def parse_options(cls, options) -> None:
        if sys.version_info < (3, 7):
            cls._activation = "never"
        elif sys.version_info >= (3, 9):
            cls._activation = "always"
        else:
            cls._activation = options.pep585_activation

        cls._whitelisted = frozenset(options.pep585_whitelisted_symbols.split())
        invalid_whitelist_items = {opt for opt in cls._whitelisted if "typing" in opt}
        if invalid_whitelist_items:
            error = "Invalid whitelist item: {0}. Use `X` instead of `typing.X`"
            raise RuntimeError(error.format(invalid_whitelist_items))

    def __iter__(self) -> Iterator[FlakeDiagnostic]:
        if self._activation == "never":
            return

        if self._activation == "auto":
            import_visitor = ImportVisitor()
            import_visitor.visit(self._tree)
            if not import_visitor.found_pep563_import():
                return

        diagnostics: list[FlakeDiagnostic] = []
        report = diagnostics.append
        for rule_cls in rule_classes:
            rule_cls(report, whitelist=self._whitelisted).visit(self._tree)
        yield from diagnostics
