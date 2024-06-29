import ply.yacc as yacc
from lexer import tokens  # 假设你的词法分析器保存在 lex_example.py 中

# 定义语法规则
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MODULO expression
                  | expression EQUALS expression
                  | expression LE expression
                  | expression GE expression
                  | expression LT expression
                  | expression GT expression
                  | expression NE expression
                  | expression AMPERSAND expression
                  | expression AMPERSOR expression'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_term(p):
    '''expression : term'''
    p[0] = p[1]

def p_term_number(p):
    '''term : NUMBER'''
    p[0] = ('number', p[1])

def p_term_hex_number(p):
    '''term : HEX_NUMBER'''
    p[0] = ('hex_number', p[1])

def p_term_float(p):
    '''term : FLOAT'''
    p[0] = ('float', p[1])

def p_term_str(p):
    '''term : STR'''
    p[0] = ('string', p[1])

def p_term_boolean(p):
    '''term : BOOLEAN'''
    p[0] = ('boolean', p[1])

def p_term_var(p):
    '''term : var'''
    p[0] = p[1]

def p_var(p):
    '''var : ID'''
    p[0] = ('var', p[1])

def p_term_vector(p):
    '''term : term_vector'''
    p[0] = p[1]

def p_term_vector_empty(p):
    '''term_vector : LBRACKET RBRACKET'''
    p[0] = ('vector', [])

def p_term_vector_content(p):
    '''term_vector : LBRACKET term_vector_content RBRACKET'''
    p[0] = ('vector', p[2])

def p_term_vector_content_items(p):
    '''term_vector_content : term
                           | term_vector_content COMMA term'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_term_pair(p):
    '''term : term_pair'''
    p[0] = p[1]

def p_term_pair_items(p):
    '''term_pair : LPAREN term COMMA term RPAREN'''
    p[0] = ('pair', p[2], p[4])

def p_term_map(p):
    '''term : term_map'''
    p[0] = p[1]

def p_term_map_empty(p):
    '''term_map : MAP LBRACKET RBRACKET'''
    p[0] = ('map', [])

def p_term_map_content(p):
    '''term_map : MAP LBRACKET term_map_content RBRACKET'''
    p[0] = ('map', p[3])

def p_term_map_content_items(p):
    '''term_map_content : term_map_content COMMA term_pair'''
    p[0] = p[1] + [p[3]]

def p_program(p):
    '''program : statement_list'''
    p[0] = ('program', p[1])

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : object_assignment
                 | object_definition
                 | unnamed_object_definition
                 | template_definition'''
    p[0] = p[1]

def p_object_assignment(p):
    '''object_assignment : var IS expression'''
    p[0] = ('assign', p[1], p[3])

def p_type(p):
    '''type : ID
            | INT
            | STR'''
    p[0] = ('type', p[1])

def p_object_definition(p):
    '''object_definition : var IS type LPAREN member_list RPAREN'''
    p[0] = ('object_definition', p[1], p[3], p[5])

def p_unnamed_object_definition(p):
    '''unnamed_object_definition : UNNAMED type LPAREN member_list RPAREN'''
    p[0] = ('unnamed_object_definition', p[2], p[4])

def p_member_list(p):
    '''member_list : member
                   | member_list member'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_member(p):
    '''member : var EQUALS expression
              | object_definition'''
    p[0] = p[1]

def p_template_definition(p):
    '''template_definition : TEMPLATE template_name LBRACKET para_list RBRACKET IS type LPAREN member_list RPAREN'''
    p[0] = ('template_definition', p[2], p[4], p[7], p[9])

def p_template_name(p):
    '''template_name : ID'''
    p[0] = ('template_name', p[1])

def p_para_list(p):
    '''para_list : para
                 | para_list COMMA para'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_para(p):
    '''para : var COLON type
            | var COLON type EQUALS expression'''
    if len(p) == 4:
        p[0] = ('parameter', p[1], p[3])
    else:
        p[0] = ('parameter', p[1], p[3], p[5])

def p_error(p):
    print(f"Syntax error at '{p.value}'")

# 构建解析器
parser = yacc.yacc()

# 测试函数
def test_parser():
    data = '''
    Gravity is -9.81
    Currencies is MAP[
      ('EUR', '€'),
      ('USD', '$'),
      ('GBP', '£')
    ]
    '''
    result = parser.parse(data)
    print(result)

test_parser()
