import ast
from io import TextIOWrapper
from itertools import groupby
from typing import Generator

from formatter.import_sort.core import (
    ImportType,
    ImportTypeChecker
)


class ImportParser:

    ImportFormatType = list[tuple[str, tuple[str, ImportType]]]

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.import_cache = None
        return None

    def parse(self) -> str:
        self.get_top_imports()
        self.sort_imports()
        self.construct_new_imports()
        return self.import_cache

    @staticmethod
    def _import_gen(file: str) -> Generator[tuple[str, str], None, None]:
        for node in ast.iter_child_nodes(ast.parse(file)):
            if isinstance(node, ast.Import):
                yield node.names[0].name, ast.unparse(node)
            elif isinstance(node, ast.ImportFrom):
                yield node.module, ast.unparse(node)


    def get_top_imports(self) -> None:
        file: TextIOWrapper = open(self.filename)
        imports: ImportFormatType = [
            (imp, (imp_str, ImportTypeChecker.get_import_type(imp)))
            for imp, imp_str in self._import_gen(file.read())
        ]
        self.import_cache = imports
        return None

    @staticmethod
    def sort_key(imp) -> int:
        return imp[1][1].value

    def sort_imports(self) -> None:
        list_of_imports: ImportFormatType = sorted(self.import_cache, key=ImportParser.sort_key)
        section_imports = [list(v) for _, v in groupby(list_of_imports, ImportParser.sort_key)]
        [section.sort() for section in section_imports]
        self.import_cache = section_imports
        return None
    
    def construct_new_imports(self):
        imports: str = "\n".join([imp[1][0] for imp in section for section in self.import_cache])
        self.import_cache = imports + "\n\n"
        return None

if __name__ == "__main__":
    print(ImportParser("formatter/import_sort/parse.py").parse())
