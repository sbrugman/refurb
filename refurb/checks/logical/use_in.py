from dataclasses import dataclass

from mypy.nodes import ComparisonExpr, OpExpr

from refurb.error import Error


@dataclass
class ErrorUseInExpr(Error):
    """
    When comparing a value to multiple possible options, don't use multiple
    `or` checks, use a single `is` expr:

    Bad:

    ```
    if x == "abc" or x == "def":
        pass
    ```

    Good:

    ```
    if x in ("abc", "def"):
        pass
    ```

    Note: This should not be used if the operands depend on boolean short
    circuting, since the operands will be eagerly evaluated. This is primarily
    useful for comparing against a range of constant values.
    """

    code = 108
    msg: str = "Use `x in (y, z)` instead of `x == y or x == z`"


def check(node: OpExpr, errors: list[Error]) -> None:
    match node:
        case OpExpr(
            op="or",
            left=ComparisonExpr(operators=["=="], operands=[lhs, _]),
            right=ComparisonExpr(operators=["=="], operands=[rhs, _]),
        ) if str(lhs) == str(rhs):
            errors.append(ErrorUseInExpr(node.line, node.column))