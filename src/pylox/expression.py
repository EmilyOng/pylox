from abc import ABC
from dataclasses import dataclass
from pylox.token import Token


class Expression(ABC):
    pass


@dataclass
class BinaryExpression(Expression):
    left: Expression
    operator: Token
    right: Expression


@dataclass
class GroupingExpression(Expression):
    expr: Expression


@dataclass
class LiteralExpression(Expression):
    value: any


@dataclass
class UnaryExpression(Expression):
    operator: Token
    right: Expression


class Visitor[T](ABC):
    def visit_binary_expression(self, expression: BinaryExpression) -> T:
        pass

    def visit_grouping_expression(self, expression: GroupingExpression) -> T:
        pass

    def visit_literal_expression(self, expression: LiteralExpression) -> T:
        pass

    def visit_unary_expression(self, expression: UnaryExpression) -> T:
        pass
