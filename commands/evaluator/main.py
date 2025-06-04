"""
Natural Language Expression Evaluator - Main Module
Handles expression parsing and evaluation coordination
"""

from typing import Any, Dict
from .parser import ExpressionParser
from .operators import OPERATORS
from .evaluator import ExpressionEvaluator
from .utils import is_quoted_string, split_outside_quotes


class NaturalLanguageEvaluator:
    """Main evaluator class that coordinates all expression evaluation"""
    
    def __init__(self):
        self.parser = ExpressionParser()
        self.evaluator = ExpressionEvaluator(OPERATORS)
    
    def evaluate(self, expression: str, variables: Dict[str, Any] = None) -> Any:
        """
        Main evaluation method
        
        Args:
            expression: Natural language expression to evaluate
            variables: Dictionary of variable name -> value mappings
            
        Returns:
            Result of the expression evaluation
        """
        if variables is None:
            variables = {}
            
        try:
            # Parse and evaluate the expression
            return self.evaluator.evaluate(expression.strip(), variables)
        except Exception as e:
            return f"[Error: {e}]"
    
    def add_operator(self, name: str, func: callable, symbol: str = None):
        """Add a custom operator"""
        self.evaluator.add_operator(name, func, symbol)
    
    def add_variable(self, name: str, value: Any, variables: Dict[str, Any]):
        """Helper to add variables"""
        variables[name] = value


# Convenience function for direct use
def evaluate_expression(expression: str, variables: Dict[str, Any] = None) -> Any:
    """Convenience function for direct expression evaluation"""
    evaluator = NaturalLanguageEvaluator()
    return evaluator.evaluate(expression, variables)


# Example usage
if __name__ == "__main__":
    # Test cases
    variables = {
        "x": 5,
        "y": 10,
        "z": 3,
        "flag": False,
        "name": "Sagnik"
    }
    
    test_cases = [
#         "(x add y) multiply 2",
#         "((x add y) multiply 2) add 5", 
#         "(x add y) between (z multiply 2) to (z multiply 6)",
#         "x modulus y is 5",
#         "name contains 'Sag'",
#         "x greater 3 and y less 15",
#         "not flag or x equals 5",
#         "'Hi ' + name + '!'",
#         "'Hello' + ' ' + 'World!'",
#         "'Hello' contains 'ell'"
            '"Checking if " + x + " is divisible by " + y'

    ]
    
    evaluator = NaturalLanguageEvaluator()
    
    print("Testing Expression Evaluator:")
    print("-" * 40)
    
    for expr in test_cases:
        result = evaluator.evaluate(expr, variables)
        print(f"{expr:35} = {result}")