import ast

from ..helpers import _reduce_module

class ComparisonParser:

    def __init__(self, source: str) -> None:
        self.source = source
        return None

    def get_none_comparisons(self):
        comparisons = [
            comparison for comparison in self._parse()
            if (isinstance(comparison.left, ast.Constant) and (comparison.left.value) is None)
            or (any([(isinstance(comparator, ast.Constant) and (comparator.value is None)) for comparator in comparison.comparators]))
        ]
        for comparison in comparisons:
            yield ast.unparse(), comparison.lineno, comparison.col_offset

    def _parse(self):
        tree: ast.Module = ast.parse(self.source)
        comparisons = [node for node in _reduce_module(tree) if isinstance(node, ast.Compare)]
        return comparisons

    @staticmethod
    def fix_none_comparisons(comparison: ast.Compare) -> ast.Compare:
        comparisons = [comp for comp in ComparisonParser.break_down_comparisons(comparison)]
        pass
    # Not finished yet

    @staticmethod
    def break_down_comparisons(comparison: ast.Compare) -> list[ast.Compare]:
        yielded_comps = 0
        comparators = comparison.comparators.insert(0, comparison.left)
        for _ in range(len(comparators)):
            yield ast.Compare(
                left=comparators[yielded_comps],
                ops=[comparison.ops[0]],
                comparators=comparators[yielded_comps + 1]
            )
            yielded_comps += 2
