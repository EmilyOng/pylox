class ParseException(Exception):
    def __init__(self):
        super().__init__()


class Reporter:
    __has_error = False

    @staticmethod
    def report_error(line: int, where: str, message: str) -> str:
        Reporter.__has_error = True
        if len(where) > 0:
            print(f"[line {line}] Error {where}: {message}")
        else:
            print(f"[line {line}] Error: {message}")

    @staticmethod
    def has_error() -> bool:
        return Reporter.__has_error

    @staticmethod
    def reset_error() -> None:
        Reporter.__has_error = False
