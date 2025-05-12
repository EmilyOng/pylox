from typing import List, Optional

from pylox.expression import (
    BinaryExpression,
    Expression,
    GroupingExpression,
    LiteralExpression,
    UnaryExpression,
)
from pylox.reporter import ParseException, Reporter
from pylox.token_type import TokenType
from pylox.tokens import Token


class Parser:
    def __init__(self, tokens: List[Token]):
        self.__tokens: List[Token] = tokens
        self.__current = 0

    def __match(self, *token_types: TokenType) -> bool:
        for token_type in token_types:
            if self.__check(token_type):
                self.__advance()
                return True

        return False

    def __check(self, token_type: TokenType) -> bool:
        if self.__is_at_end():
            return False
        return self.__peek().token_type == token_type

    def __advance(self) -> None:
        if not self.__is_at_end():
            self.__current += 1
        return self.__previous()

    def __previous(self) -> Token:
        return self.__tokens[self.__current - 1]

    def __is_at_end(self) -> bool:
        return self.__peek().token_type == TokenType.EOF

    def __peek(self) -> Token:
        return self.__tokens[self.__current]

    def __consume(self, token_type: TokenType, message: str) -> None:
        if self.__check(token_type):
            return self.__advance()

        return self.__error(self.__peek(), message)

    def __error(self, token: Token, message: str) -> Optional[ParseException]:
        if token.token_type == TokenType.EOF:
            Reporter.report_error(token.line, " at end", message)
        else:
            Reporter.report_error(token.line, f"at '{token.lexeme}'", message)
        return ParseException()

    def __synchronize(self) -> None:
        self.__advance()

        while not self.__is_at_end():
            if self.__previous().token_type == TokenType.SEMICOLON:
                return
            match self.__peek().token_type:
                case (
                    TokenType.CLASS
                    | TokenType.FUN
                    | TokenType.VAR
                    | TokenType.FOR
                    | TokenType.IF
                    | TokenType.WHILE
                    | TokenType.PRINT
                    | TokenType.RETURN
                ):
                    return
            self.__advance()

    def __expression(self) -> Expression:
        return self.__equality()

    def __equality(self) -> Expression:
        expression = self.__comparison()

        while self.__match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.__previous()
            right = self.__comparison()
            expression = BinaryExpression(expression, operator, right)

        return expression

    def __comparison(self) -> Expression:
        expression = self.__term()

        while self.__match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator = self.__previous()
            right = self.__term()
            expression = BinaryExpression(expression, operator, right)

        return expression

    def __term(self) -> Expression:
        expression = self.__factor()

        while self.__match(TokenType.MINUS, TokenType.PLUS):
            operator = self.__previous()
            right = self.__factor()
            expression = BinaryExpression(expression, operator, right)

        return expression

    def __factor(self) -> Expression:
        expression = self.__unary()

        while self.__match(TokenType.SLASH, TokenType.STAR):
            operator = self.__previous()
            right = self.__unary()
            expression = BinaryExpression(expression, operator, right)

        return expression

    def __unary(self) -> Expression:
        if self.__match(TokenType.BANG, TokenType.MINUS):
            operator = self.__previous()
            right = self.__unary()
            return UnaryExpression(operator, right)
        else:
            return self.__primary()

    def __primary(self) -> Expression:
        if self.__match(TokenType.FALSE):
            return LiteralExpression(False)
        elif self.__match(TokenType.TRUE):
            return LiteralExpression(True)
        elif self.__match(TokenType.NIL):
            return LiteralExpression(None)
        elif self.__match(TokenType.NUMBER, TokenType.STRING):
            return LiteralExpression(self.__previous().literal)
        elif self.__match(TokenType.LEFT_PAREN):
            expression = self.__expression()
            self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return GroupingExpression(expression)
        else:
            self.__error(self.__peek(), "Expect expression.")

    def parse(self) -> Optional[Expression]:
        try:
            return self.__expression()
        except ParseException:
            return None
