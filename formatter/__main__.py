import sys

from formatter.import_sort import ImportFormatter
from formatter.pep8.statement import ComparisonFormatter, LambdaFormatter
from formatter.pep8.style import WhitespaceFormatter

formatter = ImportFormatter(sys.argv[1:])
formatter.format_imports()

formatter = ComparisonFormatter(sys.argv[1:])
formatter.format_comparisons()

formatter = LambdaFormatter(sys.argv[1:])
formatter.format_lambdas()

formatter = WhitespaceFormatter(sys.argv[1:])
formatter.format_whitespace()