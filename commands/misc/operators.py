import re
import ast
import operator
from typing import Any, Dict, Union

# Simple operators for single expressions only
operators = {
    "is": lambda x, y: x == y,
    "isn't": lambda x, y: x != y,
    "equals": lambda x, y: x == y,
    "not_equals": lambda x, y: x != y,
    "less": lambda x, y: x < y,
    # "less_than": lambda x, y: x < y,
    "more": lambda x, y: x > y,
    "greater": lambda x, y: x > y,
    # "greater_than": lambda x, y: x > y,
    "atleast": lambda x, y: x >= y,
    # "at_least": lambda x, y: x >= y,
    "atmost": lambda x, y: x <= y,
    # "at_most": lambda x, y: x <= y,
    "contains": lambda x, y: str(y) in str(x),
    "startswith": lambda x, y: str(x).startswith(str(y)),
    "endswith": lambda x, y: str(x).endswith(str(y)),
    "between": lambda x, y, z: y <= x <= z,
    "adds": lambda x, y: x + y,
    "plus": lambda x, y: x + y,
    "add": lambda x, y: x + y,  # Added missing 'add'
    "subtracts": lambda x, y: x - y,
    "minus": lambda x, y: x - y,
    "multiplies": lambda x, y: x * y,
    "times": lambda x, y: x * y,
    "multiply": lambda x, y: x * y,  # Added missing 'multiply'
    "divides": lambda x, y: x / y if y != 0 else float('inf'),
    "divided_by": lambda x, y: x / y if y != 0 else float('inf'),
    "modulus": lambda x, y: x % y if y != 0 else float('inf'),
    "mod": lambda x, y: x % y if y != 0 else float('inf'),
    "power": lambda x, y: x ** y,
    "to_the_power_of": lambda x, y: x ** y,
}

operator_symbols = {
    "adds": "+",
    "plus": "+",
    "add": "+",
    "subtracts": "-",
    "minus": "-",
    "multiplies": "*",
    "times": "*",
    "multiply": "*",
    "divides": "/",
    "divided_by": "/",
    "modulus": "%",
    "mod": "%",
    "power": "**",
    "to_the_power_of": "**",
    "is": "==",
    "equals": "==",
    "isn't": "!=",
    "not_equal": "!=",
    "less": "<",
    "less_than": "<",
    "more": ">",
    "greater": ">",
    "greater_than": ">",
    "atleast": ">=",
    "at_least": ">=",
    "atmost": "<=",
    "at_most": "<=",
    "and": "and",
    "or": "or",
    "not": "not",
}

def find_innermost_brackets(expression: str) -> tuple:
    """Find the innermost bracket pair and return (start_pos, end_pos, content)"""
    # Find all bracket pairs first
    bracket_pairs = []
    stack = []
    
    for i, char in enumerate(expression):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if stack:
                start = stack.pop()
                bracket_pairs.append((start, i, expression[start+1:i]))
    
    if not bracket_pairs:
        return None
    
    # Find the bracket pair with content that doesn't contain any brackets
    for start, end, content in bracket_pairs:
        if '(' not in content and ')' not in content:
            return (start, end, content)
    
    # If all brackets contain other brackets, return the shortest one
    return min(bracket_pairs, key=lambda x: x[1] - x[0])

def evaluate_brackets_recursively(expression: str, variables: Dict[str, Any]) -> str:
    """Recursively evaluate brackets from innermost to outermost"""
    # Keep processing until no more brackets
    while '(' in expression and ')' in expression:
        bracket_info = find_innermost_brackets(expression)
        if not bracket_info:
            break
            
        start_pos, end_pos, bracket_content = bracket_info
        
        # Evaluate the content inside the brackets
        try:
            bracket_result = evaluate_expression_without_brackets(bracket_content.strip(), variables)
            
            # Replace the bracket and its content with the result
            # Convert result to string representation
            if isinstance(bracket_result, str):
                result_str = f'"{bracket_result}"'
            else:
                result_str = str(bracket_result)
                
            expression = expression[:start_pos] + result_str + expression[end_pos+1:]
            
        except Exception as e:
            raise ValueError(f"Error evaluating bracket content '{bracket_content}': {e}")
    
    return expression

