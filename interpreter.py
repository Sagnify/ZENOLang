from modules.evaluator.context import set_evaluator
from modules.evaluator.main import NaturalLanguageEvaluator
from modules import runner, custom_operators
import sys
import os

# Initialize and set evaluator
evaluator = NaturalLanguageEvaluator()
set_evaluator(evaluator)
custom_operators.register_custom_operators()

class ZENOLangInterpreter:
    def __init__(self):
        self.variables = {}

    def run(self, lines):
        runner.run_script(lines, self.variables)

def pause_if_needed():
    # Only pause if launched by double-click (i.e. not from terminal)
    if os.environ.get('PROMPT') is None and os.environ.get('TERM') is None:
        input("\n[Press Enter to close ZENOLang interpreter...]")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("ZENOLang Interpreter v1.0")
        print("Usage: zeno <script_file.znl>")
        sys.exit(0)

    script_file = sys.argv[1]

    if not script_file.endswith(".znl"):
        print("Error: Please provide a .znl file.")
        pause_if_needed()
        sys.exit(1)

    try:
        with open(script_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{script_file}' not found.")
        pause_if_needed()
        sys.exit(1)

    interpreter = ZENOLangInterpreter()
    interpreter.run(lines)

    pause_if_needed()
