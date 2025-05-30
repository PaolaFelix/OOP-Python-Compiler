import ply.yacc as yacc
from lexer import tokens

# Precedencia para resolver conflictos
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV'),
)

def p_program(p):
    'program : stmt_list'
    p[0] = ('program', p[1])

def p_stmt_list_multiple(p):
    'stmt_list : stmt stmt_list'
    p[0] = [p[1]] + p[2]

def p_stmt_list_single(p):
    'stmt_list : stmt'
    p[0] = [p[1]]

def p_stmt_class(p):
    'stmt : CLASS ID COLON NEWLINE block'
    p[0] = ('class_def', p[2], p[5])

def p_stmt_method(p):
    'stmt : DEF method_name LPAREN param_list RPAREN COLON NEWLINE block'
    p[0] = ('method_def', p[2], p[4], p[8])

def p_stmt_assignment_simple(p):
    'stmt : ID EQUALS expr NEWLINE'
    p[0] = ('assignment', p[1], p[3])

def p_stmt_assignment_attr(p):
    'stmt : ID DOT ID EQUALS expr NEWLINE'
    p[0] = ('attr_assignment', p[1], p[3], p[5])

def p_stmt_self_assignment(p):
    'stmt : SELF DOT ID EQUALS expr NEWLINE'
    p[0] = ('self_assignment', p[3], p[5])

def p_stmt_method_call(p):
    'stmt : ID DOT ID LPAREN arg_list RPAREN NEWLINE'
    p[0] = ('method_call', p[1], p[3], p[5])

def p_stmt_function_call(p):
    'stmt : ID LPAREN arg_list RPAREN NEWLINE'
    p[0] = ('function_call', p[1], p[3])

def p_stmt_return_expr(p):
    'stmt : RETURN expr NEWLINE'
    p[0] = ('return', p[2])

def p_stmt_return_only(p):
    'stmt : RETURN NEWLINE'
    p[0] = ('return', None)

def p_stmt_pass(p):
    'stmt : PASS NEWLINE'
    p[0] = ('pass',)

def p_method_name_id(p):
    'method_name : ID'
    p[0] = p[1]

def p_method_name_init(p):
    'method_name : INIT'
    p[0] = p[1]

def p_param_list_empty(p):
    'param_list : '
    p[0] = []

def p_param_list_self(p):
    'param_list : SELF'
    p[0] = ['self']

def p_param_list_self_params(p):
    'param_list : SELF COMMA params'
    p[0] = ['self'] + p[3]

def p_param_list_params(p):
    'param_list : params'
    p[0] = p[1]

def p_params_list(p):
    'params : ID COMMA params'
    p[0] = [p[1]] + p[3]

def p_params_single(p):
    'params : ID'
    p[0] = [p[1]]

def p_expr_binary(p):
    'expr : expr binary_op expr'
    p[0] = ('binary_expr', p[2], p[1], p[3])

def p_expr_term(p):
    'expr : term'
    p[0] = p[1]

def p_term_constructor_call(p):
    'term : ID LPAREN arg_list RPAREN'
    p[0] = ('constructor_call', p[1], p[3])

def p_expr_function_call(p):
    'expr : ID LPAREN arg_list RPAREN'
    p[0] = ('function_call', p[1], p[3])

def p_term_self_attr(p):
    'term : SELF DOT ID'
    p[0] = ('self_attr', p[3])

def p_term_attr_access(p):
    'term : ID DOT ID'
    p[0] = ('attr_access', p[1], p[3])

def p_term_id(p):
    'term : ID'
    p[0] = ('id', p[1])
    
def p_term_number(p):
    'term : NUMBER'
    p[0] = ('number', p[1])

def p_term_string(p):
    'term : STRING'
    p[0] = ('string', p[1])

def p_term_paren(p):
    'term : LPAREN expr RPAREN'
    p[0] = p[2]

def p_binary_op(p):
    '''binary_op : PLUS
                 | MINUS
                 | MUL
                 | DIV'''
    p[0] = p[1]

def p_arg_list_empty(p):
    'arg_list : '
    p[0] = []

def p_arg_list_multi(p):
    'arg_list : expr COMMA arg_list'
    p[0] = [p[1]] + p[3]

def p_arg_list_single(p):
    'arg_list : expr'
    p[0] = [p[1]]

def p_block(p):
    'block : INDENT stmt_list DEDENT'
    p[0] = p[2]

def p_error(p):
    if p:
        print(f"Syntax error at token {p.type} ('{p.value}'), line {p.lineno}")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()