def parse_value(value_str: str, variables: Dict[str, Any]) -> Any:
    """Parse a value from string with enhanced boolean and expression handling"""
    original_value_str = value_str
    value_str = value_str.strip()

    # Handle quoted strings (only if quotes match exactly)
    if (value_str.startswith('"') and value_str.endswith('"')) or \
    (value_str.startswith("'") and value_str.endswith("'")):
        # Strip exactly one quote from both ends
        value_str = value_str[1:-1]
        # Don't strip spaces inside quotes! Just return as is.
        return value_str

    # Handle boolean values (case-sensitive True/False)
    if value_str == 'True':
        return True
    elif value_str == 'False':
        return False
    elif value_str.lower() in ['null', 'none']:
        return None

    # Handle numbers (including negative and floats)
    num_str = value_str
    if num_str.startswith('-'):
        num_str = num_str[1:]
    if num_str.replace('.', '', 1).isdigit():
        num_val = float(value_str) if '.' in value_str else int(value_str)
        return num_val

    # Handle variables
    if value_str in variables:
        var_val = variables[value_str]
        return var_val

    # If nothing matches, raise an error
    raise ValueError(f"Cannot resolve value: '{value_str}'")

def split_outside_quotes(text: str, sep: str) -> list[str]:
    parts = []
    current = []
    in_single_quote = False
    in_double_quote = False
    i = 0
    sep_len = len(sep)
    while i < len(text):
        c = text[i]
        # Toggle quote states
        if c == "'" and not in_double_quote:
            in_single_quote = not in_single_quote
            current.append(c)
        elif c == '"' and not in_single_quote:
            in_double_quote = not in_double_quote
            current.append(c)
        # If we're outside quotes and the substring at i matches sep
        elif not in_single_quote and not in_double_quote and text[i:i+sep_len] == sep:
            parts.append(''.join(current).strip())
            current = []
            i += sep_len
            continue
        else:
            current.append(c)
        i += 1
    # Append the last chunk
    parts.append(''.join(current).strip())
    return parts

def evaluate_complex_expression(expression: str, variables: Dict[str, Any]) -> Any:
    import ast

    # Replace known natural-language operators with Python equivalents
    for word_op, symbol in sorted(operator_symbols.items(), key=lambda x: -len(x[0])):
        pattern = r'\b' + re.escape(word_op) + r'\b'
        expression = re.sub(pattern, f' {symbol} ', expression, flags=re.IGNORECASE)

    # Handle `True`, `False`, `None`, quoted strings
    for var in variables:
        pattern = r'\b' + re.escape(var) + r'\b'
        if isinstance(variables[var], str):
            replacement = f'"{variables[var]}"'
        else:
            replacement = str(variables[var])
        expression = re.sub(pattern, replacement, expression)

    class SafeTransformer(ast.NodeTransformer):
        def visit_Name(self, node):
            # Leave boolean literals and keywords as-is
            if node.id in {"True", "False", "None"}:
                return node
            raise ValueError(f"Unknown variable '{node.id}' in expression")

        def visit_Call(self, node):
            raise ValueError("Function calls are not allowed")

        def visit_Attribute(self, node):
            raise ValueError("Attribute access is not allowed")

        def visit_Subscript(self, node):
            raise ValueError("Indexing is not allowed")

        def visit_Lambda(self, node):
            raise ValueError("Lambda is not allowed")

    try:
        tree = ast.parse(expression, mode='eval')
        SafeTransformer().visit(tree)
        ast.fix_missing_locations(tree)
        return eval(compile(tree, filename="<ast>", mode="eval"))
    except Exception as e:
        return f"[Error evaluating expression: {e}]"

def is_quoted_string(s: str) -> bool:
    s = s.strip()
    
    # Must start and end with the same type of quote
    if (s.startswith("'") and s.endswith("'")) or (s.startswith('"') and s.endswith('"')):
        # Check if it's just a single literal string, no + or operators outside quotes
        # We use a helper to split outside quotes
        unquoted_parts = split_outside_quotes(s, '+')
        return len(unquoted_parts) == 1  # Only one part means it's not an expression
    return False

