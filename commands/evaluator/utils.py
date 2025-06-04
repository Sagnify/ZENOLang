"""
Utils Module - Utility functions and helpers
"""

from typing import List, Any


def is_quoted_string(s: str) -> bool:
    """Check if string is properly quoted"""
    s = s.strip()
    return ((s.startswith("'") and s.endswith("'")) or 
            (s.startswith('"') and s.endswith('"'))) and len(s) >= 2


def split_outside_quotes(text: str, separator: str) -> List[str]:
    """Split text by separator, ignoring separators inside quotes"""
    parts = []
    current = []
    in_single_quote = False
    in_double_quote = False
    i = 0
    sep_len = len(separator)
    
    while i < len(text):
        char = text[i]
        
        # Toggle quote states
        if char == "'" and not in_double_quote:
            in_single_quote = not in_single_quote
        elif char == '"' and not in_single_quote:
            in_double_quote = not in_double_quote
        
        # Check for separator outside quotes
        if (not in_single_quote and not in_double_quote and 
            text[i:i+sep_len] == separator):
            parts.append(''.join(current).strip())
            current = []
            i += sep_len
            continue
        
        current.append(char)
        i += 1
    
    parts.append(''.join(current).strip())
    return parts


def safe_divide(x: Any, y: Any) -> float:
    """Safe division that handles division by zero"""
    try:
        return x / y if y != 0 else float('inf')
    except (TypeError, ZeroDivisionError):
        return float('inf')


def safe_modulus(x: Any, y: Any) -> Any:
    """Safe modulus that handles division by zero"""
    try:
        return x % y if y != 0 else float('inf')
    except (TypeError, ZeroDivisionError):
        return float('inf')


def normalize_boolean(value: Any) -> bool:
    """Convert various values to boolean"""
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.lower() not in ['', 'false', '0', 'null', 'none']
    return bool(value)


def format_result(result: Any) -> str:
    """Format result for display"""
    if isinstance(result, bool):
        return str(result)
    elif isinstance(result, float):
        if result == float('inf'):
            return "∞"
        elif result == float('-inf'):
            return "-∞"
        elif result.is_integer():
            return str(int(result))
        else:
            return f"{result:.6g}"
    else:
        return str(result)


def validate_expression_syntax(expression: str) -> tuple[bool, str]:
    """Basic syntax validation for expressions"""
    if not expression or not expression.strip():
        return False, "Empty expression"
    
    # Check for balanced parentheses
    open_count = expression.count('(')
    close_count = expression.count(')')
    if open_count != close_count:
        return False, "Unbalanced parentheses"
    
    # Check for proper quote matching
    single_quotes = expression.count("'")
    double_quotes = expression.count('"')
    if single_quotes % 2 != 0:
        return False, "Unmatched single quotes"
    if double_quotes % 2 != 0:
        return False, "Unmatched double quotes"
    
    return True, "Valid"


class ExpressionCache:
    """Simple cache for expression results"""
    
    def __init__(self, max_size: int = 100):
        self.cache = {}
        self.max_size = max_size
        self.access_order = []
    
    def get(self, expression: str, variables_hash: str) -> Any:
        """Get cached result"""
        key = f"{expression}|{variables_hash}"
        if key in self.cache:
            # Move to end (most recent)
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        return None
    
    def set(self, expression: str, variables_hash: str, result: Any):
        """Cache result"""
        key = f"{expression}|{variables_hash}"
        
        # Remove oldest if at capacity
        if len(self.cache) >= self.max_size and key not in self.cache:
            oldest = self.access_order.pop(0)
            del self.cache[oldest]
        
        self.cache[key] = result
        if key in self.access_order:
            self.access_order.remove(key)
        self.access_order.append(key)
    
    def clear(self):
        """Clear cache"""
        self.cache.clear()
        self.access_order.clear()