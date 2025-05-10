from argparse import ArgumentParser

from pylox.scanner import scan_tokens


__PROMPT = "> "


def run(source: str):
    tokens = scan_tokens(source)
    for token in tokens:
        print(token)


def run_file(file_path: str):
    with open(file_path, "r") as file:
        run(file.readlines())


def run_interactive():
    while True:
        try:
            line = input(__PROMPT)
        except (EOFError, KeyboardInterrupt):
            break
        if len(line) == 0:
            break
        run(line)


if __name__ == "__main__":
    parser = ArgumentParser(prog="pylox", description="A tree-walk interpreter for Lox")
    parser.add_argument("-f", "--file", required=False)
    parser.add_argument("-i", "--interactive", action="store_true", default=True)
    args = parser.parse_args()

    if args.file is not None:
        run_file(args.file)
    else:
        run_interactive()
