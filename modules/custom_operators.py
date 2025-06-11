from modules.evaluator.context import get_evaluator
from math import floor

def register_custom_operators():
    evaluator = get_evaluator()
    evaluator.add_operator("length", lambda value: len(value))
    evaluator.add_operator("reverse", lambda value: value[::-1])
    evaluator.add_operator("floor", lambda value: floor(value))
    evaluator.add_operator("upper", lambda value: value.upper())
    evaluator.add_operator("lower", lambda value: value.lower())