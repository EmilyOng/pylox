from typing import List

from pylox.reporter import Reporter
from pylox.token import Token
from pylox.token_type import TokenType


def scan_token(token: str, line: int) -> TokenType:
    match token:
        case "(":
            return TokenType.LEFT_PAREN
        case ")":
            return TokenType.RIGHT_PAREN
        case "{":
            return TokenType.LEFT_BRACE
        case "}":
            return TokenType.RIGHT_BRACE
        case ",":
            return TokenType.COMMA
        case ".":
            return TokenType.DOT
        case "-":
            return TokenType.MINUS
        case "+":
            return TokenType.PLUS
        case ";":
            return TokenType.SEMICOLON
        case "*":
            return TokenType.STAR
    Reporter.report_error(line, "", "Unexpected character")


def scan_tokens(source: str) -> List[str]:
    start = 0
    current = 0
    line = 1

    tokens: List[str] = []

    while current < len(source):
        # Indicates the beginning of the next lexeme.
        start = current
        token_type = scan_token(source[current], line)
        text = source[start : current + 1]
        tokens.append(Token(token_type, text, None, line))

        current += 1

    tokens.append(Token(TokenType.EOF, "", None, line))
    return tokens
