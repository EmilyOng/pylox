class ErrorReporter:

    def __init__(self):
        self.has_error = False

    def report(self, line: int, where: str, message: str) -> str:
        self.has_error = True
        return f"[line {line}] Error {where}: {message}"
