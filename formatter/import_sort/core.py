from enum import auto, Enum
from distutils import sysconfig
import os
from pkgutil import iter_modules
from pathlib import Path


def load_standard_library() -> list[str]:
    std_lib = sysconfig.get_python_lib(standard_lib=True)
    return [
        str(path)[len(std_lib)+1:-3].strip()
        for path in Path(std_lib).iterdir()
        if str(path) != "__init__.py" and str(path)[-3:] == ".py"
    ]

STANDARD_LIB = load_standard_library()

def load_third_party_library() -> list[str]:
    return [mod.name for mod in iter_modules()]

THIRD_PARTY_LIB = load_third_party_library()

class ImportType(Enum):
    FUTURE_IMPORT = auto()
    STANDARD_IMPORT = auto()
    THIRD_PARTY_IMPORT = auto()
    LOCAL_IMPORT = auto()

class ImportTypeChecker:

    @staticmethod
    def get_import_type(module_name: str) -> ImportType:
        if module_name == "__future__":
            return ImportType.FUTURE_IMPORT
        # Imports in the format "from . import foobar" return "None" as their module name
        elif module_name == Path.cwd().name or module_name.startswith(".") or module_name == "None":
            return ImportType.LOCAL_IMPORT
        elif module_name in STANDARD_LIB:
            return ImportType.STANDARD_IMPORT
        else:
            return ImportType.THIRD_PARTY_IMPORT
        
        
