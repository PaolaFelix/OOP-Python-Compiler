import ply.yacc as yacc # Imports the PLY (Python Lex-Yacc) yacc module for creating parsers.
from lexer import tokens # Imports the 'tokens' list from the lexer module, which defines all valid tokens.

# --- Operator Precedence ---
# Defines the precedence and associativity of operators to resolve ambiguities in the grammar.
# Operations listed later have higher precedence (e.g., MUL/DIV before PLUS/MINUS).
precedence = (
    ('left', 'PLUS', 'MINUS'), # Addition and subtraction have left associativity.
    ('left', 'MUL', 'DIV'),    # Multiplication and division have left associativity and higher precedence.
)

# --- Grammar Rules ---

# Top-level rule: A program consists of a list of statements.
def p_program(p):
    'program : stmt_list'
    p[0] = ('program', p[1]) # The AST node for a program is a tuple: ('program', [list of statements]).

# Rule for a list of statements: multiple statements.
def p_stmt_list_multiple(p):
    'stmt_list : stmt stmt_list'
    p[0] = [p[1]] + p[2] # Concatenates the current statement with the rest of the statement list.

# Rule for a list of statements: a single statement.
def p_stmt_list_single(p):
    'stmt_list : stmt'
    p[0] = [p[1]] # A list containing just the single statement.

# Statement rule: Class definition.
# Matches: CLASS ID COLON NEWLINE indented_block
def p_stmt_class(p):
    'stmt : CLASS ID COLON NEWLINE block'
    p[0] = ('class_def', p[2], p[5]) # ('class_def', class_name, class_body_block).

# Statement rule: Method definition within a class.
# Matches: DEF method_name LPAREN param_list RPAREN COLON NEWLINE indented_block
def p_stmt_method(p):
    'stmt : DEF method_name LPAREN param_list RPAREN COLON NEWLINE block'
    p[0] = ('method_def', p[2], p[4], p[8]) # ('method_def', method_name, parameters, method_body_block).

# Statement rule: Simple variable assignment (e.g., x = 5).
# Matches: ID EQUALS expr NEWLINE
def p_stmt_assignment_simple(p):
    'stmt : ID EQUALS expr NEWLINE'
    p[0] = ('assignment', p[1], p[3]) # ('assignment', variable_name, expression_value).

# Statement rule: Attribute assignment on an object (e.g., obj.attr = value).
# Matches: ID DOT ID EQUALS expr NEWLINE
def p_stmt_assignment_attr(p):
    'stmt : ID DOT ID EQUALS expr NEWLINE'
    p[0] = ('attr_assignment', p[1], p[3], p[5]) # ('attr_assignment', object_name, attribute_name, expression_value).

# Statement rule: Self-attribute assignment within a method (e.g., self.attr = value).
# Matches: SELF DOT ID EQUALS expr NEWLINE
def p_stmt_self_assignment(p):
    'stmt : SELF DOT ID EQUALS expr NEWLINE'
    p[0] = ('self_assignment', p[3], p[5]) # ('self_assignment', attribute_name, expression_value).

# Statement rule: Method call on an object (e.g., obj.method(args)).
# Matches: ID DOT ID LPAREN arg_list RPAREN NEWLINE
def p_stmt_method_call(p):
    'stmt : ID DOT ID LPAREN arg_list RPAREN NEWLINE'
    p[0] = ('method_call', p[1], p[3], p[5]) # ('method_call', object_name, method_name, arguments).

# Statement rule: Standalone function call (e.g., func(args)).
# Matches: ID LPAREN arg_list RPAREN NEWLINE
def p_stmt_function_call(p):
    'stmt : ID LPAREN arg_list RPAREN NEWLINE'
    p[0] = ('function_call', p[1], p[3]) # ('function_call', function_name, arguments).

# Statement rule: Return statement with an expression (e.g., return x + 1).
# Matches: RETURN expr NEWLINE
def p_stmt_return_expr(p):
    'stmt : RETURN expr NEWLINE'
    p[0] = ('return', p[2]) # ('return', expression_to_return).

# Statement rule: Return statement without an expression (e.g., return).
# Matches: RETURN NEWLINE
def p_stmt_return_only(p):
    'stmt : RETURN NEWLINE'
    p[0] = ('return', None) # ('return', None).

# Statement rule: Pass statement.
# Matches: PASS NEWLINE
def p_stmt_pass(p):
    'stmt : PASS NEWLINE'
    p[0] = ('pass',) # ('pass',).

# Rule for method name: A standard identifier.
def p_method_name_id(p):
    'method_name : ID'
    p[0] = p[1] # The method name is simply the identifier's value.

# Rule for method name: The special '__init__' keyword.
def p_method_name_init(p):
    'method_name : INIT'
    p[0] = p[1] # The method name is '__init__'.

