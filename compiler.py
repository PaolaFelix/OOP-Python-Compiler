import ply.lex as lex
import ply.yacc as yacc
import ast
import os
import sys

# Tokens
tokens = [
    'ID',
    'NUM',
    'STR',
    'NEWLINE',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'EQ',
    'NE',
    'LT',
    'GT',
    'AND',
    'OR',
    'NOT',
    'LPAREN',
    'RPAREN',
    'COLON',
    'COMMA',
    'DOT',
    'CLASS',
    'DEF',
    'IMPORT',
    'FROM',
    'RETURN',
    'PASS',
    'IF',
    'ELSE',
    'WHILE',
    'EQ_OP'
]

# Reserved words
reserved = {
    'class': 'CLASS',
    'def': 'DEF',
    'import': 'IMPORT',
    'from': 'FROM',
    'return': 'RETURN',
    'pass': 'PASS',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT'
}

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQ = r'=='
t_NE = r'!='
t_LT = r'<'
t_GT = r'>'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON = r':'
t_COMMA = r','
t_DOT = r'\.'
t_EQ_OP = r'='

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUM(t):
    r'[0-9]+(\.[0-9]+)?'
    return t

def t_STR(t):
    r'\"([^"\\]|\\.)*\"|\'([^\'\\]|\\.)*\''
    return t

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += len(t.value)
    return t

# Ignore comments and indents
t_ignore = ' \t\r\f\v'
t_ignore_COMMENT = r'\#.*'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Yacc rules
def p_program(p):
    '''program : stmt
               | program stmt'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_stmt(p):
    '''stmt : CLASS ID LPAREN ID RPAREN COLON block
            | CLASS ID COLON block
            | DEF ID LPAREN params RPAREN COLON block
            | DEF ID LPAREN RPAREN COLON block
            | IMPORT import_path
            | FROM ID IMPORT ID
            | RETURN expr
            | RETURN
            | PASS
            | IF expr COLON block ELSE COLON block
            | IF expr COLON block
            | WHILE expr COLON block
            | target EQ_OP expr
            | expr'''
    pass

def p_block(p):
    '''block : NEWLINE program'''
    p[0] = p[2]

def p_params(p):
    '''params : ID
              | params COMMA ID'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_import_path(p):
    '''import_path : ID
                   | import_path DOT ID'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_expr(p):
    '''expr : term
            | expr PLUS term
            | expr MINUS term
            | expr TIMES term
            | expr DIVIDE term
            | expr EQ term
            | expr NE term
            | expr LT term
            | expr GT term
            | expr AND term
            | expr OR term'''
    pass

def p_term(p):
    '''term : ID
            | NUM
            | STR
            | LPAREN expr RPAREN
            | NOT term
            | MINUS term
            | ID call_chain'''
    pass

def p_call_chain(p):
    '''call_chain : DOT ID
                  | LPAREN args RPAREN
                  | call_chain DOT ID
                  | call_chain LPAREN args RPAREN'''
    pass

def p_args(p):
    '''args : expr
            | args COMMA expr'''
    pass

def p_target(p):
    '''target : ID
              | ID call_chain'''
    pass

def p_error(p):
    if p:
        raise SyntaxError(f"Syntax error at '{p.value}'")
    else:
        raise SyntaxError("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()

# Check if AST tree has OOP features
def has_oop(tree):
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            return True  # Tiene al menos una clase (aunque no tenga métodos)
    return False

# File processing
# File processing
def check_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = f.read()
        tree = ast.parse(data)

        if has_oop(tree):
            print(f"{file_path}: ACCEPTED")
        else:
            print(f"{file_path}: REJECTED (No OOP structure found)")

    except SyntaxError as e:
        print(f"{file_path}: REJECTED (Syntax Error: {e})")
    except Exception as e:
        print(f"{file_path}: REJECTED (Unexpected Error: {e})")


def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                check_file(file_path)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python .py <directory>")
        sys.exit(1)
    
    target_dir = sys.argv[1]
    if not os.path.isdir(target_dir):
        print(f"Error: '{target_dir}' is not a valid directory.")
        sys.exit(1)
    
    print(f"Checking Python files in: {target_dir}")
    process_directory(target_dir)