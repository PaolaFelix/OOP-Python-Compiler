import ply.lex as lex # Imports the PLY (Python Lex-Yacc) lexer module.

tokens = ( # Defines the list of all possible tokens (lexical units) recognized by the lexer.
    'CLASS', 'DEF', 'RETURN', 'PASS', 'SELF', # Keywords related to Python's object-oriented structure and control flow.
    'ID', 'INIT', 'NUMBER', 'STRING', # Identifiers, the special '__init__' method, numeric literals, and string literals.
    'EQUALS', 'PLUS', 'MINUS', 'MUL', 'DIV', # Operators for assignment and arithmetic operations.
    'COLON', 'LPAREN', 'RPAREN', 'DOT', 'COMMA', # Punctuation marks used in Python syntax.
    'INDENT', 'DEDENT', 'NEWLINE' # Special tokens to handle Python's indentation-based syntax.
)

reserved = { # A dictionary mapping reserved keywords to their corresponding token types.
    'class': 'CLASS',
    'def': 'DEF',
    'return': 'RETURN',
    'pass': 'PASS',
    'self': 'SELF',
}

t_EQUALS = r'=' # Regular expression for the equals sign.
t_PLUS   = r'\+' # Regular expression for the plus sign.
t_MINUS  = r'-' # Regular expression for the minus sign.
t_MUL    = r'\*' # Regular expression for the multiplication sign.
t_DIV    = r'/' # Regular expression for the division sign.
t_COLON  = r':' # Regular expression for the colon.
t_LPAREN = r'\(' # Regular expression for the left parenthesis.
t_RPAREN = r'\)' # Regular expression for the right parenthesis.
t_DOT    = r'\.' # Regular expression for the dot operator.
t_COMMA  = r',' # Regular expression for the comma.

t_ignore = ' \t' # Specifies characters to ignore (whitespace and tabs) during tokenization.

indent_stack = [0] # A stack to keep track of the current indentation levels; initialized with 0 for the base level.

def t_NEWLINE(t):
    r'\n[ \t]*' # Regular expression to match a newline character followed by any number of spaces or tabs.
    t.lexer.lineno += 1 # Increments the line number counter in the lexer.
    spaces = len(t.value) - 1 # Calculates the number of leading spaces/tabs after the newline.
    t.type = 'NEWLINE' # Sets the token type to NEWLINE.
    t.value = '\n' # Sets the token value to a single newline character.

    pending = [] # A list to store INDENT or DEDENT tokens that need to be emitted.

    if spaces > indent_stack[-1]: # Checks if the current indentation level is greater than the previous one.
        indent_stack.append(spaces) # Pushes the new indentation level onto the stack.
        pending.append(create_token('INDENT', t)) # Adds an INDENT token to the pending list.
    while spaces < indent_stack[-1]: # Checks if the current indentation level is less than the top of the stack.
        indent_stack.pop() # Removes the higher indentation level from the stack.
        pending.append(create_token('DEDENT', t)) # Adds a DEDENT token to the pending list.

    if pending: # If there are pending INDENT or DEDENT tokens.
        t.lexer.pending_tokens = pending # Stores the pending tokens on the lexer.
        return t # Returns the NEWLINE token immediately.
    return t # Returns the NEWLINE token if no INDENT/DEDENT tokens are pending.

def create_token(type_, t):
    """
    Helper function to create a new LexToken with specified type and inherited position.
    """
    tok = lex.LexToken() # Creates a new PLY LexToken object.
    tok.type = type_ # Sets the token type (e.g., 'INDENT', 'DEDENT').
    tok.value = None # Sets the token value to None (as INDENT/DEDENT don't have specific text values).
    tok.lineno = t.lineno # Inherits the line number from the original token.
    tok.lexpos = t.lexpos # Inherits the lexical position from the original token.
    return tok # Returns the newly created token.

def t_INIT(t):
    r'__init__' # Regular expression to match the special '__init__' method name.
    t.type = 'INIT' # Sets the token type to INIT.
    return t # Returns the INIT token.

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*' # Regular expression for identifiers (starts with letter/underscore, followed by letters/digits/underscores).
    # Checks if the matched text is a reserved keyword; if so, sets the token type to the keyword's type, otherwise 'ID'.
    t.type = reserved.get(t.value, 'ID')
    return t # Returns the ID or reserved keyword token.

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"' # Regular expression for double-quoted strings (handles escaped characters).
    return t # Returns the STRING token.

def t_NUMBER(t):
    r'\d+' # Regular expression for integer numbers (one or more digits).
    t.value = int(t.value) # Converts the matched string value to an integer.
    return t # Returns the NUMBER token.

def t_error(t):
    """
    Error handling rule: called when no other rule matches the input.
    """
    print(f"Illegal character '{t.value[0]}'") # Prints an error message for the illegal character.
    t.lexer.skip(1) # Skips the illegal character and continues tokenizing.

def token_wrapper(lexer):
    """
    A wrapper function for the lexer's token method to insert pending INDENT/DEDENT tokens.
    """
    if hasattr(lexer, 'pending_tokens') and lexer.pending_tokens: # Checks if there are pending tokens to emit.
        return lexer.pending_tokens.pop(0) # Returns and removes the first pending token.
    return lexer.original_token() # If no pending tokens, calls the original token method to get the next token.

lexer = lex.lex() # Builds the lexer from the defined rules.
lexer.original_token = lexer.token # Stores a reference to the original token method.
lexer.token = lambda: token_wrapper(lexer) # Overrides the lexer's token method with our wrapper.