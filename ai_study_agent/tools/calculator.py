import ast
import operator
from typing import Callable

from ai_study_agent.models import ToolResult


class CalculatorTool:
    """Safely evaluates arithmetic expressions used inside agent answers."""

    name = "calculator"

    _binary_ops: dict[type[ast.operator], Callable[[float, float], float]] = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }
    _unary_ops: dict[type[ast.unaryop], Callable[[float], float]] = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    def run(self, expression: str) -> ToolResult:
        try:
            tree = ast.parse(expression, mode="eval")
            value = self._evaluate(tree.body)
        except (SyntaxError, ValueError, ZeroDivisionError, OverflowError) as exc:
            return ToolResult(self.name, False, None, str(exc))
        return ToolResult(self.name, True, value, "calculation completed")

    def _evaluate(self, node: ast.AST) -> float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in self._binary_ops:
                raise ValueError("unsupported arithmetic operator")
            left = self._evaluate(node.left)
            right = self._evaluate(node.right)
            return self._binary_ops[op_type](left, right)
        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in self._unary_ops:
                raise ValueError("unsupported unary operator")
            return self._unary_ops[op_type](self._evaluate(node.operand))
        raise ValueError("expression contains unsupported content")
