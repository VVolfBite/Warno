import ply.yacc as yacc
from lexer import tokens

# 预定义的优先级
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
)

# 定义一个抽象语法树节点
class ASTNode:
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        self.children = children if children is not None else []
        self.leaf = leaf

# 解析规则
def p_program(p):
    '''program : statement_list'''
    p[0] = ASTNode('program', [p[1]])

def p_statement_list_single(p):
    '''statement_list : statement'''
    p[0] = ASTNode('statement_list', [p[1]])

def p_statement_list_multiple(p):
    '''statement_list : statement_list statement'''
    p[0] = ASTNode('statement_list', p[1].children + [p[2]])

def p_statement_assignment(p):
    '''statement : assignment'''
    p[0] = ASTNode('statement', [p[1]])

def p_statement_object_definition(p):
    '''statement : object_definition'''
    p[0] = ASTNode('statement', [p[1]])

def p_statement_template_definition(p):
    '''statement : template_definition'''
    p[0] = ASTNode('statement', [p[1]])

def p_assignment(p):
    '''assignment : ID IS expression'''
    p[0] = ASTNode('assignment', [p[1], p[3]])

def p_object_definition_named(p):
    '''object_definition : ID IS ID LPAREN member_list RPAREN'''
    p[0] = ASTNode('object_definition', [p[1], p[3], p[5]])

def p_object_definition_unnamed(p):
    '''object_definition : UNNAMED ID LPAREN member_list RPAREN'''
    p[0] = ASTNode('object_definition', [p[2], p[4]])

def p_template_definition(p):
    '''template_definition : TEMPLATE ID LPAREN member_list RPAREN IS ID'''
    p[0] = ASTNode('template_definition', [p[2], p[4], p[7]])

def p_member_list_single(p):
    '''member_list : member'''
    p[0] = ASTNode('member_list', [p[1]])

def p_member_list_multiple(p):
    '''member_list : member_list member'''
    p[0] = ASTNode('member_list', p[1].children + [p[2]])

def p_member(p):
    '''member : ID EQUALS expression'''
    p[0] = ASTNode('member', [p[1], p[3]])

def p_expression_term(p):
    '''expression : term'''
    p[0] = ASTNode('expression', [p[1]])

def p_expression_binary_operation(p):
    '''expression : expression PLUS term
                  | expression MINUS term
                  | expression TIMES term
                  | expression DIVIDE term
                  | expression MODULO term'''
    p[0] = ASTNode('expression', [p[1], p[2], p[3]])

def p_term_single(p):
    '''term : NUMBER
            | HEX_NUMBER
            | FLOAT
            | STRING
            | BOOLEAN
            | ID'''
    p[0] = ASTNode('term', leaf=p[1])

def p_term_expression(p):
    '''term : LPAREN expression RPAREN'''
    p[0] = ASTNode('term', [p[2]])

def p_term_vector(p):
    '''term : LBRACKET vector_content RBRACKET'''
    p[0] = ASTNode('vector', [p[2]])

def p_vector_content_single(p):
    '''vector_content : term'''
    p[0] = ASTNode('vector_content', [p[1]])

def p_vector_content_multiple(p):
    '''vector_content : vector_content COMMA term'''
    p[0] = ASTNode('vector_content', p[1].children + [p[3]])

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

# 构建解析器
parser = yacc.yacc()

# 测试解析器
def test_parser():
    def parse_file(filename):
        with open(filename, 'r') as file:
            data = file.read()
        result = parser.parse(data)
        print(result)

    parse_file('./Parser/test.ndf')

test_parser()
