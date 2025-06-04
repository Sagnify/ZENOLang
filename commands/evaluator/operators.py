"""
Operators Module - Defines all supported operators and their implementations
"""

from typing import Any


# Core operator implementations
OPERATORS = {
    # Comparison operators
    "is": lambda x, y: x == y,
    "equals": lambda x, y: x == y,
    "isn't": lambda x, y: x != y,
    "not_equals": lambda x, y: x != y,
    
    # Relational operators
    "less": lambda x, y: x < y,
    "less_than": lambda x, y: x < y,
    "more": lambda x, y: x > y,
    "greater": lambda x, y: x > y,
    "greater_than": lambda x, y: x > y,
    "atleast": lambda x, y: x >= y,
    "at_least": lambda x, y: x >= y,
    "atmost": lambda x, y: x <= y,
    "at_most": lambda x, y: x <= y,
    
    # String operators
    "contains": lambda x, y: str(y) in str(x),
    "startswith": lambda x, y: str(x).startswith(str(y)),
    "endswith": lambda x, y: str(x).endswith(str(y)),
    
    # Range operator
    "between": lambda x, y, z: y <= x <= z,
    
    # Arithmetic operators
    "add": lambda x, y: x + y,
    "adds": lambda x, y: x + y,
    "plus": lambda x, y: x + y,
    "subtract": lambda x, y: x - y,
    "subtracts": lambda x, y: x - y,
    "minus": lambda x, y: x - y,
    "multiply": lambda x, y: x * y,
    "multiplies": lambda x, y: x * y,
    "times": lambda x, y: x * y,
    "divide": lambda x, y: x / y if y != 0 else float('inf'),
    "divides": lambda x, y: x / y if y != 0 else float('inf'),
    "divided_by": lambda x, y: x / y if y != 0 else float('inf'),
    "modulus": lambda x, y: x % y if y != 0 else float('inf'),
    "mod": lambda x, y: x % y if y != 0 else float('inf'),
    "power": lambda x, y: x ** y,
    "to_the_power_of": lambda x, y: x ** y,
    
    # Logical operators
    "and": lambda x, y: bool(x) and bool(y),
    "or": lambda x, y: bool(x) or bool(y),
    "not": lambda x: not bool(x),
}

# Symbol mappings for conversion to Python operators
OPERATOR_SYMBOLS = {
    # Arithmetic
    "add": "+", "adds": "+", "plus": "+",
    "subtract": "-", "subtracts": "-", "minus": "-", 
    "multiply": "*", "multiplies": "*", "times": "*",
    "divide": "/", "divides": "/", "divided_by": "/",
    "modulus": "%", "mod": "%",
    "power": "**", "to_the_power_of": "**",
    
    # Comparison
    "is": "==", "equals": "==",
    "isn't": "!=", "not_equals": "!=",
    "less": "<", "less_than": "<",
    "more": ">", "greater": ">", "greater_than": ">",
    "atleast": ">=", "at_least": ">=",
    "atmost": "<=", "at_most": "<=",
    
    # Logical
    "and": "and", "or": "or", "not": "not",
}

# Categorize operators for processing logic
ARITHMETIC_OPS = {
    "add", "adds", "plus", "subtract", "subtracts", "minus",
    "multiply", "multiplies", "times", "divide", "divides", "divided_by",
    "modulus", "mod", "power", "to_the_power_of"
}

COMPARISON_OPS = {
    "is", "equals", "isn't", "not_equals", "less", "less_than",
    "more", "greater", "greater_than", "atleast", "at_least",
    "atmost", "at_most"
}

LOGICAL_OPS = {"and", "or", "not"}
STRING_OPS = {"contains", "startswith", "endswith"}
SPECIAL_OPS = {"between"}


def get_operator_type(op_name: str) -> str:
    """Get the category of an operator"""
    op_lower = op_name.lower()
    if op_lower in ARITHMETIC_OPS:
        return "arithmetic"
    elif op_lower in COMPARISON_OPS:
        return "comparison"
    elif op_lower in LOGICAL_OPS:
        return "logical"
    elif op_lower in STRING_OPS:
        return "string"
    elif op_lower in SPECIAL_OPS:
        return "special"
    else:
        return "unknown"


def is_arithmetic_only(expression: str) -> bool:
    """Check if expression contains only arithmetic operators"""
    words = expression.lower().split()
    has_arithmetic = any(op in words for op in ARITHMETIC_OPS)
    has_comparison = any(op in words for op in COMPARISON_OPS)
    return has_arithmetic and not has_comparison


def is_arithmetic_comparison(expression: str) -> bool:
    """Check if expression is arithmetic comparison like 'a modulus b is c'"""
    words = expression.lower().split()
    has_arithmetic = any(op in words for op in ARITHMETIC_OPS)
    has_comparison = any(op in words for op in COMPARISON_OPS)
    return has_arithmetic and has_comparison