# Rule for parameter list: An empty list.
def p_param_list_empty(p):
    'param_list : '
    p[0] = [] # Represents an empty list of parameters.

# Rule for parameter list: Just 'self'.
def p_param_list_self(p):
    'param_list : SELF'
    p[0] = ['self'] # A list containing only the 'self' parameter.

# Rule for parameter list: 'self' followed by other parameters.
def p_param_list_self_params(p):
    'param_list : SELF COMMA params'
    p[0] = ['self'] + p[3] # Combines 'self' with the rest of the parameters.

# Rule for parameter list: Just other parameters (no 'self').
def p_param_list_params(p):
    'param_list : params'
    p[0] = p[1] # The parameter list is just the 'params' production.

# Rule for parameters: Multiple parameters separated by commas.
def p_params_list(p):
    'params : ID COMMA params'
    p[0] = [p[1]] + p[3] # Combines the current ID with the rest of the parameters.

# Rule for parameters: A single parameter.
def p_params_single(p):
    'params : ID'
    p[0] = [p[1]] # A list containing just the single ID.

# Rule for expression: Binary operations (e.g., 2 + 3, x * y).
# Applies precedence rules defined earlier.
def p_expr_binary(p):
    'expr : expr binary_op expr'
    p[0] = ('binary_expr', p[2], p[1], p[3]) # ('binary_expr', operator, left_operand, right_operand).

# Rule for expression: An expression can also be a simple term.
def p_expr_term(p):
    'expr : term'
    p[0] = p[1] # The expression is simply the value of the term.

# Term rule: Constructor call (e.g., MyClass()). This specifically captures class instantiation.
# Note: It matches the same pattern as a function call at the lexical level, but context implies constructor.
def p_term_constructor_call(p):
    'term : ID LPAREN arg_list RPAREN'
    p[0] = ('constructor_call', p[1], p[3]) # ('constructor_call', class_name, arguments).

# Expression rule: Function call (e.g., func(args)).
# This rule is used for function calls when they appear as part of an expression (e.g., result = func()).
def p_expr_function_call(p):
    'expr : ID LPAREN arg_list RPAREN'
    p[0] = ('function_call', p[1], p[3]) # ('function_call', function_name, arguments).

# Term rule: Self-attribute access (e.g., self.x).
def p_term_self_attr(p):
    'term : SELF DOT ID'
    p[0] = ('self_attr', p[3]) # ('self_attr', attribute_name).

# Term rule: Attribute access on an object (e.g., obj.x).
def p_term_attr_access(p):
    'term : ID DOT ID'
    p[0] = ('attr_access', p[1], p[3]) # ('attr_access', object_name, attribute_name).

# Term rule: An identifier (e.g., a variable name).
def p_term_id(p):
    'term : ID'
    p[0] = ('id', p[1]) # ('id', variable_name).
    
# Term rule: A number literal.
def p_term_number(p):
    'term : NUMBER'
    p[0] = ('number', p[1]) # ('number', numeric_value).

# Term rule: A string literal.
def p_term_string(p):
    'term : STRING'
    p[0] = ('string', p[1]) # ('string', string_value).

# Term rule: Parenthesized expression (for overriding precedence).
def p_term_paren(p):
    'term : LPAREN expr RPAREN'
    p[0] = p[2] # The value is the expression inside the parentheses.

# Rule for binary operators: Defines the actual tokens that represent binary operations.
def p_binary_op(p):
    '''binary_op : PLUS
                 | MINUS
                 | MUL
                 | DIV'''
    p[0] = p[1] # The operator is simply its token value.

# Rule for argument list: An empty list.
def p_arg_list_empty(p):
    'arg_list : '
    p[0] = [] # Represents an empty list of arguments.

# Rule for argument list: Multiple arguments separated by commas.
def p_arg_list_multi(p):
    'arg_list : expr COMMA arg_list'
    p[0] = [p[1]] + p[3] # Combines the current expression with the rest of the arguments.

# Rule for argument list: A single argument.
def p_arg_list_single(p):
    'arg_list : expr'
    p[0] = [p[1]] # A list containing just the single expression.

# Rule for a block of indented code.
# Matches: INDENT stmt_list DEDENT
def p_block(p):
    'block : INDENT stmt_list DEDENT'
    p[0] = p[2] # The block's content is the list of statements within it.

# Error handling rule: Called when the parser encounters a syntax error.
def p_error(p):
    if p: # If an error token is available.
        print(f"Syntax error at token {p.type} ('{p.value}'), line {p.lineno}") # Print detailed error info.
    else: # If the error is at the end of the input (unexpected EOF).
        print("Syntax error at EOF") # Indicate syntax error at end of file.

parser = yacc.yacc() # Build the parser from the grammar rules.