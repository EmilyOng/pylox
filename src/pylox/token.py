from pylox.token_type import TokenType


class Token:
    def __init__(self, token_type: TokenType, lexeme: str, literal: any, line: int):
        self.__token_type = token_type
        self.__lexeme = lexeme
        self.__literal = literal
        self.__line = line

    def __str__(self):
        return f"{self.__token_type} {self.__lexeme} {self.__literal}"
