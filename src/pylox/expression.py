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
