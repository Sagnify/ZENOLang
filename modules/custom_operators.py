from modules.evaluator.context import get_evaluator

# Register unary string operators using lambdas
evaluator = get_evaluator()
evaluator.add_operator("length", lambda value: len(value))
evaluator.add_operator("reverse", lambda value: value[::-1])
