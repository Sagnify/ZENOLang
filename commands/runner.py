from commands import let, say, ask, if_else, while_

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
        if current_indent == if_indent:
            if line == 'else':
                return i
            else:
                # Hit another statement at same level, no else
                return None
        # If we hit lower indentation, no else
        elif current_indent < if_indent:
            return None
            
        i += 1
    return None

def run_script(lines, variables):
    i = 0

    while i < len(lines):
        line = lines[i].rstrip('\n')
        # print(f"Raw line: {repr(line)}")

        indent = get_indent_level(line)
        stripped = line.strip()
        # print(f"[Line {i+1}] Indent={indent} Content='{stripped}'")

        # Skip empty lines and comments
        if not stripped or stripped.startswith(('#', '//')):
            i += 1
            continue

        try:
            if stripped.startswith('let '):
                let.execute(stripped, variables)
                i += 1

            elif stripped.startswith('say '):
                say.execute(stripped, variables)
                i += 1

            elif stripped.startswith('ask '):
                ask.execute(stripped, variables)
                i += 1

            elif stripped.startswith('if '):
                condition = if_else.evaluate(stripped, variables)
                # print(f"  IF condition evaluated to {condition}")
                
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
                    
                    # Skip to after the else block
                    i = j
                else:
                    # No else, skip to after if block
                    i = j
                
                # Execute the appropriate block
                if condition:
                    if if_block:
                        run_script(if_block, variables)
                else:
                    if else_block:
                        run_script(else_block, variables)
                    elif not if_block:  # No if block and no else block
                        # print("  Skipping IF block due to condition False")
                        pass

            elif stripped == 'else':
                # This should not be reached if our logic is correct
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
                
                # Execute while loop
                while while_.evaluate(stripped, variables):
                    if while_block:
                        run_script(while_block, variables)
                
                i = j

            else:
                print(f"Unknown command at line {i+1}: {stripped}")
                i += 1
                
        except Exception as e:
            print(f"Error: {e}")
            return  # Stop execution on error

# Example usage:
# if __name__ == "__main__":
#     # Example script with indentation-based blocks
#     script = """
# let x = 5
# if x > 3
#     say "x is greater than 3"
#     let y = 10
#     if y > 8
#         say "y is also greater than 8"
#     else
#         say "y is not greater than 8"
# else
#     say "x is not greater than 3"

# let counter = 0
# while counter < 3
#     say "Counter is: " + str(counter)
#     let counter = counter + 1
    
# say "Done!"
# """
    
#     variables = {}
#     lines = script.strip().split('\n')
#     run_script(lines, variables)