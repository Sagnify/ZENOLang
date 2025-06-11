
from . import let, say, ask, if_else, while_, for_, list_operations
from .exception_case import BreakLoop
from . import function_handler
from .function_handler import ReturnValue


def get_indent_level(line):
    # Convert tabs to spaces (4 spaces per tab)
    line_expanded = line.expandtabs(4)
    return len(line_expanded) - len(line_expanded.lstrip(' '))

def find_matching_else(lines, if_line_index, if_indent):
    """Find the else that matches the if at if_line_index"""
    i = if_line_index + 1
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith('#') or line.startswith('//'):
            i += 1
            continue

        current_indent = get_indent_level(lines[i])

        # If we hit same indentation level
        if current_indent == if_indent and line == 'else':
            return i
        elif current_indent == if_indent or current_indent < if_indent:
            # Hit another statement at same level, no else
            return None
        i += 1
    return None

def run_script(lines, variables):  # sourcery skip: use-contextlib-suppress
    i = 0
    return_value = None

    while i < len(lines):
        line = lines[i].rstrip('\n')
        indent = get_indent_level(line)
        stripped = line.strip()

        # Skip empty lines and comments
        if not stripped or stripped.startswith(('#', '//')):
            i += 1
            continue

        try:
            if stripped.startswith('let '):
                let.execute(stripped, variables, run_script)
                i += 1

            elif stripped.startswith('say '):
                say.execute(stripped, variables)
                i += 1

            elif stripped.startswith('ask '):
                ask.execute(stripped, variables)
                i += 1

            elif stripped.startswith('return'):
                # Handle return statement using function_handler
                # You'll need to pass your expression evaluator here
                function_handler.handle_return_statement(stripped, variables)

            elif stripped.startswith('if '):
                condition = if_else.evaluate(stripped, variables)

                # Find all lines in the if block
                if_block = []
                else_block = []
                j = i + 1

                # Collect if block
                while j < len(lines):
                    current_line = lines[j].strip()
                    if not current_line or current_line.startswith('#') or current_line.startswith('//'):
                        j += 1
                        continue

                    current_indent = get_indent_level(lines[j])

                    if current_indent <= indent:
                        break

                    if_block.append(lines[j])
                    j += 1

                # Check if there's an else at the same indentation level
                else_index = find_matching_else(lines, i, indent)
                if else_index is not None:
                    # Collect else block
                    j = else_index + 1
                    while j < len(lines):
                        current_line = lines[j].strip()
                        if not current_line or current_line.startswith('#') or current_line.startswith('//'):
                            j += 1
                            continue

                        current_indent = get_indent_level(lines[j])

                        if current_indent <= indent:
                            break

                        else_block.append(lines[j])
                        j += 1

                # Execute the appropriate block
                if condition:
                    if if_block:
                        try:
                            run_script(if_block, variables)
                        except (BreakLoop, ReturnValue):
                            raise
                elif else_block:
                    try:
                        run_script(else_block, variables)
                    except (BreakLoop, ReturnValue):
                        raise

                i = j

            elif stripped == 'else':
                print(f"Unexpected 'else' at line {i+1} - this should be handled by if statement")
                i += 1

            elif stripped.startswith('while '):
                # Collect the while block
                while_block = []
                j = i + 1

                while j < len(lines):
                    current_line = lines[j].strip()
                    if not current_line or current_line.startswith('#') or current_line.startswith('//'):
                        j += 1
                        continue

                    current_indent = get_indent_level(lines[j])

                    if current_indent <= indent:
                        break

                    while_block.append(lines[j])
                    j += 1

                try:
                    while while_.evaluate(stripped, variables):
                        if while_block:
                            try:
                                run_script(while_block, variables)
                            except BreakLoop:
                                break
                            except ReturnValue:
                                raise
                except BreakLoop:
                    pass

                i = j

            elif stripped.startswith('repeat counting '):
                indent = get_indent_level(lines[i])
                var_name, start, end, step = for_.evaluate(stripped, variables)

                # Collect the repeat block
                repeat_block = []
                j = i + 1
                while j < len(lines):
                    current_line = lines[j].strip()
                    if not current_line or current_line.startswith('#') or current_line.startswith('//'):
                        j += 1
                        continue

                    current_indent = get_indent_level(lines[j])
                    if current_indent <= indent:
                        break

                    repeat_block.append(lines[j])
                    j += 1

                try:
                    step_sign = 1 if step > 0 else -1
                    for val in range(start, end + step_sign, step):
                        variables[var_name] = val
                        if repeat_block:
                            try:
                                run_script(repeat_block, variables)
                            except BreakLoop:
                                break
                            except ReturnValue:
                                raise
                except BreakLoop:
                    pass

                i = j
            
            elif stripped.startswith("repeat each "):
                indent = get_indent_level(lines[i])
                
                # Use your new evaluator
                var_name, iterable = for_.evaluate_list_loop(stripped, variables)

                # Collect the repeat block
                repeat_block = []
                j = i + 1
                while j < len(lines):
                    current_line = lines[j].strip()
                    if not current_line or current_line.startswith('#') or current_line.startswith('//'):
                        j += 1
                        continue

                    current_indent = get_indent_level(lines[j])
                    if current_indent <= indent:
                        break

                    repeat_block.append(lines[j])
                    j += 1

                # Execute block for each item
                try:
                    for val in iterable:
                        variables[var_name] = val
                        if repeat_block:
                            try:
                                run_script(repeat_block, variables)
                            except BreakLoop:
                                break
                            except ReturnValue:
                                raise
                except BreakLoop:
                    pass

                i = j
            elif (stripped.startswith("add ") or 
                stripped.startswith("remove ") or 
                stripped.startswith("length of ") or
                (" at " in stripped and " in " in stripped)):
                list_operations.handle_list_command(stripped, variables)
                i += 1


            elif stripped.startswith('stop'):
                raise BreakLoop()
            
            # Function definition handling
            elif function_handler.is_function_definition(stripped):
                func_name, params = function_handler.parse_function_definition(stripped)
                func_body, next_i = function_handler.collect_function_body(lines, i)
                function_handler.register_function(func_name, params, func_body)
                i = next_i
                continue

            # Function call handling
            elif function_handler.is_function_call(stripped):
                func_name, args = function_handler.parse_function_call(stripped)
                if function_handler.function_exists(func_name):
                    # Execute function - pass run_script and optionally your expression evaluator
                    # Example: ret_val = function_handler.execute_function(func_name, args, variables, run_script, your_expression_module.evaluate)
                    ret_val = function_handler.execute_function(func_name, args, variables, run_script)
                    # Handle return value if needed (e.g., for assignment)
                else:
                    print(f"Function '{func_name}' is not defined")
                i += 1
                continue

            else:
                print(f"Unknown command at line {i+1}: {stripped}")
                i += 1

        except BreakLoop:
            raise
        except ReturnValue:
            raise
        except Exception as e:
            print(f"Error: {e}")
            return

    return return_value