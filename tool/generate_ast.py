from argparse import ArgumentParser
import ast
from dataclasses import dataclass
from typing import List


def define_classes() -> str:
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
        ast.ImportFrom(module="abc", names=[ast.alias(name="ABC")]),
        ast.ImportFrom(module="dataclasses", names=[ast.alias(name="dataclass")]),
        ast.ImportFrom(module="pylox.token", names=[ast.alias(name="Token")]),
    ]
    base_classes = [
        ast.ClassDef(name="Expression", bases=[ast.Name(id="ABC")], body=[ast.Pass()])
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
            [ClassType.PropertyType("expr", "Expression")],
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
            ),
            decorator_list=[ast.Name(id="dataclass")],
        ),
        class_types,
    )

    return ast.unparse(ast.Module(body=[*imports, *base_classes, *sub_classes]))


def generate_classes(output_file: str) -> None:
    with open(output_file, "w+") as file:
        file.writelines(define_classes())


if __name__ == "__main__":
    parser = ArgumentParser(prog="pylox", description="Lox tool to generate ASTs")
    parser.add_argument("-o", "--output", required=True)

    args = parser.parse_args()
    generate_classes(args.output)
