import ast
import itertools

from formatter.pep8.helpers import _reduce_module, _replace_tokens

class ComparisonParser:

    def __init__(self, source: str) -> None:
        self.source = source
        return None

    def get_comparisons(self):
        for comp in self.get_none_comparisons():
            yield comp

    def get_none_comparisons(self):
        comparisons = [comparison for comparison in self._parse()]
        none_comparisons = [
            comparison for comparison in comparisons
            if (isinstance(comparison.left, ast.Constant) and (comparison.left.value) is None)
            or (any((isinstance(comparator, ast.Constant) and (comparator.value is None)) for comparator in comparison.comparators))
        ]
        for comparison in none_comparisons:
            yield (
                ast.unparse(
                    ComparisonParser.fix_none_comparisons(comparison)
                ),
                comparison.lineno,
                comparison.end_lineno,
                comparison.col_offset,
                comparison.end_col_offset
            )

    def _parse(self):
        tree: ast.Module = ast.parse(self.source)
        comparisons = list(set([node for node in _reduce_module(tree) if isinstance(node, ast.Compare)]))
        return comparisons

    @staticmethod
    def fix_none_comparisons(comparison: ast.Compare) -> ast.Compare:

        FIXED_COMP_OPS = {
            ast.Eq: ast.Is(),
            ast.NotEq: ast.IsNot(),
        }

        if comparison.ops[0] not in (ast.Is, ast.IsNot):
            return ast.Compare(
                left=comparison.left,
                ops=[FIXED_COMP_OPS.get(type(comparison.ops[0]), comparison.ops[0])],
                comparators=comparison.comparators
            )
        else:
            return comparison
    

class ComparisonFormatter:

    def __init__(self, filenames) -> None:
        self.filenames = filenames

    def format_comparisons(self) -> None:

        for filename in self.filenames:
            with open(filename, "r+") as file:
                comparisonparser = ComparisonParser(file.read())
                new_comparisons = [comp for comp in comparisonparser.get_comparisons()]
                _replace_tokens(filename, new_comparisons)