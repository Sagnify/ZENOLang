# ZENOLang — A Gentle Educational Programming Language

> *"Where human words become code,
> and learning blooms with every line."*

---

## Overview

**ZENOLang** is a thoughtfully crafted **natural-language-inspired programming language and interpreter**, designed from the ground up to **make programming intuitive and approachable for beginners and curious minds**.

Inspired by the rhythms of everyday language, ZENOLang lets you write code that *feels like conversation* — mixing simple English phrases with powerful programming concepts. It’s an educational tool bridging the gap between human thought and computational logic.

---

## What’s Done So Far

### ✅ Core Interpreter Built in Python

* Natural language style commands like:

  * `let x be 5`
  * `say "Hello, world!"`
  * `while condition then ...`
  * `if condition then ... else ...`
  * `ask "Prompt" into variable`
  * `stop` (to break loops)
* Indentation-based block parsing
* Handles variables, numbers, booleans, and strings
* Prints numbers automatically as strings during `say` or concatenation

### ✅ Expression Evaluator

* Supports:

  * Arithmetic operations (`adds`, `minus`, `multiplies`, `divides`, `modulus`)
  * Comparisons (`is`, `isn't`, `more`, `less`, `greater`, `less than or equal`, etc.)
  * Logical operations (`and`, `or`, `not`)
  * Parentheses for grouping and precedence
* Evaluates natural-English expressions easily

### ✅ Conditionals and Loops

* `if-else` structure with support for nesting
* `while` loops with break using `stop`
* `repeat counting from X to Y with step Z` loop (similar to for-loop)

### ✅ Functions Support

* Define functions with:

  ```zeno
  define greet with name
      say "Hello, " + name + "!"
  ```
* Call with:

  ```zeno
  call greet with "Sagnik"
  ```
* Support for:

  * Multiple parameters (comma-separated)
  * Return values using `return`
  * Recursive functions
  * Assigning function call result to variables

### ✅ String Utility Functions

* `length of <string>` returns string length
* `if <string> contains <substring>` evaluates inclusion

### ✅ Sample Programs Include:

* Divisibility checker using loops
* Factorial (both iterative and recursive)
* Grade evaluator using `if-else` and function call
* Arithmetic function composition (e.g., `add`, `factorial`, etc.)

### ✅ User-Friendly Output

* `say` command prints readable, conversational output
* Concatenation and mixed-type messages handled naturally

---

## Why ZENOLang?

* **Designed for learners:** Avoids intimidating syntax, uses simple English phrases to express logic
* **Encourages experimentation:** Easy to write and modify code to explore programming fundamentals
* **Clear feedback:** Errors and runtime messages crafted to teach as well as inform
* **Extensible:** Built modularly to allow adding new commands and expressions

---

## What’s Next?

* List/array support and indexing
* File/module imports
* Enhanced error handling (undefined variables, bad types)
* Step-through execution and debugging tools
* Visual and GUI integrations
* Interactive input modules and small games

---

## Getting Started

1. Clone the repository
2. Install Python 3.x if you don’t have it
3. Run the interpreter on your `.znl` scripts
4. Explore and create programs using natural language commands!

---

## Example

```zeno
let number be 15
let divisor be 2
let found be 0

say "Checking divisibility of " + number

while found is 0 then
    if number modulus divisor is 0 then
        say "Found divisor: " + divisor
        let found be 1
    else
        say number + " is not divisible by " + divisor
        let divisor be divisor adds 1

    if divisor more number then
        say "No divisor found (number is prime)"
        let found be 1
```

---

```zeno
// Function Example

define factorial with n
    if n less 2 then
        return 1
    else
        let prev be n minus 1
        let result be call factorial with prev
        return n multiplies result

let number be 5
let fact be call factorial with number
say "Factorial of " + number + " is " + fact
```

---
