import sys

from formatter.import_sort import ImportFormatter


formatter = ImportFormatter(sys.argv[1:])
formatter.format_imports()