from .evaluator.context import get_evaluator



def execute(line, variables):
    evaluator = get_evaluator()
    evaluate_expression = evaluator.evaluate
    parts = line.split(" ", 1)

    if len(parts) != 2:
        raise SyntaxError("Invalid syntax in 'say' command")
    to_say = parts[1].strip()

    fragments = [fragment.strip() for fragment in to_say.split('+')]
    output = ""

    for fragment in fragments:
        # If fragment is a quoted string, take it literally
        if fragment.startswith('"') and fragment.endswith('"'):
            output += fragment[1:-1]
        else:
            # Try evaluating as expression (variable, number, or arithmetic)
            val = evaluate_expression(fragment, variables)
            output += str(val)

    print(output)