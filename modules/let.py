import re
from .evaluator.main import NaturalLanguageEvaluator
from . import function_handler



def execute(line, variables, run_script_func=None):
    evaluator = NaturalLanguageEvaluator()
    evaluate_expression = evaluator.evaluate
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
    elif value_str.startswith('call '):
        # Handle function call
        if run_script_func is None:
            raise Exception("Function calls in 'let' require run_script_func to be passed")
        
        try:
            func_name, args = function_handler.parse_function_call(value_str)
            if function_handler.function_exists(func_name):
                value = function_handler.execute_function(func_name, args, variables, run_script_func, evaluate_expression)
                # print(f"Function '{func_name}' returned: {value}")
            else:
                raise Exception(f"Function '{func_name}' is not defined")
        except Exception as e:
            raise Exception(f"Error calling function in 'let' statement: {e}")
        
    elif value_str.startswith("[") and value_str.endswith("]"):
        try:
            # Evaluate the list safely — only literals allowed
            value = eval(value_str, {"__builtins__": None}, {})
            if not isinstance(value, list):
                raise ValueError("Expected a list")
        except Exception as e:
            raise SyntaxError(f"Invalid list syntax: {e}")
    else:
        # print(f"Evaluating expression for variable '{var_name}': {value_str}")
        value = evaluate_expression(value_str, variables)

    variables[var_name] = value