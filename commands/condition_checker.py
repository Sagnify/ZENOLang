import re
from commands.evaluator.main import NaturalLanguageEvaluator


def check_condition(expr: str, variables: dict) -> bool:
    evaluator = NaturalLanguageEvaluator()
    evaluate_expression = evaluator.evaluate
    expr = expr.strip()

    # Preprocess booleans to Python style
    expr = re.sub(r'\btrue\b', 'True', expr, flags=re.IGNORECASE)
    expr = re.sub(r'\bfalse\b', 'False', expr, flags=re.IGNORECASE)

    # Handle leading "not"
    if expr.startswith("not "):
        return not check_condition(expr[4:].strip(), variables)

    # Handle 'and' with higher precedence
    if ' and ' in expr and is_safe_to_split(expr, 'and'):
        parts = split_by_logical(expr, 'and')
        return all(check_condition(part, variables) for part in parts)

    # Handle 'or'
    if ' or ' in expr and is_safe_to_split(expr, 'or'):
        parts = split_by_logical(expr, 'or')
        return any(check_condition(part, variables) for part in parts)

    # Base condition — simple expression
    try:
        return bool(evaluate_expression(expr, variables))
    except Exception as e:
        raise ValueError(f"Condition evaluation failed for '{expr}': {e}")


def split_by_logical(expr: str, logical_op: str):
    parts = []
    buffer = ''
    in_quote = None
    i = 0
    while i < len(expr):
        char = expr[i]

        # Handle quotes properly
        if char in "\"'":
            if in_quote is None:
                in_quote = char
            elif in_quote == char:
                in_quote = None

        # Try to match logical op only when outside quotes
        if not in_quote and expr[i:i+len(logical_op)+2] == f' {logical_op} ':
            parts.append(buffer.strip())
            buffer = ''
            i += len(logical_op) + 1
            continue

        buffer += char
        i += 1

    if buffer:
        parts.append(buffer.strip())

    return parts


def is_safe_to_split(expr: str, logical_op: str):
    in_quote = None
    i = 0
    while i < len(expr):
        char = expr[i]
        if char in "\"'":
            if in_quote is None:
                in_quote = char
            elif in_quote == char:
                in_quote = None
        elif not in_quote and expr[i:i+len(logical_op)+2] == f' {logical_op} ':
            return True
        i += 1
    return False



# ─────────────────────────────
# 🧪 Testing with your variables
# variables = {
#     "x": 5,
#     "y": 10,
#     "z": 5,
#     "status": "active",
#     "username": "sagnik123",
#     "role": "admin",
#     "flag": False,
#     "message": "welcome to zenolang",
#     # Uncomment when `total` and `discount` are defined
#     "total": 100, 
#     "discount": 20
# }

# print(check_condition("x is z and status is 'active'", variables))
# print(check_condition("x less y or role is 'admin'", variables))
# print(check_condition("username contains 'sagnik' and y more x", variables))
# print(check_condition("role isn't 'user' and flag is False", variables))
# print(check_condition("x atleast z and y atmost 10", variables))
# print(check_condition("message contains 'zenolang' and message contains 'welcome'", variables))
# # Uncomment when `total` and `discount` are defined in variables
# print(check_condition("total subtracts discount is y", variables))
