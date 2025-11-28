from crewai.tools import BaseTool
from typing import Type, Any
from pydantic import BaseModel, Field
import ast
import operator
import re


class CalculatorInput(BaseModel):
    """Input schema for CalculatorTool."""
    operation: str = Field(..., description="A mathematical expression like 200*7 or 5000/2*10")


class CalculatorTool(BaseTool):
    name: str = "Make a calculation"
    description: str = "Useful to perform any mathematical calculations, like sum, minus, multiplication, division, etc. The input should be a mathematical expression, examples: 200*7 or 5000/2*10"
    args_schema: Type[BaseModel] = CalculatorInput

    def _run(self, operation: Any) -> str:
        try:
            # Handle if operation is passed as a dict
            if isinstance(operation, dict):
                if 'operation' in operation:
                    operation = operation['operation']
                elif 'expression' in operation:
                    operation = operation['expression']
                else:
                    operation = str(operation)
            
            # Convert to string if needed
            operation = str(operation)
            
            # Define allowed operators for safe evaluation
            allowed_operators = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.Pow: operator.pow,
                ast.Mod: operator.mod,
                ast.USub: operator.neg,
                ast.UAdd: operator.pos,
            }
            
            # Parse and validate the expression
            if not re.match(r'^[0-9+\-*/().% ]+$', operation):
                return "Error: Invalid characters in mathematical expression"
            
            # Parse the expression
            tree = ast.parse(operation, mode='eval')
            
            def _eval_node(node):
                if isinstance(node, ast.Expression):
                    return _eval_node(node.body)
                elif isinstance(node, ast.Constant):  # Python 3.8+
                    return node.value
                elif isinstance(node, ast.Num):  # Python < 3.8
                    return node.n
                elif isinstance(node, ast.BinOp):
                    left = _eval_node(node.left)
                    right = _eval_node(node.right)
                    op = allowed_operators.get(type(node.op))
                    if op is None:
                        raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
                    return op(left, right)
                elif isinstance(node, ast.UnaryOp):
                    operand = _eval_node(node.operand)
                    op = allowed_operators.get(type(node.op))
                    if op is None:
                        raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
                    return op(operand)
                else:
                    raise ValueError(f"Unsupported node type: {type(node).__name__}")
            
            result = _eval_node(tree)
            return str(result)
            
        except (SyntaxError, ValueError, ZeroDivisionError, TypeError) as e:
            return f"Error: {str(e)}"
        except Exception:
            return "Error: Invalid mathematical expression"
