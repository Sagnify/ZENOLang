"""
Evaluator Module - Core expression evaluation logic
"""

import re
import ast
from typing import Any, Dict
from .parser import ExpressionParser
from .operators import OPERATORS, OPERATOR_SYMBOLS, is_arithmetic_only, is_arithmetic_comparison


class ExpressionEvaluator:
    """Core expression evaluation engine"""
    
    def __init__(self, operators: Dict[str, Any] = None):
        self.operators = operators or OPERATORS.copy()
        self.parser = ExpressionParser()
    
    def add_operator(self, name: str, func: callable, symbol: str = None):
        """Add a custom operator"""
        self.operators[name] = func
        if symbol:
            OPERATOR_SYMBOLS[name] = symbol
    
    def evaluate(self, expression: str, variables: Dict[str, Any]) -> Any:
        """Main evaluation method with bracket handling"""
        expression = expression.strip()
        
        # Handle brackets recursively
        if '(' in expression and ')' in expression:
            expression = self._evaluate_brackets_recursively(expression, variables)
        
        # Evaluate the final expression
        return self._evaluate_without_brackets(expression, variables)
    
    def _evaluate_brackets_recursively(self, expression: str, variables: Dict[str, Any]) -> str:
        """Recursively evaluate brackets from innermost to outermost"""
        while '(' in expression and ')' in expression:
            bracket_info = self.parser.find_innermost_brackets(expression)
            if not bracket_info:
                break
            
            start_pos, end_pos, bracket_content = bracket_info
            
            try:
                bracket_result = self._evaluate_without_brackets(bracket_content.strip(), variables)
                
                # Convert result to string representation
                if isinstance(bracket_result, str):
                    result_str = f'"{bracket_result}"'
                else:
                    result_str = str(bracket_result)
                
                expression = expression[:start_pos] + result_str + expression[end_pos+1:]
                
            except Exception as e:
                raise ValueError(f"Error evaluating bracket content '{bracket_content}': {e}")
        
        return expression
    
    def _evaluate_without_brackets(self, expression: str, variables: Dict[str, Any]) -> Any:
        """Evaluate expression without brackets"""
        expression = expression.strip()
        # print(f"Expression: {expression!r}")
        # print("Contains '+':", '+' in expression)
        # print("Contains 'add' or 'plus':", any(op in expression.lower() for op in ['add', 'plus']))
        
        
        # Handle quoted strings
        if self.parser.is_quoted_string(expression):
            # print("Calling parse_value for quoted string:", expression)
            return self.parser.parse_value(expression, variables)
        
        # Handle unary NOT
        if expression.lower().startswith('not '):
            inner_expr = expression[4:].strip()
            val = self._evaluate_without_brackets(inner_expr, variables)
            if isinstance(val, bool):
                return not val
            else:
                return f"[Error: Cannot apply 'not' to {val}]"
        
        # Handle string concatenation
        if '+' in expression:
            # print("Calling _handle_string_concatenation for:", expression)
            return self._handle_string_concatenation(expression, variables)
        
        # Handle single values
        if not self._contains_operators(expression):
            # print("Calling _handle_single_value for:", expression)
            return self.parser.parse_value(expression, variables)
        
        # Handle special cases
        if 'between' in expression.lower():
            # print("Calling _handle_between_expression for:", expression)
            return self._handle_between_expression(expression, variables)
        
        if is_arithmetic_comparison(expression):
            # print("Calling _handle_arithmetic_comparison for:", expression)
            return self._handle_arithmetic_comparison(expression, variables)
        
        if is_arithmetic_only(expression):
            # print("Calling _handle_arithmetic_expression for:", expression)
            return self._handle_arithmetic_expression(expression, variables)
        
        # Handle complex expressions with AST
        if self._is_complex_expression(expression):
            # print("Calling _evaluate_complex_expression for:", expression)
            return self._evaluate_complex_expression(expression, variables)
        

        # Handle simple binary operations
        # print("Calling _handle_binary_operation for:", expression)
        return self._handle_binary_operation(expression, variables)
    
    def _handle_string_concatenation(self, expression: str, variables: Dict[str, Any]) -> str:
        """Handle string concatenation with +"""
        parts = self.parser.split_outside_quotes(expression, '+')
        # print("Split parts:", parts)
        results = []
        
        for i, p in enumerate(parts):
            val = str(self._evaluate_without_brackets(p.strip(), variables))
            # print(f"Evaluating part: {p.strip()} -> {val}")
            results.append(val)

        if all(isinstance(v, str) for v in results):
            result = ''.join(results)
            return result
        else:
            raise TypeError("Operator '+' is only for string concatenation.")
        
    
    def _handle_between_expression(self, expression: str, variables: Dict[str, Any]) -> bool:
        """Handle 'value between lower to upper' expressions"""
        value_part, lower_part, upper_part = self.parser.extract_between_expression(expression)
        
        value = self.parser.parse_value(value_part, variables)
        lower_bound = self.parser.parse_value(lower_part, variables)
        upper_bound = self.parser.parse_value(upper_part, variables)
        
        return lower_bound <= value <= upper_bound
    
    def _handle_arithmetic_comparison(self, expression: str, variables: Dict[str, Any]) -> bool:
        """Handle arithmetic comparisons like 'a modulus b is c'"""
        # Find comparison operator
        comparison_op, _ = self.parser.find_operator_in_expression(
            expression, {k: v for k, v in self.operators.items() 
                        if k in ['is', 'equals', 'isn\'t', 'not_equals', 'less', 'more', 'greater', 
                                'atleast', 'at_least', 'atmost', 'at_most']}
        )
        
        if not comparison_op:
            raise ValueError(f"No comparison operator found: '{expression}'")
        
        # Split at comparison operator
        parts = re.split(r'\b' + re.escape(comparison_op) + r'\b', expression, flags=re.IGNORECASE)
        if len(parts) != 2:
            raise ValueError(f"Invalid arithmetic comparison format: '{expression}'")
        
        left_expr = parts[0].strip()
        right_value_str = parts[1].strip()
        
        # Evaluate arithmetic expression on left
        arithmetic_result = self._handle_arithmetic_expression(left_expr, variables)
        right_value = self.parser.parse_value(right_value_str, variables)
        
        # Perform comparison
        return self.operators[comparison_op](arithmetic_result, right_value)
    
    def _handle_arithmetic_expression(self, expression: str, variables: Dict[str, Any]) -> Any:
        """Handle pure arithmetic expressions"""
        # Find arithmetic operator
        arithmetic_op, _ = self.parser.find_operator_in_expression(
            expression, {k: v for k, v in self.operators.items() 
                        if k in ['add', 'adds', 'plus', 'subtract', 'subtracts', 'minus',
                                'multiply', 'multiplies', 'times', 'divide', 'divides', 'divided_by',
                                'modulus', 'mod', 'power', 'to_the_power_of']}
        )
        
        if not arithmetic_op:
            raise ValueError(f"No arithmetic operator found: '{expression}'")
        
        # Split and evaluate
        parts = re.split(r'\b' + re.escape(arithmetic_op) + r'\b', expression, flags=re.IGNORECASE)
        if len(parts) != 2:
            raise ValueError(f"Invalid arithmetic expression format: '{expression}'")
        
        left_value = self.parser.parse_value(parts[0].strip(), variables)
        right_value = self.parser.parse_value(parts[1].strip(), variables)
        
        return self.operators[arithmetic_op](left_value, right_value)
    
    def _handle_binary_operation(self, expression: str, variables: Dict[str, Any]) -> Any:
        """Handle simple binary operations"""
        operator_found, _ = self.parser.find_operator_in_expression(expression, self.operators)
        
        if not operator_found:
            raise ValueError(f"No valid operator found: '{expression}'")
        
        parts = self.parser.split_outside_quotes(expression, operator_found)
        if len(parts) != 2:
            raise ValueError(f"Invalid expression format: '{expression}'")
        
        left_value = self.parser.parse_value(parts[0].strip(), variables)
        # print(f"Left value: {left_value!r}")
        # print(f"Operator: {operator_found!r}")
        right_value = self.parser.parse_value(parts[1].strip(), variables)
        # print(f"Right value: {right_value!r}")
        
        return self.operators[operator_found](left_value, right_value)
    
    def _evaluate_complex_expression(self, expression: str, variables: Dict[str, Any]) -> Any:
        """Evaluate complex expressions using AST"""
        # Replace operators with Python equivalents
        for word_op, symbol in sorted(OPERATOR_SYMBOLS.items(), key=lambda x: -len(x[0])):
            pattern = r'\b' + re.escape(word_op) + r'\b'
            expression = re.sub(pattern, f' {symbol} ', expression, flags=re.IGNORECASE)
        
        # Replace variables
        for var in variables:
            pattern = r'\b' + re.escape(var) + r'\b'
            replacement = f'"{variables[var]}"' if isinstance(variables[var], str) else str(variables[var])
            expression = re.sub(pattern, replacement, expression)
        
        # Safe evaluation using AST
        try:
            tree = ast.parse(expression, mode='eval')
            self._validate_ast_safety(tree)
            return eval(compile(tree, filename="<ast>", mode="eval"))
        except Exception as e:
            raise ValueError(f"Error evaluating complex expression: {e}")
    
    def _validate_ast_safety(self, tree: ast.AST):
        """Validate AST for safety - no function calls, imports, etc."""
        class SafeVisitor(ast.NodeVisitor):
            def visit_Call(self, node):
                raise ValueError("Function calls not allowed")
            def visit_Attribute(self, node):
                raise ValueError("Attribute access not allowed")
            def visit_Import(self, node):
                raise ValueError("Imports not allowed")
            def visit_ImportFrom(self, node):
                raise ValueError("Imports not allowed")
        
        SafeVisitor().visit(tree)
    
    def _contains_operators(self, expression: str) -> bool:
        """Check if expression contains any operators"""
        return any(op in expression.lower().split() for op in self.operators.keys())
    
    def _is_complex_expression(self, expression: str) -> bool:
        """Check if expression is complex (contains logical operators)"""
        logical_ops = ['and', 'or', 'not']
        return any(f' {op} ' in expression.lower() for op in logical_ops)