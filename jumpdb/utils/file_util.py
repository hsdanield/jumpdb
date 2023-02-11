def read_file(path_file: str):
    with open(path_file, "r") as file:
        content = file.read()

    return content
