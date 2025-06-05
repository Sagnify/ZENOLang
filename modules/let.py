import re
from .evaluator.main import NaturalLanguageEvaluator

evaluator = NaturalLanguageEvaluator()
evaluate_expression = evaluator.evaluate

def execute(line, variables):
    parts = line[4:].split(" be ")
    if len(parts) != 2:
        raise SyntaxError("Invalid syntax in 'let' command")

    var_name = parts[0].strip()
    value_str = parts[1].strip()

    if value_str == '""':
        # print(f"Assigning empty string to variable '{var_name}'")
        value = ""  # Directly assign empty string without evaluation
    elif value_str.startswith('"') and value_str.endswith('"'):
        # print(f"Assigning string literal to variable '{var_name}': {value_str}")
        value = evaluate_expression(value_str, variables)
    else:
        # print(f"Evaluating expression for variable '{var_name}': {value_str}")
        value = evaluate_expression(value_str, variables)

    variables[var_name] = value
