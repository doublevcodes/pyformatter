import ast
import itertools
from typing import Generator

from rich.pretty import pprint

def _reduce_module(module: ast.AST) -> Generator[ast.AST, None, None]:
    for node in ast.iter_child_nodes(module):
        yield node
        for nod in ast.iter_child_nodes(node):
            yield nod
            for no in _reduce_module(nod):
                yield no
        try:
            for _, field in ast.iter_fields(node):
                yield field
                for fld in _reduce_module(field):
                    yield fld
        except AttributeError:
            continue

def _replace_tokens(filename: str, tokens: list[tuple[str, int, int, int]]):

    with open(filename, "r") as file:
        filelines = file.readlines()

    tokens = itertools.groupby(tokens, lambda _:_[1])

    counter = 0

    for lineno, token_group in tokens:
            tokgroup = list(token_group)

            # Select the line/lines for the current group
            lines = "".join(filelines[
                (lineno-1):sorted(tokgroup, key=lambda _:_[2])[0][2]
            ])
            
            
            split_list = []
            for tok in tokgroup:
                if tokgroup.index(tok) == 0:
                    split_list.append(lines[:tok[3]])
                else:
                    idx = tokgroup.index(tok)
                    split_list.append(lines[tokgroup[idx-1][4]:tok[3]])
            split_list.append(lines[tok[4]:])

            for i, tok in enumerate(tokgroup):
                split_list.insert(2 * (i + 1) - 1, tok[0])

            lines = "".join(split_list)

            for i in range(lineno-1, sorted(tokgroup, key=lambda _:_[2])[0][2]):
                filelines.pop(i)

            filelines.insert(lineno-1, lines)
            
    with open(filename, "w") as file:
        file.write("".join(filelines))

