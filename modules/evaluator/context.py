_evaluator = None

def set_evaluator(evaluator_instance):
    global _evaluator
    _evaluator = evaluator_instance
    print("Evaluator set successfully!")

def get_evaluator():
    global _evaluator
    if _evaluator is None:
        raise RuntimeError("Evaluator not set yet!")
    return _evaluator
