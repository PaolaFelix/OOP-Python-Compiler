import ply.lex as lex

tokens = (
    'CLASS', 'DEF', 'RETURN', 'PASS', 'SELF',
    'ID', 'INIT', 'NUMBER', 'STRING',
    'EQUALS', 'PLUS', 'MINUS', 'MUL', 'DIV',
    'COLON', 'LPAREN', 'RPAREN', 'DOT', 'COMMA',
    'INDENT', 'DEDENT', 'NEWLINE'
)

reserved = {
    'class': 'CLASS',
    'def': 'DEF',
    'return': 'RETURN',
    'pass': 'PASS',
    'self': 'SELF',
}

t_EQUALS = r'='
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_MUL    = r'\*'
t_DIV    = r'/'
t_COLON  = r':'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_DOT    = r'\.'
t_COMMA  = r','

t_ignore = ' \t'

indent_stack = [0]

def t_NEWLINE(t):
    r'\n[ \t]*'
    t.lexer.lineno += 1
    spaces = len(t.value) - 1
    t.type = 'NEWLINE'
    t.value = '\n'

    pending = []

    if spaces > indent_stack[-1]:
        indent_stack.append(spaces)
        pending.append(create_token('INDENT', t))
    while spaces < indent_stack[-1]:
        indent_stack.pop()
        pending.append(create_token('DEDENT', t))

    if pending:
        t.lexer.pending_tokens = pending
        return t
    return t

def create_token(type_, t):
    tok = lex.LexToken()
    tok.type = type_
    tok.value = None
    tok.lineno = t.lineno
    tok.lexpos = t.lexpos
    return tok

def t_INIT(t):
    r'__init__'
    t.type = 'INIT'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

def token_wrapper(lexer):
    if hasattr(lexer, 'pending_tokens') and lexer.pending_tokens:
        return lexer.pending_tokens.pop(0)
    return lexer.original_token()

lexer = lex.lex()
lexer.original_token = lexer.token
lexer.token = lambda: token_wrapper(lexer)