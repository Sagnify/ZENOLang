import contextlib
import re

from .evaluator.context import get_evaluator



def handle_list_command(line, variables):
    evaluator = get_evaluator()
    evaluate_expression = evaluator.evaluate
    if line.startswith("add "):
        match = re.match(r"add (.+) to (.+)", line)
        if not match:
            raise SyntaxError("Invalid syntax for 'add' command")
        value_expr, list_name = match.groups()
        list_name = list_name.strip()
        if list_name not in variables:
            raise NameError(f"List variable '{list_name}' not defined")
        target_list = variables[list_name]
        if not isinstance(target_list, list):
            raise TypeError(f"Variable '{list_name}' is not a list")
        value = evaluate_expression(value_expr.strip(), variables)
        target_list.append(value)

    elif line.startswith("remove "):
        match = re.match(r"remove (.+) from (.+)", line)
        if not match:
            raise SyntaxError("Invalid syntax for 'remove' command")
        value_expr, list_name = match.groups()
        list_name = list_name.strip()
        if list_name not in variables:
            raise NameError(f"List variable '{list_name}' not defined")
        target_list = variables[list_name]
        if not isinstance(target_list, list):
            raise TypeError(f"Variable '{list_name}' is not a list")
        value = evaluate_expression(value_expr.strip(), variables)
        with contextlib.suppress(ValueError):
            target_list.remove(value)
    elif line.startswith("length of "):
        match = re.match(r"length of (.+)", line)
        if not match:
            raise SyntaxError("Invalid syntax for 'length of' command")
        list_name = match[1].strip()
        if list_name not in variables:
            raise NameError(f"List variable '{list_name}' not defined")
        target_list = variables[list_name]
        if not isinstance(target_list, list):
            raise TypeError(f"Variable '{list_name}' is not a list")
        variables["_last_length"] = len(target_list)

    elif " at " in line and " in " in line:
        match = re.match(r"(.+) at (.+) in (.+)", line)
        if not match:
            raise SyntaxError("Invalid syntax for 'at' command")
        var_name, index_expr, list_name = match.groups()
        list_name = list_name.strip()
        if list_name not in variables:
            raise NameError(f"List variable '{list_name}' not defined")
        target_list = variables[list_name]
        if not isinstance(target_list, list):
            raise TypeError(f"Variable '{list_name}' is not a list")
        index = int(evaluate_expression(index_expr.strip(), variables))
        if index < 0 or index >= len(target_list):
            raise IndexError("Index out of range")
        variables[var_name.strip()] = target_list[index]

    else:
        raise SyntaxError("Unknown list operation")
