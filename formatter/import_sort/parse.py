import ast
from typing import Generator
from typing import NamedTuple

import itertools

from formatter.import_sort.core import ImportType, ImportTypeChecker


class ImportStorageTypeInfo(NamedTuple):
    """
    Holds data held in the `info` field of an `ImportStorageType` instance.
    """
    code: str
    type: ImportType


class ImportStorageType(NamedTuple):
    """
    Represents an import.
    """
    name: str
    info: ImportStorageTypeInfo


class ImportParser:
    """
    Parses the imports in source code and the normalises them according to PEP8.

    The import parser sorts imports in source code in three main steps. The first step
    is to retrieve all the imports at the top of the file. This is the job of the
    `ImportParser.get_top_imports` method. Secondly we sort the imports by sections,
    (where the order of the sections is: __future__ imports, standard library imports,
    third party imports and local imports. Each of these individual sections is sorted
    alphabetically. Finally, from these sorted imports, we construct new imports using
    the magical `ast.parse` function.
    """

    def __init__(self, source: str) -> None:
        """
        Creates an import parser.
        
        This specific instance of the parser can only parse the source code passed in
        through the `source` argument.
        """

        self.source = source

        # The import cache is where the instance stores its sorted or partially sorted
        # imports, whatever state they are in.
        self.import_cache = None
        return None

    def parse(self) -> str:
        """
        Executes the process explained in the class docstring.

        Steps taken by this method get existing imports and then sort them returning
        new import statements as string which can be inserted at the top of the file
        instead of the existing imports.
        """

        self.get_top_imports()
        self.sort_imports()
        self.construct_new_imports()
        return self.import_cache

    def get_top_imports(self) -> None:
        """
        Grabs the imports at the top of the source code.

        Creates a list of `ImportStorageType`s using the imports generated from the
        `ImportParser._import_gen` staticmethod generator. The `import_cache` is then
        set to this list.
        """
        
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
        """
        Sorts imports held in the `import_cache`.

        The `import_cache` currently contains a list of `ImportStorageType` instances,
        each representing an import at the top of `source`. The first list
        comprehension sorts the list by `ImportParser.sort_key` and then groups them
        according to the type of import (accessible through
        `ImportStorageType.info.type.value` because the `ImportStorageType.info.type`
        is an `enum.Enum`). Then sorts the grouped import list alphabetically.
        """

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
        """
        Creates a string of imports which can be inserted into a file.

        It simply iterates through each import and replaces it with
        that import's code; inserting a newline whenever it gets to the end of a 
        section and making sure there are tow new lines at the end of the string
        in order to abide by PEP8.
        """

        imports: str = ""
        for section in self.import_cache:
            for imp in section:
                imports += f"{imp.info.code}\n"
            imports += "\n"

        self.import_cache: str = imports
        return None

    @staticmethod
    def _import_gen(file: str) -> Generator[tuple[str, str], None, None]:
        """
        Constructs an AST of the file and returns tuples of imports
        followed by their respective "in code" forms.
        """
        for node in ast.iter_child_nodes(ast.parse(file)):
            if isinstance(node, ast.Import):
                yield node.names[0].name.split(".")[0], ast.unparse(node)
            elif isinstance(node, ast.ImportFrom):
                yield str(node.module).split(".")[0], ast.unparse(node)

    @staticmethod
    def sort_key(imp: ImportStorageType) -> int:
        """
        Used to sort lists of imports.
        
        The import's type in an enum which corresponds to an integer value
        representing the priority of the import.
        """
        return imp.info.type.value
