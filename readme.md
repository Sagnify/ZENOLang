# ZENOLang — A Gentle Educational Programming Language

> *"Where human words become code,  
> and learning blooms with every line."*  

---

## Overview

**ZENOLang** is a thoughtfully crafted **natural-language-inspired programming language and interpreter**, designed from the ground up to **make programming intuitive and approachable for beginners and curious minds**.

Inspired by the rhythms of everyday language, ZENOLang lets you write code that *feels like conversation* — mixing simple English phrases with powerful programming concepts. It’s an educational tool bridging the gap between human thought and computational logic.

---

## What’s Done So Far

- **Core Interpreter** built in Python:
  - Natural language style commands like `let x be 5`, `say "Hello, world!"`, `while condition then ...`
  - Support for variables, strings, numbers, and boolean values
  - Basic arithmetic and string concatenation with clear operator rules
  - Conditional statements (`if-else`)
  - Loops (`while`) with nested blocks using indentation
  - Error handling with meaningful feedback on syntax and runtime issues

- **Expression Evaluator:**
  - Handles arithmetic, comparison, and logical expressions
  - Supports natural language keywords (`adds`, `minus`, `more than`, `less than`, etc.)
  - Robust parsing of complex expressions with brackets and operator precedence
  - True/False booleans handled in intuitive English form (`true`, `false`)

- **Sample Programs Included:**
  - Divisibility checker using loops and conditions
  - Factorial calculator demonstrating recursion and loops
  - Conditional branching with nested expressions and variables

- **User-friendly output:**
  - `say` command prints meaningful messages combining literals and evaluated expressions
  - Concatenation and variable interpolation supported naturally

---

## Why ZENOLang?

- **Designed for learners:** Avoids intimidating syntax, uses simple English phrases to express logic
- **Encourages experimentation:** Easy to write and modify code to explore programming fundamentals
- **Clear feedback:** Errors and runtime messages crafted to teach as well as inform
- **Extensible:** Built modularly to allow adding new commands and expressions

---

## What’s Next?

- Step-through execution and debugging tools  
- Enhanced input handling for interactive programs  
- Richer control structures and user-defined functions  
- Visual and GUI integrations for real-time learning  
- Comprehensive tutorial scripts and learning modules

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
