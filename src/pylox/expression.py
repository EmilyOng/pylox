from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pylox.tokens import Token


class Expression(ABC):
    pass


@dataclass
class BinaryExpression(Expression):
    left: Expression
    operator: Token
    right: Expression

    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit_binary_expression(self)


@dataclass
class GroupingExpression(Expression):
    expression: Expression

    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit_grouping_expression(self)


@dataclass
class LiteralExpression(Expression):
    value: any

    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit_literal_expression(self)


@dataclass
class UnaryExpression(Expression):
    operator: Token
    right: Expression

    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit_unary_expression(self)


class Visitor[T](ABC):
    @abstractmethod
    def visit_binary_expression(self, expression: BinaryExpression) -> T:
        pass

    @abstractmethod
    def visit_grouping_expression(self, expression: GroupingExpression) -> T:
        pass

    @abstractmethod
    def visit_literal_expression(self, expression: LiteralExpression) -> T:
        pass

    @abstractmethod
    def visit_unary_expression(self, expression: UnaryExpression) -> T:
        pass
