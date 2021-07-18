import ast
from io import TextIOWrapper
import itertools
from typing import Generator
from typing import NamedTuple


from formatter.import_sort.core import (
    ImportType,
    ImportTypeChecker
)

class ImportStorageTypeInfo(NamedTuple):
    code: str
    type: ImportType

class ImportStorageType(NamedTuple):
    name: str
    info: ImportStorageTypeInfo

class ImportParser:

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.import_cache = None
        return None

    def parse(self) -> str:
        self.get_top_imports()
        self.sort_imports()
        self.construct_new_imports()
        return self.import_cache

    def get_top_imports(self) -> None:
        file: TextIOWrapper = open(self.filename)
        imports: ImportStorageType = [
            ImportStorageType(
                name=imp, 
                info=ImportStorageTypeInfo(
                    code=imp_str,
                    type=ImportTypeChecker.get_import_type(imp)
                )
            )
            for imp, imp_str in self._import_gen(file.read())
        ]
        self.import_cache = imports
        return None

    def sort_imports(self) -> None:
        section_imports: list[itertools._grouper] = [
            list(v) for _, v in itertools.groupby(
                self.import_cache.sort(key=ImportParser.sort_key),
                ImportParser.sort_key
            )
        ]
        [section.sort() for section in section_imports]
        self.import_cache = section_imports
        return None
    
    def construct_new_imports(self) -> None:
        imports: str = "\n".join(
            [
                 imp.info.code for imp in section
                 for section in self.import_cache
            ]
          )
        self.import_cache: str = imports + "\n\n"
        return None

    @staticmethod
    def _import_gen(file: str) -> Generator[tuple[str, str], None, None]:
        for node in ast.iter_child_nodes(ast.parse(file)):
            if isinstance(node, ast.Import):
                yield node.names[0].name, ast.unparse(node)
            elif isinstance(node, ast.ImportFrom):
                yield node.module, ast.unparse(node)

    @staticmethod
    def sort_key(imp: ImportStorageType) -> int:
        return imp.info.type.value


if __name__ == "__main__":
    print(ImportParser("formatter/import_sort/parse.py").parse())
