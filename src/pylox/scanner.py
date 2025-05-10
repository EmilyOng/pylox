from typing import List, Optional

from pylox.reporter import Reporter
from pylox.token import Token
from pylox.token_type import TokenType


class Scanner:
    def __init__(self, source: str):
        self.__source = source

        self.__start = 0
        self.__current = 0
        self.__line = 1

        self.__tokens = []

    def __advance(self) -> None:
        self.__current += 1

    def __is_at_end(self) -> bool:
        return self.__current >= len(self.__source)

    def __peek(self) -> Optional[str]:
        # Performs one-character lookahead but does not consume
        # the character.
        if not self.__is_at_end():
            return self.__source[self.__current]

        return None

    def __add_token(self, token_type: TokenType, literal: str = None) -> None:
        lexeme = self.__source[self.__start : self.__current]
        self.__tokens.append(Token(token_type, lexeme, literal, self.__line))

    def __match(self, expected: str) -> bool:
        if self.__peek() == expected:
            self.__advance()
            return True

        return False

    def __match_string(self) -> str:
        while (not self.__is_at_end()) and self.__peek() != '"':
            if self.__peek() == "\n":
                self.__line += 1
            self.__advance()

        if self.__is_at_end():
            Reporter.report_error(
                self.__line, self.__source[self.__start :], "Unterminated string."
            )
            return

        # Consume the string terminating symbol.
        self.__advance()

        # Trim the surrounding quotes
        return self.__source[self.__start + 1 : self.__current - 1]

    def __scan_token(self) -> None:
        token = self.__source[self.__current]
        self.__advance()

        match token:
            case "(":
                self.__add_token(TokenType.LEFT_PAREN)
            case ")":
                self.__add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.__add_token(TokenType.LEFT_BRACE)
            case "}":
                self.__add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.__add_token(TokenType.COMMA)
            case ".":
                self.__add_token(TokenType.DOT)
            case "-":
                self.__add_token(TokenType.MINUS)
            case "+":
                self.__add_token(TokenType.PLUS)
            case ";":
                self.__add_token(TokenType.SEMICOLON)
            case "*":
                self.__add_token(TokenType.STAR)
            case "!":
                if self.__match("="):
                    self.__add_token(TokenType.BANG_EQUAL)
                else:
                    self.__add_token(TokenType.BANG)
            case "=":
                if self.__match("="):
                    self.__add_token(TokenType.EQUAL_EQUAL)
                else:
                    self.__add_token(TokenType.EQ)
            case "<":
                if self.__match("="):
                    self.__add_token(TokenType.LESS_EQUAL)
                else:
                    self.__add_token(TokenType.LESS)
            case ">":
                if self.__match("="):
                    self.__add_token(TokenType.GREATER_EQUAL)
                else:
                    self.__add_token(TokenType.GREATER)
            case "/":
                if self.__match("/"):
                    # A comment goes until the end of line.
                    while (not self.__is_at_end()) and self.__peek() != "\n":
                        self.__advance()
                else:
                    self.__add_token(TokenType.SLASH)
            case '"':
                self.__add_token(TokenType.STRING, self.__match_string())
            case " " | "\r" | "\t":
                return None
            case "\n":
                self.__line += 1
                return None

        Reporter.report_error(self.__line, token, "Unexpected character.")

    def scan_tokens(self) -> List[Token]:
        while not self.__is_at_end():
            # Indicates the beginning of the next lexeme.
            self.__start = self.__current
            self.__scan_token()

        self.__tokens.append(Token(TokenType.EOF, "", None, self.__line))
        return self.__tokens
