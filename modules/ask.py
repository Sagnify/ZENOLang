def execute(line, variables):
    parts = line.split()
    if len(parts) != 2:
        raise SyntaxError("Invalid syntax in 'ask' command")
    var_name = parts[1].strip()
    user_input = input(">> ")
    variables[var_name] = user_input.strip()  # Store user input in the variable