def evaluate_expression_without_brackets(expression: str, variables: Dict[str, Any] = None) -> Any:
    """Evaluate expression assuming no brackets are present"""
    if variables is None:
        variables = {}

    expression = expression.strip()

    if is_quoted_string(expression):
        return parse_value(expression, variables)

    # Handle string concatenation using +
    if '+' in expression:
        parts = split_outside_quotes(expression, '+')

        results = []
        for i, p in enumerate(parts):
            val = evaluate_expression_without_brackets(p.strip(), variables)
            results.append(val)

        if all(isinstance(v, str) for v in results):
            result = ''.join(results)
            return result
        else:
            raise TypeError("Operator '+' is only for string concatenation.")

    # Handle single values (no operators)
    if not any(op in expression.lower().split() for op in operators.keys()) and ' between ' not in expression.lower():
        try:
            val = parse_value(expression, variables)
            return val
        except ValueError as e:
            raise ValueError(f"Unable to resolve single value: '{expression}'")

    # Handle 'between' operator specially
    if ' between ' in expression.lower():
        return handle_between_expression(expression, variables)

    # Arithmetic comparison
    if is_arithmetic_comparison(expression):
        return handle_arithmetic_comparison(expression, variables)

    # Pure arithmetic
    if is_pure_arithmetic(expression):
        return evaluate_arithmetic_expression(expression, variables)

    # Handle regular comparisons and operations
    operator_found = None
    operator_pos = -1

    for op in sorted(operators.keys(), key=len, reverse=True):
        pattern = r'\b' + re.escape(op) + r'\b'
        match = re.search(pattern, expression, re.IGNORECASE)
        if match:
            operator_found = op
            operator_pos = match.start()
            break

    if not operator_found:
        raise ValueError(f"No valid operator found in expression: '{expression}'")

    parts = split_outside_quotes(expression, operator_found)

    if len(parts) != 2:
        raise ValueError(f"Invalid expression format: '{expression}'")

    left_part = parts[0].strip()
    right_part = parts[1].strip()

    try:
        left_value = parse_value(left_part, variables)
        right_value = parse_value(right_part, variables)
    except ValueError as e:
        raise ValueError(f"Error parsing expression '{expression}': {e}")

    try:
        result = operators[operator_found](left_value, right_value)
        return result
    except Exception as e:
        raise ValueError(f"Error executing operation '{operator_found}': {e}")

def evaluate_expression(expression: str, variables: Dict[str, Any] = None) -> Any:
    """Main function to evaluate expressions with proper bracket handling"""
    if variables is None:
        variables = {}

    expression = expression.strip()

    # First, handle all brackets recursively from innermost to outermost
    if '(' in expression and ')' in expression:
        expression = evaluate_brackets_recursively(expression, variables)

    # Now evaluate the final expression without brackets
    return evaluate_expression_without_brackets(expression, variables)

def handle_between_expression(expression, variables):
    """Handle 'between' expressions: 'x between y to z'"""
    # Pattern: value between lower_bound to upper_bound
    pattern = r'(.+?)\s+between\s+(.+?)\s+to\s+(.+)'
    match = re.search(pattern, expression, re.IGNORECASE)
    
    if not match:
        raise ValueError(f"Invalid between expression format. Use: 'value between lower to upper'")
    
    value_part = match.group(1).strip()
    lower_part = match.group(2).strip()
    upper_part = match.group(3).strip()
    
    try:
        value = parse_value(value_part, variables)
        lower_bound = parse_value(lower_part, variables)
        upper_bound = parse_value(upper_part, variables)
        
        return lower_bound <= value <= upper_bound
    except ValueError as e:
        raise ValueError(f"Error in between expression '{expression}': {e}")

def is_pure_arithmetic(expression):
    """Check if expression is pure arithmetic (no comparison operators)"""
    arithmetic_ops = ['adds', 'plus', 'add', 'subtracts', 'minus', 'multiplies', 'times', 'multiply',
                      'divides', 'divided_by', 'modulus', 'mod', 'power', 'to_the_power_of']
    comparison_ops = ['is', 'isn\'t', 'equals', 'not_equals', 'less', 'less_than', 
                      'more', 'greater', 'greater_than', 'atleast', 'at_least', 
                      'atmost', 'at_most', 'contains', 'startswith', 'endswith']
    
    words = expression.lower().split()
    
    # Check if we have arithmetic operators but NO comparison operators
    has_arithmetic = any(op in words for op in arithmetic_ops)
    has_comparison = any(op in words for op in comparison_ops)
    
    return has_arithmetic and not has_comparison

def is_arithmetic_comparison(expression):
    """Check if expression is arithmetic comparison like 'a modulus b is c'"""
    arithmetic_ops = ['adds', 'plus', 'add', 'subtracts', 'minus', 'multiplies', 'times', 'multiply',
                      'divides', 'divided_by', 'modulus', 'mod', 'power', 'to_the_power_of']
    comparison_ops = ['is', 'isn\'t', 'equals', 'not_equals', 'less', 'less_than', 
                      'more', 'greater', 'greater_than', 'atleast', 'at_least', 
                      'atmost', 'at_most']
    
    words = expression.lower().split()
    
    # Check if we have both arithmetic and comparison operators
    has_arithmetic = any(op in words for op in arithmetic_ops)
    has_comparison = any(op in words for op in comparison_ops)
    
    return has_arithmetic and has_comparison

