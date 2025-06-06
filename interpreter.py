from modules.evaluator.context import set_evaluator
from modules.evaluator.main import NaturalLanguageEvaluator

# Initialize and set evaluator before importing any modules that use it
evaluator = NaturalLanguageEvaluator()
set_evaluator(evaluator)

# Now import modules that require the evaluator
from modules import runner, custom_operators
import sys


class ZENOLangInterpreter:
    def __init__(self):
        self.variables = {}

    def run(self, lines):
        runner.run_script(lines, self.variables)


if __name__ == "__main__":
    print("ZENOLang Interpreter initialized successfully.")

    if len(sys.argv) < 2:
        print("Usage: python interpreter.py <script_file>")
        sys.exit(1)

    script_file = sys.argv[1]

    if not script_file.endswith(".znl"):
        print("Error: Please provide a ZENOLang file with '.znl' extension.")
        sys.exit(1)

    try:
        with open(script_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{script_file}' not found.")
        sys.exit(1)

    interpreter = ZENOLangInterpreter()
    interpreter.run(lines)
