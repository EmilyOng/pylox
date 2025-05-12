from typing import List
from pylox.expression import (
    BinaryExpression,
    Expression,
    GroupingExpression,
    LiteralExpression,
    TernaryExpression,
    UnaryExpression,
    Visitor,
)


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

    def visit_ternary_expression(self, expression: TernaryExpression) -> str:
        return self.parenthesize(
            "?:",
            [
                expression.conditional_expression,
                expression.true_expression,
                expression.false_expression,
            ],
        )
