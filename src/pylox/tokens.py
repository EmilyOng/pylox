from dataclasses import dataclass
from pylox.token_type import TokenType


@dataclass
class Token:
    token_type: TokenType
    lexeme: str
    literal: any
    line: int

    def __str__(self):
        return f"{self.token_type} {self.lexeme} {self.literal}"
