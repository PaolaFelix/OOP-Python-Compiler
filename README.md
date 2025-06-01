# OOP Code Analyzer

## Description

**OOP Code Analyzer** is a lightweight Python tool that detects whether a given piece of code follows **Object-Oriented Programming (OOP)** principles.

It uses a custom **preprocessor** and an **abstract syntax tree (AST)** to evaluate the structural components of OOP, such as:

- Classes  
- Methods  
- Constructors (`__init__`)  
- Attributes  
- Instance usage

---

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.7 or higher  
- Git  

### 🛠️ Installation & Running

1. **Clone the repository**

```bash
git clone https://github.com/PaolaFelix/OOP-Python-Compiler.git
cd OOP-Python-Compiler
```

2. **Install required dependency: [PLY](https://pypi.org/project/ply/)**

```bash
pip install ply
```

3. **Run the analyzer**

```bash
python main.py
```

> **Note:**  
> By default, the tool analyzes all `.py` files in the `tests` directory.  
> Sample Python test files are already included.  
> You can add your own code by placing `.py` files inside the `tests` folder — no extra configuration needed.

---

## Project Structure

| File / Folder     | Description |
|-------------------|-------------|
| **`main.py`**      | Entry point of the application. It loads test files, applies preprocessing, parsing, builds the AST, and performs OOP analysis. |
| **`preprocessor.py`** | Handles cleanup and formatting of the code (e.g., removing comments, excessive indentation). This helps ensure better parsing accuracy. |
| **`parser_module.py`** | Defines a custom lexer and parser using `ply`. It transforms input code into a parse tree using simplified grammar suited for OOP detection. |
| **`ast_builder.py`** | Translates the parse tree into a lightweight AST that represents the code’s structure in an analysis-friendly format. |
| **`analyzer.py`** | Implements the logic for traversing the AST and detecting OOP features like class and method usage, constructors, and instance tracking. It scores and classifies code as OOP or not. |
| **`tests/`** | Directory containing sample `.py` test files. These are automatically analyzed when running `main.py`. You can freely add or replace files here. |

---

## Output

### Example Summary

After execution, the tool prints a detailed report for each file and a final summary like:

```
========================================
FINAL SUMMARY
========================================
test1.py: REJECTED
test2.py: REJECTED
...
test10.py: REJECTED
```

### Meaning of Results

- **`REJECTED`**: The file does **not** implement enough OOP features to be classified as object-oriented code.
- Other outputs may include labels like `"CÓDIGO OOP"` or `"POSIBLEMENTE OOP"` for files that contain clear or partial OOP structures.
