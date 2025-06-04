"""
Comprehensive Test Suite for Natural Language Expression Evaluator
"""

import unittest
from .main import NaturalLanguageEvaluator, evaluate_expression


class TestNaturalLanguageEvaluator(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.evaluator = NaturalLanguageEvaluator()
        self.variables = {
            "x": 5,
            "y": 10,
            "z": 3,
            "flag": False,
            "name": "Sagnik",
            "score": 85.5,
            "count": 0
        }
    
    def test_arithmetic_operations(self):
        """Test basic arithmetic operations"""
        test_cases = [
            ("x add y", 15),
            ("x plus y", 15),
            ("y minus x", 5),
            ("x multiply z", 15),
            ("y times z", 30),
            ("y divide x", 2.0),
            ("y divided_by x", 2.0),
            ("y modulus z", 1),
            ("x power z", 125),
            ("x to_the_power_of z", 125)
        ]
        
        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                result = self.evaluator.evaluate(expr, self.variables)
                self.assertEqual(result, expected)
    
    def test_comparison_operations(self):
        """Test comparison operations"""
        test_cases = [
            ("x is 5", True),
            ("x equals 5", True),
            ("x isn't 10", True),
            ("x not_equals 10", True),
            ("x less y", True),
            ("y greater x", True),
            ("x atleast 5", True),
            ("x at_least 5", True),
            ("y atmost 10", True),
            ("y at_most 10", True)
        ]
        
        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                result = self.evaluator.evaluate(expr, self.variables)
                self.assertEqual(result, expected)
    
    def test_string_operations(self):
        """Test string operations"""
        test_cases = [
            ("name contains 'Sag'", True),
            ("name contains 'xyz'", False),
            ("name startswith 'Sag'", True),
            ("name startswith 'nik'", False),
            ("name endswith 'nik'", True),
            ("name endswith 'Sag'", False)
        ]
        
        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                result = self.evaluator.evaluate(expr, self.variables)
                self.assertEqual(result, expected)
    
    def test_logical_operations(self):
        """Test logical operations"""
        test_cases = [
            ("x greater 3 and y less 15", True),
            ("x greater 10 and y less 15", False),
            ("x greater 10 or y less 15", True),
            ("flag or x equals 5", True),
            ("not flag", True),
            ("not flag and x equals 5", True)
        ]
        
        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                result = self.evaluator.evaluate(expr, self.variables)
                self.assertEqual(result, expected)
    
    def test_between_expressions(self):
        """Test between expressions"""
        test_cases = [
            ("x between 1 to 10", True),
            ("x between 6 to 10", False),
            ("score between 80 to 90", True),
            ("score between 90 to 100", False)
        ]
        
        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                result = self.evaluator.evaluate(expr, self.variables)
                self.assertEqual(result, expected)
    
    def test_bracket_expressions(self):
        """Test expressions with brackets"""
        test_cases = [
            ("(x add y) multiply z", 45),
            ("x add (y multiply z)", 35),
            ("((x add y) multiply z) add 5", 50),
            ("(x add y) between (z multiply 2) to (z multiply 6)", True),
            ("(x greater 3) and (y less 15)", True)
        ]
        
        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                result = self.evaluator.evaluate(expr, self.variables)
                self.assertEqual(result, expected)
    
    def test_complex_expressions(self):
        """Test complex mixed expressions"""
        test_cases = [
            ("x modulus z is 2", True),
            ("(x add y) divide z greater 4", True),
            ("name contains 'Sag' and x greater z", True),
            ("score between 80 to 90 and name startswith 'Sag'", True)
        ]
        
        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                result = self.evaluator.evaluate(expr, self.variables)
                self.assertEqual(result, expected)
    
    def test_string_concatenation(self):
        """Test string concatenation"""
        string_vars = {"first": "Hello", "second": "World", "space": " "}
        
        test_cases = [
            ("first + space + second", "Hello World"),
            ("'Hello' + ' ' + 'World'", "Hello World")
        ]
        
        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                result = self.evaluator.evaluate(expr, string_vars)
                self.assertEqual(result, expected)
    
    def test_quoted_strings(self):
        """Test quoted string handling"""
        test_cases = [
            ("'hello world'", "hello world"),
            ('"hello world"', "hello world"),
            ("'hello' contains 'ell'", True),
            ('"test string" startswith "test"', True)
        ]
        
        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                result = self.evaluator.evaluate(expr, {})
                self.assertEqual(result, expected)
    
    def test_boolean_values(self):
        """Test boolean value handling"""
        test_cases = [
            ("True", True),
            ("False", False),
            ("True and False", False),
            ("True or False", True),
            ("not True", False),
            ("not False", True)
        ]
        
        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                result = self.evaluator.evaluate(expr, {})
                self.assertEqual(result, expected)
    
    def test_edge_cases(self):
        """Test edge cases and error handling"""
        # Division by zero
        result = self.evaluator.evaluate("x divide count", self.variables)
        self.assertEqual(result, float('inf'))
        
        # Modulus by zero
        result = self.evaluator.evaluate("x modulus count", self.variables)
        self.assertEqual(result, float('inf'))
        
        # Invalid variable (should return error message)
        result = self.evaluator.evaluate("unknown_var", {})
        self.assertIn("[Error", str(result))
    
    def test_convenience_function(self):
        """Test the convenience function"""
        result = evaluate_expression("x add y", {"x": 5, "y": 10})
        self.assertEqual(result, 15)
    
    def test_custom_operators(self):
        """Test adding custom operators"""
        # Add a custom operator
        self.evaluator.add_operator("max", lambda x, y: max(x, y))
        
        result = self.evaluator.evaluate("x max y", self.variables)
        self.assertEqual(result, 10)


class TestPerformance(unittest.TestCase):
    """Performance tests for the evaluator"""
    
    def setUp(self):
        self.evaluator = NaturalLanguageEvaluator()
        self.variables = {"x": 5, "y": 10, "z": 3}
    
    def test_simple_expression_performance(self):
        """Test performance of simple expressions"""
        import time
        
        expr = "x add y multiply z"
        start_time = time.time()
        
        # Run 1000 evaluations
        for _ in range(1000):
            self.evaluator.evaluate(expr, self.variables)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete 1000 evaluations in reasonable time (< 1 second)
        self.assertLess(duration, 1.0, "Performance test failed - took too long")
    
    def test_complex_expression_performance(self):
        """Test performance of complex expressions"""
        import time
        
        expr = "((x add y) multiply z) between (z multiply 2) to (z multiply 10) and x greater 3"
        start_time = time.time()
        
        # Run 100 evaluations
        for _ in range(100):
            self.evaluator.evaluate(expr, self.variables)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete 100 complex evaluations in reasonable time (< 1 second)
        self.assertLess(duration, 1.0, "Complex expression performance test failed")


if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)