import contextlib
from .exception_case import BreakLoop

# Global function storage
functions = {}

class ReturnValue(Exception):
    """Exception used to handle return statements in functions"""
    def __init__(self, value=None):
        self.value = value

def get_indent_level(line):
    """Get indentation level of a line"""
    line_expanded = line.expandtabs(4)
    return len(line_expanded) - len(line_expanded.lstrip(' '))

def parse_function_definition(line):
    """
    Parse function definition line
    Syntax: define <func_name> with <var1>,<var2>,...
    Or: define <func_name>
    """
    line = line.strip()
    
    # Remove 'define ' prefix
    remaining = line[7:].strip()  # Remove 'define '
    
    if ' with ' in remaining:
        # Function with parameters
        func_name = remaining[:remaining.index(' with ')].strip()
        params_str = remaining[remaining.index(' with ') + 6:].strip()
        
        # Parse parameters - split by comma and strip whitespace
        if params_str:
            params = [p.strip() for p in params_str.split(',')]
        else:
            params = []
    else:
        # Function without parameters
        func_name = remaining.strip()
        params = []
    
    return func_name, params

def parse_function_call(line):
    """
    Parse function call line
    Syntax: call <func_name> with <arg1>,<arg2>,...
    Or: call <func_name>
    """
    line = line.strip()
    
    # Remove 'call ' prefix
    remaining = line[5:].strip()  # Remove 'call '
    
    if ' with ' in remaining:
        # Function call with arguments
        func_name = remaining[:remaining.index(' with ')].strip()
        args_str = remaining[remaining.index(' with ') + 6:].strip()
        
        # Parse arguments - split by comma and strip whitespace
        if args_str:
            args = [arg.strip() for arg in args_str.split(',')]
        else:
            args = []
    else:
        # Function call without arguments
        func_name = remaining.strip()
        args = []
    
    return func_name, args

def collect_function_body(lines, start_index):
    """
    Collect all lines that belong to a function body
    Returns: (body_lines, next_line_index)
    """
    body_lines = []
    base_indent = get_indent_level(lines[start_index])
    
    i = start_index + 1
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Skip empty lines and comments within function
        if not stripped or stripped.startswith('#') or stripped.startswith('//'):
            i += 1
            continue
        
        current_indent = get_indent_level(line)
        
        # If we hit same or lower indentation, we're done with the function body
        if current_indent <= base_indent:
            break
            
        body_lines.append(line)
        i += 1
    
    return body_lines, i

def is_function_definition(line):
    """Check if line is a function definition"""
    stripped = line.strip()
    return stripped.startswith('define ')

def is_function_call(line):
    """Check if line is a function call"""
    stripped = line.strip()
    return stripped.startswith('call ')

def register_function(func_name, params, body):
    """Register a function in the global functions dictionary"""
    functions[func_name] = {
        "params": params,
        "body": body
    }
    # print(f"Function '{func_name}' defined with {len(params)} parameters")

def execute_function(func_name, args, global_variables, run_script_func, expression_evaluator_func=None):
    """
    Execute a user-defined function
    Args:
        func_name: Name of function to execute
        args: List of argument expressions
        global_variables: Global variable scope
        run_script_func: The run_script function to execute function body
        expression_evaluator_func: Your existing expression evaluator function (optional)
    """
    if func_name not in functions:
        raise Exception(f"Function '{func_name}' is not defined")
    
    func_def = functions[func_name]
    params = func_def["params"]
    body = func_def["body"]
    
    # Check argument count
    if len(args) != len(params):
        raise Exception(f"Function '{func_name}' expects {len(params)} arguments, got {len(args)}")
    
    # Create local variable scope (copy of global variables)
    local_variables = global_variables.copy()
    
    # Evaluate arguments and bind to parameters
    for param, arg_expr in zip(params, args):
        if expression_evaluator_func:
            # Use your existing expression evaluator if provided
            try:
                arg_value = expression_evaluator_func(arg_expr, global_variables)
            except Exception as e:
                # Fallback to simple evaluation
                arg_value = simple_evaluate_expression(arg_expr, global_variables)
        else:
            # Use simple built-in evaluator
            arg_value = simple_evaluate_expression(arg_expr, global_variables)
        
        local_variables[param] = arg_value
    
    # Execute function body
    try:
        return_value = run_script_func(body, local_variables)
        return return_value
    except ReturnValue as rv:
        return rv.value
    except BreakLoop:
        # BreakLoop should not escape function boundaries
        raise Exception("'stop' command cannot be used to exit from functions")
    except Exception as e:
        raise Exception(f"Error in function '{func_name}': {e}")

def handle_return_statement(line, variables):
    """
    Handle return statement
    Syntax: return <expression>
    Or: return
    """
    from .evaluator.context import get_evaluator

    evaluator = get_evaluator()
    evaluate_expression = evaluator.evaluate

    line = line.strip()
    
    if len(line) > 6:  # 'return expression'
        return_expr = line[6:].strip()
        if return_expr:
            try:
                return_value = evaluate_expression(return_expr, variables)
            except Exception:
                return_value = simple_evaluate_expression(return_expr, variables)
        else:
            return_value = None
    else:  # Just 'return'
        return_value = None
    
    raise ReturnValue(return_value)

def simple_evaluate_expression(expr, variables):
    """
    Simple expression evaluator as fallback
    """
    expr = str(expr).strip()

    # Handle string literals
    if (expr.startswith('"') and expr.endswith('"')) or (expr.startswith("'") and expr.endswith("'")):
        return expr[1:-1]

    # Handle numbers
    with contextlib.suppress(ValueError):
        if '.' in expr:
            return float(expr)
        else:
            return int(expr)
    # Handle variables
    if expr in variables:
        return variables[expr]

    # Handle simple expressions (basic arithmetic)
    try:
        # Simple evaluation for basic math
        # Replace variables with their values
        eval_expr = expr
        for var_name, var_value in variables.items():
            if isinstance(var_value, str):
                eval_expr = eval_expr.replace(var_name, f'"{var_value}"')
            else:
                eval_expr = eval_expr.replace(var_name, str(var_value))
        return eval(eval_expr)
    except Exception:
        return expr

def get_function_names():
    """Get list of all defined function names"""
    return list(functions.keys())

def function_exists(func_name):
    """Check if a function exists"""
    return func_name in functions

def clear_functions():
    """Clear all defined functions (useful for testing)"""
    global functions
    functions = {}