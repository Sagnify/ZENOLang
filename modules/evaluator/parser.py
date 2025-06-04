"""
Parser Module - Handles parsing of values and expressions
"""

import re
from typing import Any, Dict, List, Tuple, Optional


class ExpressionParser:
    """Handles parsing of natural language expressions"""

    def parse_value(self, value_str: str, variables: Dict[str, Any]) -> Any:
        """Parse a value from string with enhanced boolean and expression handling"""
        original_value_str = value_str
        value_str = value_str.strip()

        # Handle quoted strings (only if quotes match exactly)
        if (value_str.startswith('"') and value_str.endswith('"')) or \
        (value_str.startswith("'") and value_str.endswith("'")):
            # Strip exactly one quote from both ends
            value_str = value_str[1:-1]
            # Don't strip spaces inside quotes! Just return as is.
            return value_str

        # Handle boolean values (case-sensitive True/False)
        if value_str == 'True':
            return True
        elif value_str == 'False':
            return False
        elif value_str.lower() in ['null', 'none']:
            return None

        # Handle numbers (including negative and floats)
        num_str = value_str
        if num_str.startswith('-'):
            num_str = num_str[1:]
        if num_str.replace('.', '', 1).isdigit():
            num_val = float(value_str) if '.' in value_str else int(value_str)
            return num_val

        # Handle variables
        if value_str in variables:
            var_val = variables[value_str]
            return var_val

        # If nothing matches, raise an error
        raise ValueError(f"Cannot resolve value: '{value_str}'")
    
    def contains_operator_outside_quotes(self, s: str, operators: list) -> bool:
        s = s.strip()
        # For each operator, check if it appears outside quotes
        for op in operators:
            parts = self.split_outside_quotes(s, op)
            if len(parts) > 1:
                return True
        return False

    
    def is_quoted_string(self, s: str) -> bool:
        s = s.strip()
        if (s.startswith("'") and s.endswith("'")) or (s.startswith('"') and s.endswith('"')):
            # Check if contains operators outside quotes
            operators = ['+', 'contains', 'startswith', 'endswith', 'and', 'or', 'not']
            if self.contains_operator_outside_quotes(s, operators):
                return False
            # No operators outside quotes, so this is a single quoted string
            return True
        return False


    
    def is_number(self, s: str) -> bool:
        """Check if string represents a number"""
        try:
            float(s)
            return True
        except ValueError:
            return False
    
    def split_outside_quotes(self, text: str, sep: str) -> list[str]:
        parts = []
        current = []
        in_single_quote = False
        in_double_quote = False
        i = 0
        sep_len = len(sep)
        while i < len(text):
            c = text[i]
            # Toggle quote states
            if c == "'" and not in_double_quote:
                in_single_quote = not in_single_quote
                current.append(c)
            elif c == '"' and not in_single_quote:
                in_double_quote = not in_double_quote
                current.append(c)
            # If we're outside quotes and the substring at i matches sep
            elif not in_single_quote and not in_double_quote and text[i:i+sep_len] == sep:
                parts.append(''.join(current).strip())
                current = []
                i += sep_len
                continue
            else:
                current.append(c)
            i += 1
        # Append the last chunk
        parts.append(''.join(current).strip())
        return parts
    
    def find_operator_in_expression(self, expression: str, operators: Dict[str, Any]) -> Tuple[Optional[str], int]:
        """Find the first operator in expression and return (operator, position)"""
        # Sort operators by length (longest first) to match longer operators first
        sorted_ops = sorted(operators.keys(), key=len, reverse=True)
        
        for op in sorted_ops:
            pattern = r'\b' + re.escape(op) + r'\b'
            match = re.search(pattern, expression, re.IGNORECASE)
            if match:
                return op, match.start()
        
        return None, -1
    
    def extract_between_expression(self, expression: str) -> Tuple[str, str, str]:
        """Extract parts from 'value between lower to upper' expression"""
        pattern = r'(.+?)\s+between\s+(.+?)\s+to\s+(.+)'
        match = re.search(pattern, expression, re.IGNORECASE)
        
        if not match:
            raise ValueError("Invalid between expression. Use: 'value between lower to upper'")
        
        return (match.group(1).strip(), 
                match.group(2).strip(), 
                match.group(3).strip())
    
    def find_innermost_brackets(self, expression: str) -> Optional[Tuple[int, int, str]]:
        """Find innermost bracket pair and return (start_pos, end_pos, content)"""
        bracket_pairs = []
        stack = []
        
        for i, char in enumerate(expression):
            if char == '(':
                stack.append(i)
            elif char == ')' and stack:
                start = stack.pop()
                bracket_pairs.append((start, i, expression[start+1:i]))
        
        if not bracket_pairs:
            return None
        
        # Find bracket pair with no nested brackets
        for start, end, content in bracket_pairs:
            if '(' not in content and ')' not in content:
                return (start, end, content)
        
        # Return shortest bracket pair if all contain nested brackets
        return min(bracket_pairs, key=lambda x: x[1] - x[0])