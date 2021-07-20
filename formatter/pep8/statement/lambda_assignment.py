import ast
from typing import Generator
from typing import Union

from ..helpers import _reduce_module

class LambdaParser:

    def __init__(self, source: str) -> None:
        self.source = source
        return None

    def get_new_defs(self) -> Generator[tuple[str, int]]:
        lambdas: list[Union[ast.Assign, ast.AnnAssign]] = [assignment for assignment in self._parse()]
        for lamb in lambdas:
            yield (
                ast.unparse(
                    self.lambda_to_def(
                        lamb.targets[0].id
                        if hasattr(lamb, "targets") else lamb.target.id,
                        lamb.value,
                    )
                ),
                lamb.lineno
            )

    def _parse(self) -> list[Union[ast.Assign, ast.AnnAssign]]:
        tree: ast.Module = ast.parse(self.source)
        return [
            node for node in _reduce_module(tree)
            if isinstance(node, (ast.Assign, ast.AnnAssign))
            and isinstance(node.value, ast.Lambda)
        ]

    @staticmethod
    def lambda_to_def(func_name: str, lambda_func: ast.Lambda) -> ast.FunctionDef:
        return ast.fix_missing_locations(
            ast.FunctionDef(
                name=func_name,
                args=lambda_func.args,
                body=[ast.Return(value=lambda_func.body)],
                decorator_list=[]
            )
        )


class LambdaFormatter:

    def __init__(self, filenames: list[str]) -> None:
        self.filenames = filenames
        return None

    def format_lambdas(self) -> None:
        for filename in self.filenames:     
            
            with open(filename, "r+") as file:
                
                lambdaparser = LambdaParser(file.read())
                formatted_lambdas = [
                    (func, ln - 1) for func, ln in lambdaparser.get_new_defs()
                ]

                file.seek(0)
                
                filelines = file.readlines()
                for formatted_lambda in formatted_lambdas:
                    filelines[formatted_lambda[1]] = f"{formatted_lambda[0]}\n"
            
            with open(filename, "w") as file:
                new_file = "".join(filelines)
                file.write(new_file)

        return None

if __name__ == "__main__":
    formatter = LambdaFormatter(["lambda_test.py"])
    formatter.format_lambdas()