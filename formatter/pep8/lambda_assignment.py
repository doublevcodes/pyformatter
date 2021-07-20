import ast
from typing import Generator


class LambdaParser:

    def __init__(self, source: str) -> None:
        self.source = source

    def get_defs(self):
        lambdas = [assignment for assignment in self._parse() if isinstance(assignment.value, ast.Lambda)]
        for lamb in lambdas:
            yield ast.unparse(
                self.lambda_to_def(
                    lamb.targets[0].id if hasattr(lamb, "targets") else lamb.target.id,
                    lamb.value,
                )
            ), lamb.lineno

    def _parse(self):
        tree: ast.Module = ast.parse(self.source)
        assignments = [node for node in LambdaParser._reduce_module(tree) if isinstance(node, (ast.Assign, ast.AnnAssign))]
        return assignments

    @staticmethod
    def _reduce_module(module: ast.AST) -> Generator[ast.AST, None, None]:
        for node in ast.iter_child_nodes(module):
            if not hasattr(node, "body"):
                yield node
            else:
                for ret_node in LambdaParser._reduce_module(node):
                    yield ret_node

    @staticmethod
    def lambda_to_def(func_name: str, lambda_func: ast.Lambda) -> ast.FunctionDef:
        return ast.fix_missing_locations(ast.FunctionDef(
            name=func_name,
            args=lambda_func.args,
            body=[ast.Return(
                value=lambda_func.body
            )],
            decorator_list=[]
        ))


class LambdaFormatter:

    def __init__(self, filenames: list[str]) -> None:
        self.filenames = filenames

    def format_lambdas(self):

        for filename in self.filenames:     
            with open(filename) as file:
                lambdaparser = LambdaParser(file.read())
                formatted_lambdas = [(func, ln - 1) for func, ln in lambdaparser.get_defs()]

            with open(filename) as file:
                filelines = file.readlines()
                for formatted_lambda in formatted_lambdas:
                    filelines[formatted_lambda[1]] = f"{formatted_lambda[0]}\n"
            
            with open(filename, "w+") as file:
                new_file = "".join(filelines)
                file.write(new_file)

if __name__ == "__main__":
    formatter = LambdaFormatter(["lambda_test.py"])
    formatter.format_lambdas()