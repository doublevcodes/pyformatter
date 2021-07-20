import ast
from typing import Generator

def _reduce_module(module: ast.AST) -> Generator[ast.AST, None, None]:
    for node in ast.iter_child_nodes(module):
        if isinstance(node, ast.If):
            for node_ in _reduce_module(node.test):
                yield node_
        if not hasattr(node, "body"):
            yield node
        else:
            for ret_node in _reduce_module(node):
                yield ret_node