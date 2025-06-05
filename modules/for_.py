from . import runner
from .evaluator.context import get_evaluator

evaluator = get_evaluator()
evaluate_expression = evaluator.evaluate

def resolve_value(val, variables):
    try:
        return int(val)
    except ValueError:
        if val in variables:
            return int(variables[val])
        else:
            raise ValueError(f"Cannot resolve value: '{val}'")

def evaluate(line, variables):
    # Expected: repeat counting i from 1 to 10 [step 2]
    if not line.startswith("repeat counting "):
        raise SyntaxError("Invalid syntax in 'repeat' command.")

    line = line[len("repeat counting "):].strip()

    parts = line.split(" from ")
    if len(parts) != 2:
        raise SyntaxError("Missing 'from' in 'repeat' command.")
    
    var_name = parts[0].strip()
    remaining = parts[1]

    # Split "start to end [step stepval]"
    step = 1  # default

    # Check if 'step' is present
    if " step " in remaining:
        to_part, step_str = remaining.split(" step ")
        step_val_raw = step_str.strip()
        step = resolve_value(step_val_raw, variables)
    else:
        to_part = remaining

    if " to " not in to_part:
        raise SyntaxError("Missing 'to' in 'repeat' command.")

    start_raw, end_raw = to_part.split(" to ")
    start_value = resolve_value(start_raw.strip(), variables)
    end_value = resolve_value(end_raw.strip(), variables)

    return var_name, start_value, end_value, step


# def handle_repeat_block(lines, i, variables):
#     header = lines[i]
#     i += 1  # move to body

#     # Get loop block
#     block = []
#     while i < len(lines) and (lines[i].startswith("   ") or lines[i].startswith("\t")):
#         block.append(lines[i].lstrip())
#         i += 1

#     # Evaluate loop bounds
#     var_name, start, end, step = evaluate(header, variables)

#     for val in range(start, end + (1 if step > 0 else -1), step):
#         variables[var_name] = val
#         runner.run_script(block, variables)  # run the entire block at once


#     return i
