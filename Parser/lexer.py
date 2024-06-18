import ply.lex as lex

# 定义Token
tokens = (
    'NUMBER', 'HEX_NUMBER', 'FLOAT', 'STRING', 'BOOLEAN',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET', 'LANGLE', 'RANGLE',
    'EQUALS', 'COMMA', 'DOT', 'QUESTION', 'COLON', 'AMPERSOR', 'AMPERSAND',
    'LT', 'GT', 'LE', 'GE', 'NE', 'TILDE',
    'EXPORT', 'IS', 'TEMPLATE', 'UNNAMED', 'NIL', 'PRIVATE', 'INT', 'TRUE', 'FALSE', 'DIV', 'MAP',
    'ID',
)

# 定义关键字
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

# Token正则表达形式
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
t_AMPERSOR = r'\|'
t_AMPERSAND = r'&'
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_NE = r'!='
t_TILDE = r'~'

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

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"|\'([^\\\n]|(\\.))*?\''
    t.value = t.value[1:-1]  # 移除引号
    return t

def t_BOOLEAN(t):
    r'\btrue\b|\bfalse\b'
    t.value = True if t.value.lower() == 'true' else False
    return t

def t_ID(t):
    r'[A-Za-z_][A-Za-z_0-9]*'
    t.type = keywords.get(t.value.lower(), 'ID')  # 先去除关键字，然后识别为ID
    return t


t_ignore = ' \t\n' # 忽略空格/换行/制表

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_COMMENT(t):
    r'//.*|/\*[\s\S]*?\*/|{[\s\S]*?}|[(\*)[\s\S]*?(\*)]' # 注释这里有点问题，{}实际并不是注释，主要用于描述GUID:{}
    pass


def t_error(t):
    print(f"Illegal character '{t.value[0]}'") # 错误处理，单纯跳过去
    t.lexer.skip(1)


# 构建和创建Lexer
lexer = lex.lex()
# 测试函数
def test_lexer():
    def tokenize_file(filename):
        with open(filename, 'r') as file:
            data = file.read()
        lexer.input(data)
        while True:
            tok = lexer.token()
            if not tok:
                break
            print(tok)
            
    tokenize_file('./Parser/test.ndf')

test_lexer()