from __future__ import barry_as_FLUFL

from __future__ import nested_scopes
from formatter.import_sort.core import (
    ImportType,
    ImportTypeChecker
)
import ast
from rich.pretty import pprint

from io import TextIOWrapper

from flask import Flask
from itertools import groupby


class ImportParser:

    def __init__(self, filename: str) -> None:
        self.filename: str = filename
        self.import_cache = None

    def parse(self):
        self.get_top_imports()
        self.sort_imports()
        self.construct_new_imports()
        return self.import_cache

    @staticmethod
    def _import_gen(file: str):
        for node in ast.iter_child_nodes(ast.parse(file)):
            if isinstance(node, ast.Import):
                yield node.names[0].name, ast.unparse(node)
            elif isinstance(node, ast.ImportFrom):
                yield node.module, ast.unparse(node)


    def get_top_imports(self):
        file: TextIOWrapper = open(self.filename)
        imports = [(imp, (imp_str, ImportTypeChecker.get_import_type(imp))) for imp, imp_str in self._import_gen(file.read())]
        self.import_cache = imports
        return

    @staticmethod
    def sort_key(imp):
        return imp[1][1].value

    def sort_imports(self):
        list_of_imports = sorted(self.import_cache, key=ImportParser.sort_key)
        section_imports = [list(v) for _, v in groupby(list_of_imports, ImportParser.sort_key)]
        for section in section_imports:
            section.sort()
        self.import_cache = section_imports
        return
    
    def construct_new_imports(self):
        imports = self.import_cache
        self.import_cache = str()
        for section in imports:
            for imp in section:
                self.import_cache += f"{imp[1][0]}\n"
            self.import_cache += "\n"
        return

print(ImportParser("formatter/import_sort/parse.py").parse())