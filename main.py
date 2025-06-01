import os
from preprocessor import preprocess_code
from parser import parser
from lexer import lexer
from oop_analyzer import OOPAnalyzer

def analyze_file(filename, test_path):
    """Analyzes a single file with minimal output"""
    print(f"Analyzing {filename}...")

    # Preprocessing
    preprocessed_code = preprocess_code(test_path)

    # Parsing
    result = parser.parse(''.join(preprocessed_code), lexer=lexer)
    if result is None:
        print(f"{filename}: Parsing failed.")
        return None

    # OOP analysis
    analyzer = OOPAnalyzer()
    oop_analysis = analyzer.analyze_ast(result)

    # Decide accepted or rejected based on classification
    classification = oop_analysis['classification']
    if classification == "CÓDIGO OOP":
        status = "ACCEPTED"
    else:
        status = "REJECTED"

    print(f"{filename}: {status}")
    return status

def main():
    tests_dir = 'tests'
    
    if not os.path.isdir(tests_dir):
        print(f"Folder '{tests_dir}' not found.")
        return
    
    python_files = [f for f in os.listdir(tests_dir) if f.endswith('.py')]
    if not python_files:
        print(f"No Python files found in '{tests_dir}'.")
        return
    
    print(f"Found {len(python_files)} files in '{tests_dir}'.\n")
    
    results = {}
    for filename in python_files:
        test_path = os.path.join(tests_dir, filename)
        status = analyze_file(filename, test_path)
        if status:
            results[filename] = status

    # Final summary - just file name and ACCEPTED/REJECTED
    print("\nFinal Summary:")
    for filename, status in results.items():
        print(f"{filename}: {status}")

if __name__ == '__main__':
    main()
