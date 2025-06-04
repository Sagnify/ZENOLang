import re
from commands.evaluator.main import NaturalLanguageEvaluator

evaluator = NaturalLanguageEvaluator()
evaluate_expression = evaluator.evaluate
def execute(line, variables):
    parts = line[4:].split(" be ")
    if len(parts) != 2:
        raise SyntaxError("Invalid syntax in 'let' command")
    var_name = parts[0].strip() # Variable name should be before 'be'
    value_str = parts[1].strip() # Value should be after 'be'
    # print(f"Setting variable '{var_name}' to value '{value_str}'")

    if value_str.startswith('"') and value_str.endswith('"'):
        # value = value_str[1:-1]
        value = evaluate_expression(value, variables)  # Evaluate the string as an expression
    else:
        # print(f"Evaluating expression for variable '{var_name}' with value '{value_str}'")
        value = evaluate_expression(value_str, variables)


    variables[var_name] = value