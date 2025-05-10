from argparse import ArgumentParser
import sys

from pylox.reporter import Reporter
from pylox.scanner import Scanner


__PROMPT = "> "


def run(source: str):
    scanner = Scanner(source)

    for token in scanner.scan_tokens():
        print(token)


def run_file(file_path: str):
    with open(file_path, "r") as file:
        run(file.readlines())

        if Reporter.has_error:
            sys.exit()


def run_interactive():
    while True:
        try:
            line = input(__PROMPT)
        except (EOFError, KeyboardInterrupt):
            break
        if len(line) == 0:
            break

        run(line)
        Reporter.reset_error()


if __name__ == "__main__":
    parser = ArgumentParser(prog="pylox", description="A tree-walk interpreter for Lox")
    parser.add_argument("-f", "--file", required=False)
    parser.add_argument("-i", "--interactive", action="store_true", default=True)
    args = parser.parse_args()

    if args.file is not None:
        run_file(args.file)
    elif args.interactive:
        run_interactive()
