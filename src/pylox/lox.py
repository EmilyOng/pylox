from argparse import ArgumentParser


def run_file(file_path: str):
    with open(file_path, "r") as file:
        pass


def run_interactive():
    pass


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="pylox",
        description="A tree-walk interpreter for Lox"
    )
    parser.add_argument("-f", "--file", required=False)
    parser.add_argument("-i", "--interactive", action="store_true", default=True)
    args = parser.parse_args()
    
    if args.file is not None:
        run_file(args.file)
    else:
        run_interactive()
