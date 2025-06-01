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
