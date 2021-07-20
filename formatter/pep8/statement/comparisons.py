import ast
import itertools

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
            yield (
                ast.unparse(
                    ComparisonParser.fix_none_comparisons(comparison)
                ),
                comparison.lineno,
                comparison.col_offset,
                comparison.end_col_offset
            )

    def _parse(self):
        tree: ast.Module = ast.parse(self.source)
        comparisons = [node for node in _reduce_module(tree) if isinstance(node, ast.Compare)]
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
                ops=[FIXED_COMP_OPS[type(comparison.ops[0])]],
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
                new_comparisons = itertools.groupby(
                    [comp for comp in comparisonparser.get_none_comparisons()],
                    lambda _:_[1]
                )
                file.seek(0)
                filelines = file.readlines()

            for _, comparison_group in new_comparisons:
                compgroup = list(comparison_group)
                line = filelines[compgroup[0][1]-1]
                split_list = []
                for comparison in compgroup:
                    if compgroup.index(comparison) == 0:
                        split_list.append(line[:comparison[2]])
                    else:
                        idx = compgroup.index(comparison)
                        split_list.append(line[compgroup[idx-1][3]:comparison[2]])
                split_list.append(line[compgroup[-1][3]:])
                split_line = split_list
                for i, comparison in enumerate(compgroup):
                    split_line.insert((2 * (i + 1)) - 1, comparison[0])
                line = "".join(split_line)
                filelines[compgroup[0][1]]
            
            with open(filename, "w") as file:
                



if __name__ == "__main__":
    fmt = ComparisonFormatter(["test.py"])
    fmt.format_comparisons()