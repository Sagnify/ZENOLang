from commands import runner, condition_checker
# from commands.operators import operators

def evaluate(line, variables):
    # Basic syntax check
    if not line.startswith("while ") or " then" not in line:
        raise SyntaxError("Invalid syntax in 'while' command - missing 'then'")

    # Extract condition part between "while" and "then"
    condition_part = line.strip()[6:].split(" then")[0].strip()

    # Pass condition to the condition checker
    return condition_checker.check_condition(condition_part, variables)




def handle_while_block(lines, i, variables):
    condition_line = lines[i]
    i += 1  # move to the block

    # Capture block
    start = i
    block = []
    while i < len(lines) and (lines[i].startswith("   ") or lines[i].startswith("\t")):
        block.append(lines[i].lstrip())
        i += 1

    # Execute block while condition is true
    while True:
        try:
            if not evaluate(condition_line, variables):
                break
        except (SyntaxError, ValueError) as e:
            print(f"Error: {e}")
            break

        for bline in block:
            runner.run_script([bline], variables)

    return i


