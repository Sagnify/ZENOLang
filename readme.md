# ZENOLang — A Gentle Educational Programming Language

> *"Where human words become code,  
> and learning blooms with every line."*

## Overview

**ZENOLang** is a thoughtfully crafted **natural-language-inspired programming language and interpreter**, designed from the ground up to **make programming intuitive and approachable for beginners and curious minds**.

Inspired by the rhythms of everyday language, ZENOLang lets you write code that *feels like conversation* — mixing simple English phrases with powerful programming concepts. It's an educational tool bridging the gap between human thought and computational logic.

## Features

### ✅ Core Language Features

- **Natural language style commands:**
  - `let x be 5`
  - `say "Hello, world!"`
  - `while condition then ...`
  - `if condition then ... else ...`
  - `ask variable`
  - `stop` (to break loops)
  - `repeat counting i start to end`
  - `repeat each item in list ` (supports list operations)
  
- **Indentation-based block parsing**
- **Variable support:** numbers, booleans, and strings
- **Automatic type conversion** for output and concatenation

### ✅ Expression Evaluator

**Arithmetic operations:**
- `adds`, `minus`, `multiplies`, `divides`, `modulus`

**Comparisons:**
- `is`, `isn't`, `more`, `less`, `greater`, `less than or equal`

**Logical operations:**
- `and`, `or`, `not`

**Advanced features:**
- Parentheses for grouping and precedence
- Natural English expression evaluation

### ✅ Control Flow

**Conditionals:**
- `if-else` structure with nesting support

**Loops:**
- `while` loops with `stop` for breaking
- `repeat counting <var> from <start> to <end> [step <step>]` (for-loop equivalent)

### ✅ Functions

**Function definition:**
```zeno
define greet with name
    say "Hello, " + name + "!"
```

**Function calls:**
```zeno
call greet with "Sagnik"
```

**Advanced function features:**
- Multiple parameters (comma-separated)
- Return values using `return`
- Recursive functions
- Assigning function results to variables

### ✅ Data Structures & Utilities

**String operations:**
- `length of <string>` returns string length
- `if <string> contains <substring>` checks inclusion

**List operations:**
- List creation, indexing, adding/removing elements
- Length queries and manipulation

## Why ZENOLang?

- **Designed for learners:** Avoids intimidating syntax; uses simple English phrases to express logic
- **Encourages experimentation:** Easy to write and modify code to explore programming fundamentals
- **Clear feedback:** Errors and runtime messages crafted to teach as well as inform
- **Extensible:** Built modularly to allow adding new commands and expressions over time

## Getting Started

1. Clone the repository
2. Install Python 3.x if you don't have it
3. Run the interpreter on your `.znl` script files
4. Explore and create programs using natural language commands!

## Example Programs

### Example 1: Divisibility Checker

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

### Example 2: Recursive Factorial

```zeno
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

### Example 3: Binary Search

```zeno
define binary_search with target, lst, start, end
    let result be -1

    repeat counting _ from start to end
        if start more end then
            stop

        let mid be floor ((start adds end) divides 2)
        val at mid in lst
        let mid_val be val

        if mid_val is target then
            let result be mid
            stop
        if mid_val less target then
            let start be mid adds 1
        else
            let end be mid minus 1

    return result

let my_list be [1, 3, 5, 7, 9, 11, 13]
let idx be call binary_search with 7, my_list, 0, 6
say idx
```

## Roadmap

### 🚧 What's Next?

- Enhanced list/array operations and advanced indexing
- File/module import system
- Robust error handling (undefined variables, type mismatches)
- Try-catch/finally style exception handling
- Step-through execution and debugging tools
- Visual and GUI integrations
- Interactive input modules and small educational games

## Contributing

We welcome contributions! Whether you're fixing bugs, adding features, or improving documentation, your help makes ZENOLang better for everyone.

## License

[Add your license information here]

---

*With ZENOLang, your journey to programming fluency begins gently — with words, logic, and curiosity as your guides.*