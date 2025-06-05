def execute(line, variables):
    parts = line.split()
    if len(parts) != 2:
        raise SyntaxError("Invalid syntax in 'ask' command")
    
    var_name = parts[1].strip()
    user_input = input(">> ").strip()

    # Try to convert to integer if it's a number
    if user_input.isdigit() or (user_input.startswith('-') and user_input[1:].isdigit()):
        variables[var_name] = int(user_input)
    else:
        variables[var_name] = user_input  # Keep as string if not numeric
