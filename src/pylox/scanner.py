from typing import List, Optional

from pylox.reporter import Reporter
from pylox.token import Token
from pylox.token_type import TokenType


class Scanner:
    __RESERVED_KEYWORDS = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "fun": TokenType.FUN,
        "for": TokenType.FOR,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

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

    def __peek(self, lookahead: int = 0) -> Optional[str]:
        # Performs lookahead but does not consume the character.
        if self.__current + lookahead < len(self.__source):
            return self.__source[self.__current + lookahead]

        return None

    def __add_token(self, token_type: TokenType, literal: str = None) -> None:
        lexeme = self.__source[self.__start : self.__current]
        self.__tokens.append(Token(token_type, lexeme, literal, self.__line))

    def __match(self, expected: str) -> bool:
        if (not self.__is_at_end()) and self.__peek() == expected:
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

    def __match_number(self) -> float:
        while (not self.__is_at_end()) and self.__peek().isdigit():
            self.__advance()

        # Locate the fractional part.
        if (not self.__is_at_end()) and self.__peek() == ".":
            next = self.__peek(1)
            if next is not None and next.isdigit():
                self.__advance()

                while (not self.__is_at_end()) and self.__peek().isdigit():
                    self.__advance()

        return float(self.__source[self.__start : self.__current])

    def __match_identifier(self) -> str:
        while (not self.__is_at_end()) and self.__peek().isalnum():
            self.__advance()

        return self.__source[self.__start : self.__current]

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
                self.__add_token(
                    TokenType.BANG_EQUAL if self.__match("=") else TokenType.BANG
                )
            case "=":
                self.__add_token(
                    TokenType.EQUAL_EQUAL if self.__match("=") else TokenType.EQUAL
                )
            case "<":
                self.__add_token(
                    TokenType.LESS_EQUAL if self.__match("=") else TokenType.LESS
                )
            case ">":
                self.__add_token(
                    TokenType.GREATER_EQUAL if self.__match("=") else TokenType.GREATER
                )
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
                return
            case "\n":
                self.__line += 1
                return
            case _:
                if token.isdigit():
                    self.__add_token(TokenType.NUMBER, self.__match_number())
                elif token.isalpha():
                    lexeme = self.__match_identifier()
                    token_type = Scanner.__RESERVED_KEYWORDS.get(lexeme)
                    if token_type is None:
                        self.__add_token(TokenType.IDENTIFIER)
                    else:
                        self.__add_token(token_type)
                else:
                    Reporter.report_error(self.__line, token, "Unexpected character.")

    def scan_tokens(self) -> List[Token]:
        while not self.__is_at_end():
            # Indicates the beginning of the next lexeme.
            self.__start = self.__current
            self.__scan_token()

        self.__tokens.append(Token(TokenType.EOF, "", None, self.__line))
        return self.__tokens
