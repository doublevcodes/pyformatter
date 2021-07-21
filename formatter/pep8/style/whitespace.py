import ast

from formatter.pep8.helpers import _reduce_module, _replace_tokens

class WhitespaceParser:

    def __init__(self, source, filename) -> None:
        self.source = source
        self.filename = filename

    def ensure_operator_space(self):
        binops = [binop for binop in self._parse()]
        for binop in binops:
            yield (
                ast.unparse(binop),
                binop.lineno,
                binop.end_lineno,
                binop.col_offset,
                binop.end_col_offset
            )
    
    def ensure_newline(self):
        filecontents = self.source.rstrip()
        filecontents += "\n"
        with open(self.filename, "w") as file:
            file.write(filecontents)

    def _parse(self):
        tree: ast.Module = ast.parse(self.source)
        binops = [node for node in _reduce_module(tree) if isinstance(node, ast.BinOp)]
        return binops

class WhitespaceFormatter:
    
    def __init__(self, filenames: list[str]) -> None:
        self.filenames = filenames

    def format_whitespace(self):
        for filename in self.filenames:
            whitespaceparser = WhitespaceParser(open(filename).read(), filename)
            whitespaceparser.ensure_newline()
            fixed_ops = [op for op in whitespaceparser.ensure_operator_space()]
            _replace_tokens(filename, fixed_ops)

if __name__ == "__main__":
    w = WhitespaceFormatter(["test.py"])
    w.format_whitespace()