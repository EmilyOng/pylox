from argparse import ArgumentParser
import ast
from dataclasses import dataclass
from typing import List


def __title_case_to_camel_case(title_case: str) -> str:
    camel_case = ""
    for i, letter in enumerate(title_case):
        if letter.isupper() and i > 0:
            camel_case += "_"
        camel_case += letter.lower()
    return camel_case


def define_ast() -> str:
    @dataclass
    class ClassType:
        @dataclass
        class PropertyType:
            name: str
            type: str

        name: str
        base_name: str
        property_types: List[PropertyType]

    imports = [
        ast.ImportFrom(module="__future__", names=[ast.alias(name="annotations")]),
        ast.ImportFrom(
            module="abc",
            names=[ast.alias(name="ABC"), ast.alias(name="abstractmethod")],
        ),
        ast.ImportFrom(module="dataclasses", names=[ast.alias(name="dataclass")]),
        ast.ImportFrom(module="pylox.tokens", names=[ast.alias(name="Token")]),
    ]

    class_types: List[ClassType] = [
        ClassType(
            "BinaryExpression",
            "Expression",
            [
                ClassType.PropertyType("left", "Expression"),
                ClassType.PropertyType("operator", "Token"),
                ClassType.PropertyType("right", "Expression"),
            ],
        ),
        ClassType(
            "GroupingExpression",
            "Expression",
            [ClassType.PropertyType("expression", "Expression")],
        ),
        ClassType(
            "LiteralExpression", "Expression", [ClassType.PropertyType("value", "any")]
        ),
        ClassType(
            "UnaryExpression",
            "Expression",
            [
                ClassType.PropertyType("operator", "Token"),
                ClassType.PropertyType("right", "Expression"),
            ],
        ),
    ]

    base_classes = [
        ast.ClassDef(name="Expression", bases=[ast.Name(id="ABC")], body=[ast.Pass()])
    ]
    sub_classes = map(
        lambda class_type: ast.ClassDef(
            name=class_type.name,
            bases=[ast.Name(id=class_type.base_name)],
            body=list(
                map(
                    lambda property_type: ast.AnnAssign(
                        target=ast.Name(id=property_type.name, ctx=ast.Store()),
                        annotation=ast.Name(id=property_type.type),
                        simple=1,
                    ),
                    class_type.property_types,
                )
            )
            + [
                ast.fix_missing_locations(
                    ast.FunctionDef(
                        name="accept",
                        args=ast.arguments(
                            args=[
                                ast.arg(arg="self"),
                                ast.arg(
                                    arg="visitor",
                                    annotation=ast.Name(id="Visitor[T]"),
                                ),
                            ]
                        ),
                        returns=ast.Name(id="T"),
                        body=[
                            ast.Return(
                                value=ast.Call(
                                    func=ast.Name(
                                        f"visitor.visit_{__title_case_to_camel_case(class_type.name)}"
                                    ),
                                    args=[ast.Name(id="self")],
                                )
                            )
                        ],
                        type_params=[ast.TypeVar(name="T")],
                    )
                )
            ],
            decorator_list=[ast.Name(id="dataclass")],
        ),
        class_types,
    )
    visitor_classes = [
        ast.ClassDef(
            name="Visitor",
            bases=[ast.Name(id="ABC")],
            type_params=[ast.TypeVar(name="T")],
            body=list(
                map(
                    lambda class_type: ast.fix_missing_locations(
                        ast.FunctionDef(
                            name=f"visit_{__title_case_to_camel_case(class_type.name)}",
                            args=ast.arguments(
                                args=[
                                    ast.arg(arg="self"),
                                    ast.arg(
                                        arg="expression",
                                        annotation=ast.Name(id=class_type.name),
                                    ),
                                ]
                            ),
                            returns=ast.Name(id="T"),
                            body=[ast.Pass()],
                            decorator_list=[ast.Name(id="abstractmethod")],
                        )
                    ),
                    class_types,
                )
            ),
        )
    ]

    return ast.unparse(
        ast.Module(body=[*imports, *base_classes, *sub_classes, *visitor_classes])
    )


def generate_ast(output_file: str) -> None:
    with open(output_file, "w+") as file:
        file.writelines(define_ast())


if __name__ == "__main__":
    parser = ArgumentParser(prog="pylox", description="Lox tool to generate ASTs")
    parser.add_argument("-o", "--output", required=True)

    args = parser.parse_args()
    generate_ast(args.output)