def handle_arithmetic_comparison(expression, variables):
    """Handle arithmetic comparisons like 'a modulus b is c' or 'x adds y more 10'"""
    
    # Define operator precedence (arithmetic first, then comparison)
    arithmetic_ops = ['adds', 'plus', 'add', 'subtracts', 'minus', 'multiplies', 'times', 'multiply',
                      'divides', 'divided_by', 'modulus', 'mod', 'power', 'to_the_power_of']
    comparison_ops = ['is', 'isn\'t', 'equals', 'not_equals', 'less', 'less_than', 
                      'more', 'greater', 'greater_than', 'atleast', 'at_least', 
                      'atmost', 'at_most']
    
    # Find comparison operator (should be the last one in precedence)
    comparison_op = None
    comparison_pos = -1
    
    for op in comparison_ops:
        pattern = r'\b' + re.escape(op) + r'\b'
        match = re.search(pattern, expression, re.IGNORECASE)
        if match:
            comparison_op = op
            comparison_pos = match.start()
            break
    
    if not comparison_op:
        raise ValueError(f"No comparison operator found in arithmetic comparison: '{expression}'")
    
    # Split at comparison operator
    parts = re.split(r'\b' + re.escape(comparison_op) + r'\b', expression, flags=re.IGNORECASE)
    if len(parts) != 2:
        raise ValueError(f"Invalid arithmetic comparison format: '{expression}'")
    
    left_expr = parts[0].strip()  # e.g., "a modulus b"
    right_value_str = parts[1].strip()  # e.g., "c" or "10"
    
    # Evaluate the arithmetic expression on the left
    arithmetic_result = evaluate_arithmetic_expression(left_expr, variables)
    
    # Parse the right side value
    right_value = parse_value(right_value_str, variables)
    
    # Perform the comparison
    return perform_comparison(arithmetic_result, comparison_op, right_value)

def evaluate_arithmetic_expression(expression, variables):
    """Evaluate simple arithmetic expressions like 'a modulus b' or 'x adds y'"""
    arithmetic_ops = ['adds', 'plus', 'add', 'subtracts', 'minus', 'multiplies', 'times', 'multiply',
                      'divides', 'divided_by', 'modulus', 'mod', 'power', 'to_the_power_of']
    
    # Find the arithmetic operator
    arithmetic_op = None
    for op in sorted(arithmetic_ops, key=len, reverse=True):
        pattern = r'\b' + re.escape(op) + r'\b'
        match = re.search(pattern, expression, re.IGNORECASE)
        if match:
            arithmetic_op = op
            break
    
    if not arithmetic_op:
        raise ValueError(f"No arithmetic operator found in: '{expression}'")
    
    # Split at arithmetic operator
    parts = re.split(r'\b' + re.escape(arithmetic_op) + r'\b', expression, flags=re.IGNORECASE)
    if len(parts) != 2:
        raise ValueError(f"Invalid arithmetic expression format: '{expression}'")
    
    left_part = parts[0].strip()
    right_part = parts[1].strip()
    
    # Parse operands
    left_value = parse_value(left_part, variables)
    right_value = parse_value(right_part, variables)
    
    # Perform arithmetic operation
    return operators[arithmetic_op](left_value, right_value)

def perform_comparison(left_value, comparison_op, right_value):
    """Perform comparison operation between two values"""
    if comparison_op in ['is', 'equals']:
        return left_value == right_value
    elif comparison_op in ['isn\'t', 'not_equals']:
        return left_value != right_value
    elif comparison_op in ['less', 'less_than']:
        return left_value < right_value
    elif comparison_op in ['more', 'greater', 'greater_than']:
        return left_value > right_value
    elif comparison_op in ['atleast', 'at_least']:
        return left_value >= right_value
    elif comparison_op in ['atmost', 'at_most']:
        return left_value <= right_value
    else:
        raise ValueError(f"Unknown comparison operator: {comparison_op}")
    

# Test cases
if __name__ == "__main__":
    variables = {
        "x": 5,
        "y": 10,
        "z": 3,
        "flag": False,
        "name": "Sagnik"
    }

    # Test the fixed bracket handling
    print("Testing bracket expressions:")
    print("(x add y) multiply 2 =", evaluate_expression("(x add y) multiply 2", variables))  # Should be 30
    print("((x add y) multiply 2) add 5 =", evaluate_expression("((x add y) multiply 2) add 5", variables))  # Should be 35
    print("(x add y) between (z multiply 2) to (z multiply 6) =", evaluate_expression("(x add y) between (z multiply 2) to (z multiply 6)", variables))  # Should be True
    print("x modulus y is 5 =", evaluate_expression("x modulus y is 5", variables))  # Should be True (5 % 10 = 5)
    print(evaluate_expression("'Hi '+name+'!'", variables))  # Should be "Hi Sagnik!"