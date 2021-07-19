from formatter.import_sort.parse import ImportParser

class ImportFormatter:

    def __init__(self, filenames: list[str]) -> None:
        self.filenames = filenames

    def format_imports(self) -> None:

        filenames = self.filenames

        for filename in filenames:
            with open(filename, "r") as file:
                importparser = ImportParser(file.read())
                formatted_imps = importparser.parse()

            with open(filename, "r") as file:
                line_counter = 0
                for line in file.readlines():
                    if line.startswith(("from", "import")) or line == "\n":
                        line_counter += 1
                    else:
                        break
                file.seek(0)
                code_content = "".join(file.readlines()[line_counter:])

            with open(filename, "w+") as file:
                file.write(
                    f"{formatted_imps}\n{code_content}"
                )
        
        return None