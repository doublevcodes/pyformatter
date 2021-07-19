import ast
from typing import Generator
from typing import NamedTuple

import itertools

from formatter.import_sort.core import ImportType, ImportTypeChecker


class ImportStorageTypeInfo(NamedTuple):
    code: str
    type: ImportType

class ImportStorageType(NamedTuple):
    name: str
    info: ImportStorageTypeInfo

class ImportParser:

    def __init__(self, source: str) -> None:
        self.source = source
        self.import_cache = None
        return None

    def parse(self) -> str:
        self.get_top_imports()
        self.sort_imports()
        self.construct_new_imports()
        return self.import_cache

    def get_top_imports(self) -> None:
        imports: ImportStorageType = [
            ImportStorageType(
                name=imp, 
                info=ImportStorageTypeInfo(
                    code=imp_str,
                    type=ImportTypeChecker.get_import_type(imp)
                )
            )
            for imp, imp_str in self._import_gen(self.source)
        ]
        self.import_cache = imports
        return None

    def sort_imports(self) -> None:
        section_imports: list[itertools._grouper] = [
            list(v) for _, v in itertools.groupby(
                sorted(self.import_cache, key=ImportParser.sort_key),
                ImportParser.sort_key
            )
        ]
        [section.sort() for section in section_imports]
        self.import_cache = section_imports
        return None
    
    def construct_new_imports(self) -> None:
        imports: str = ""
        for section in self.import_cache:
            for imp in section:
                imports += f"{imp.info.code}\n"
            imports += "\n"
        self.import_cache: str = imports
        return None

    @staticmethod
    def _import_gen(file: str) -> Generator[tuple[str, str], None, None]:
        for node in ast.iter_child_nodes(ast.parse(file)):
            if isinstance(node, ast.Import):
                yield node.names[0].name.split(".")[0], ast.unparse(node)
            elif isinstance(node, ast.ImportFrom):
                yield str(node.module).split(".")[0], ast.unparse(node)

    @staticmethod
    def sort_key(imp: ImportStorageType) -> int:
        return imp.info.type.value
