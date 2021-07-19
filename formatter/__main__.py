from . import ImportParser

filename = input("Which file should I sort imports for: ")

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
    print(f"Successfully formatted {filename}")