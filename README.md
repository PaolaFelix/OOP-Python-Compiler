OOP Code Analyzer
description: >
  A lightweight Python tool that detects whether a given piece of code follows object-oriented programming (OOP) principles.
  It uses a custom preprocessor and an abstract syntax tree (AST) to evaluate the structural components of OOP, such as classes, methods, constructors, attributes, and instance usage.

Getting_started:
  prerequisites:
    - Python 3.7 or higher installed on your system
    - Git installed for cloning the repository

  installation_and_running:
    steps:
      - step: "Clone the repository"
        command: |
          git clone https://github.com/PaolaFelix/OOP-Python-Compiler.git
          cd /OOP-Python-Compiler

      - step: "Install required dependency: ply"
        command: |
          pip install ply

      - step: "Run the analyzer"
        command: |
          python main.py
        note: >
          By default, the tool analyzes all `.py` files in the 'tests' directory.
          Sample Python test files are already included for demonstration.
          To analyze your own code, simply add more `.py` files to the 'tests' directory.


Project_structure:
  - main.py: >
      Entry point of the application. It loads test files from the 'tests' folder, runs preprocessing, parsing, AST construction,
      and finally OOP analysis on each file.
  
  - preprocessor.py: >
      Responsible for basic cleanup and formatting of the input code before tokenization. This step improves the parser's accuracy
      by removing comments, extra indentation, or unsupported syntax.

  - parser_module.py: >
      Defines the lexer and parser using the `ply` library. It tokenizes Python-like syntax and builds a parse tree from the input.
      This custom parser allows us to work with a simplified grammar suited to OOP structure detection.

  - ast_builder.py: >
      Converts the parse tree into a lightweight Abstract Syntax Tree (AST) tailored for OOP analysis.
      The AST represents code structure (classes, methods, attribute access, etc.) in a way that's easier to analyze.

  - analyzer.py: >
      The core logic that traverses the AST and detects OOP features like class definitions, constructors (`__init__`),
      method usage, instance creation, and attribute access. It assigns an OOP score and classifies the code accordingly
      (e.g., 'CÓDIGO OOP', 'POSIBLEMENTE OOP', etc.).

  - tests/: >
      Contains sample `.py` files that serve as input to the analyzer. These can be edited or replaced with your own test files.
      All files in this folder are automatically analyzed when you run `python main.py`.

Output:
  summary: >
    After execution, the tool prints a detailed analysis for each file and a final summary like the following:

    ========================================
    FINAL SUMMARY
    ========================================
    test1.py: REJECTED
    test2.py: REJECTED
    ...
    test10.py: REJECTED

  meaning: >
    The result "REJECTED" means that the code does not sufficiently implement OOP patterns according to the detection rules.
    If a file meets key OOP features, it will be marked with different levels of confidence (e.g., "CÓDIGO OOP").




