from typing import List
from pylox.expression import (
    BinaryExpression,
    Expression,
    GroupingExpression,
    LiteralExpression,
    UnaryExpression,
    Visitor,
)
from pylox.token_type import TokenType
from pylox.tokens import Token


class AstPrinter(Visitor[str]):
    def print(self, expression: Expression) -> str:
        return expression.accept(self)

    def parenthesize(self, name: str, expressions: List[Expression]) -> str:
        return f"({name} {''.join((map(lambda expr: ' ' + expr.accept(self), expressions)))})"

    def visit_binary_expression(self, expression: BinaryExpression) -> str:
        return self.parenthesize(
            expression.operator.lexeme, [expression.left, expression.right]
        )

    def visit_grouping_expression(self, expression: GroupingExpression) -> str:
        return self.parenthesize("group", [expression.expression])

    def visit_literal_expression(self, expression: LiteralExpression) -> str:
        if expression.value is None:
            return "nil"

        return str(expression.value)

    def visit_unary_expression(self, expression: UnaryExpression) -> str:
        return self.parenthesize(expression.operator.lexeme, [expression.right])


if __name__ == "__main__":
    expression = BinaryExpression(
        UnaryExpression(Token(TokenType.MINUS, "-", None, 1), LiteralExpression("123")),
        Token(TokenType.STAR, "*", None, 1),
        GroupingExpression(LiteralExpression(45.67)),
    )

    ast_printer = AstPrinter()
    print(ast_printer.print(expression))
