from . import runner, condition_checker
# from commands.operators import operators

def evaluate(line: str, variables: dict) -> bool:
    # Basic syntax check
    if not line.startswith("if ") or " then" not in line:
        raise SyntaxError("Invalid syntax in 'if' command - missing 'then'")
    
    # Extract condition part between "if" and "then"
    condition_part = line.strip()[3:].split(" then")[0].strip()
    
    # Pass condition to the condition checker
    return condition_checker.check_condition(condition_part, variables)



def handle_if_block(lines, i, variables):
    try:
        condition = evaluate(lines[i], variables)
    except (SyntaxError, ValueError) as e:
        print(f"Error: {e}")
        return i + 1

    i += 1  # move to line after 'if ... then'

    if condition:
        # Run indented block under the if
        while i < len(lines) and (lines[i].startswith("   ") or lines[i].startswith("\t")):
            runner.run_script([lines[i].lstrip()], variables)
            i += 1

        # Check for 'else' for skipping
        if i < len(lines) and lines[i].strip() == "else":
            # Skip the else block entirely
            i += 1
            while i < len(lines) and (lines[i].startswith("   ") or lines[i].startswith("\t")):
                i += 1  # just skip
    else:
        # Skip indented block
        while i < len(lines) and (lines[i].startswith("   ") or lines[i].startswith("\t")):
            i += 1

        # Check for 'else'
        if i < len(lines) and lines[i].strip() == "else":
            i += 1
            while i < len(lines) and (lines[i].startswith("   ") or lines[i].startswith("\t")):
                runner.run_script([lines[i].lstrip()], variables)
                i += 1

    return i

