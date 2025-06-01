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

## Core Components Explained

### 1. `preprocessor.py`

This module is responsible for the **initial cleaning and normalization** of the source code. It prepares the code for lexical analysis by:

- **Removing Comments**: Eliminates single-line (`#`) and multi-line (`"""Docstrings"""` or `'''Docstrings'''`) comments.
- **Handling Empty Lines**: Removes blank lines to streamline the input for the lexer.

** Why a Preprocessor?**

A preprocessor simplifies the job of the lexer and parser. By removing non-essential elements like comments and empty lines upfront, it reduces the complexity of the grammar rules needed later. This ensures that only meaningful code constructs are passed on to the next stages, improving **efficiency** and **robustness**.

---

### 2. `lexer.py`

The **lexer (tokenizer)** takes the cleaned code and breaks it into a stream of tokens. Each token represents a basic building block such as:

- **Keywords** (`class`, `def`, etc.)
- **Identifiers** (`my_variable`, etc.)
- **Operators** (`=`, `+`, etc.)
- **Punctuation** (`:`, `()`, etc.)
- **Indentation Handling**: Emits `INDENT` and `DEDENT` tokens for Python's indentation-based syntax.

---

### 3. `parser.py`

The **parser** takes the token stream from the lexer and constructs an **Abstract Syntax Tree (AST)**.

The AST is a hierarchical tree structure that represents the **logic and relationships** in the code, without being tied to surface-level syntax like spacing or punctuation.

** Why an Abstract Syntax Tree (AST)?**

- **Identifies Structure**: Detects class definitions, method definitions, and constructor calls.
- **Analyzes Relationships**: Determines method-class associations, attribute usage (`self.attr`, `obj.attr`), and instance creation.
- **Enables Semantic Checks**: Verifies OOP usage, like the presence of `__init__` methods or proper use of `self`.

Without an AST, deeper analysis would require fragile pattern matching on raw text — error-prone and hard to scale.

---

### 4. `oop_analyzer.py`

The core intelligence of the tool resides here. The `OOPAnalyzer` class **traverses the AST** and performs detailed OOP analysis:

- **Detects OOP Features**: Finds classes, methods, constructors, and instance usage.
- **Tracks Metrics**: Counts OOP structures found in the code.
- **Generates Observations**: Notes findings like `"Class defined: MyClass"` or `"Constructor found: __init__"`.
- **Classifies Code**: Applies internal rules to classify the code as either:
  - `ACCEPTED` – contains sufficient OOP elements.
  - `REJECTED` – lacks necessary OOP structure.

---

### 5. `main.py`

The **entry point** of the application. This file orchestrates the full workflow:

1. **Receives target directory** (default: `'tests'`) containing `.py` files.
2. **Processes each file**:
   - Runs it through the `preprocessor`, `lexer`, and `parser`.
   - Passes the AST to the `OOPAnalyzer`.
3. **Outputs results**:
   - Prints detailed file-level OOP analysis.
   - Shows a **final summary** marking each file as `ACCEPTED` or `REJECTED`.

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

- **`ACCEPTED`**: The file demonstrates object-oriented programming features such as class definitions, constructors (`__init__`), methods, and instance usage.
- **`REJECTED`**: The file does **not** implement sufficient OOP features to be classified as object-oriented.
