import ply.lex as lex

# Define tokens
tokens = (
    'NUMBER', 'HEX_NUMBER', 'FLOAT', 'STRING', 'BOOLEAN',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET', 'LANGLE', 'RANGLE',
    'EQUALS', 'COMMA', 'DOT', 'QUESTION', 'COLON', 'PIPE', 'AMPERSAND',
    'LT', 'GT', 'LE', 'GE', 'NE',
    'EXPORT', 'IS', 'TEMPLATE', 'UNNAMED', 'NIL', 'PRIVATE', 'INT', 'TRUE', 'FALSE', 'DIV', 'MAP',
    'ID',  # Ensure 'ID' is included in the tokens
)

# Define keywords
keywords = {
    'export': 'EXPORT',
    'is': 'IS',
    'template': 'TEMPLATE',
    'unnamed': 'UNNAMED',
    'nil': 'NIL',
    'private': 'PRIVATE',
    'int': 'INT',
    'true': 'TRUE',
    'false': 'FALSE',
    'div': 'DIV',
    'map': 'MAP',
}

# Define token regex patterns
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LANGLE = r'<'
t_RANGLE = r'>'
t_EQUALS = r'='
t_COMMA = r','
t_DOT = r'\.'
t_QUESTION = r'\?'
t_COLON = r':'
t_PIPE = r'\|'
t_AMPERSAND = r'&'
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_NE = r'!='

# Define a rule to handle numbers (both integers and hexadecimal)
def t_HEX_NUMBER(t):
    r'0x[0-9A-Fa-f]+'
    t.value = int(t.value, 16)
    return t

def t_FLOAT(t):
    r'-?\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

# Define a rule to handle strings (both single and double quoted)
def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"|\'([^\\\n]|(\\.))*?\''
    t.value = t.value[1:-1]  # Remove quotes
    return t

# Define a rule to handle boolean values
def t_BOOLEAN(t):
    r'\btrue\b|\bfalse\b'
    t.value = True if t.value.lower() == 'true' else False
    return t

# Define a rule to handle identifiers and keywords
def t_ID(t):
    r'[A-Za-z_][A-Za-z_0-9]*'
    t.type = keywords.get(t.value.lower(), 'ID')  # Check for reserved words
    return t

# Ignore whitespace and newline characters
t_ignore = ' \t\n'

# Define a rule to handle newlines and update line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Define a rule to handle comments (both single-line and multi-line)
def t_COMMENT(t):
    r'//.*|/\*[\s\S]*?\*/|{[\s\S]*?}|[(\*)[\s\S]*?(\*)]'
    pass

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Function to read data from file and tokenize
def tokenize_file(filename):
    with open(filename, 'r') as file:
        data = file.read()
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

# Test the lexer with the content of test.ndf
tokenize_file('test.ndf')
