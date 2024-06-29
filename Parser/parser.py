import ply.yacc as yacc
from lexer import tokens
import sys

# 本语法分析的主要工作是完成对数据的记录格式转换，准备以字典的形式记录NDF所描述Object的全部信息

# 运算优先级
precedence = (
    ('left', 'AMPERSAND', 'AMPERSOR'),
    ('left', 'EQUALS', 'LE', 'GE', 'LT', 'GT', 'NE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    ('right', 'UMINUS'),  # 单目减法运算符
)

# 抽象语法树节点
class ASTNode:
    def __init__(self, type, children=None, leaf=None, value=None):
        self.type = type
        self.children = children if children is not None else []
        self.leaf = leaf
        self.value = value

    def to_dict(self):
        pass

    def __repr__(self):
        return f"ASTNode( type={self.type}, leaf={self.leaf}, value={self.value}, children={self.children} )"

# 语法规则
## 程序基本结构
def p_program(p):
    '''program : statement_list'''
    p[0] = ASTNode(type='program', children=[p[1]], value = p[1].value)

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = ASTNode(type='statement_list', children=[p[1]] , value = [p[1].value])
    else:
        p[0] = ASTNode(type='statement_list', children=p[1].children + [p[2]], value = p[1].value + [p[2].value])
    
def p_statement(p):
    '''statement : normal_definition
                 | unnamed_definition
                 | template_definition'''
    p[0] = ASTNode(type = 'statement', children = [p[1]] , value = p[1].value)
    
## 定义语句
def p_normal_definition(p):
    '''normal_definition : var IS expression'''
    p[0] = ASTNode(type = 'normal_definition', children= [p[1], p[3]], leaf = p[2], value = {
        "statementType" : "normalDefinition",
        "key" : p[1].value,
        "value": p[3].value,
    })

def p_unnamed_definition(p):
    '''unnamed_definition : UNNAMED term_object'''
    p[0] = ASTNode(type = 'unnamed_definition', children= [p[2]] ,leaf = p[1], value = {
        "statementType" : "unnamedDefinition",
        "key" : None,
        "value": p[2].value,
    })

def p_template_definition(p):
    '''template_definition : TEMPLATE term_template IS term_object'''
    p[0] = ASTNode(type = 'template_definition',children = [p[2], p[4]] ,leaf = p[1], value = {
        "statementType" : "templateDefinition",
        "key" : p[2].value,
        "value": p[4].value,
    })

## 值与表达式
def p_expression(p):
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
                  | expression AMPERSOR expression
                  | MINUS expression %prec UMINUS
                  | term'''
    if len(p) == 2:
        p[0] = ASTNode(type = 'term', children = [p[1]], value=p[1].value)  # term
    elif len(p) == 3:
        p[0] = ASTNode(type = 'uminus', children = [p[2]], value=-p[2].value)  # uminus
    else:
        if p[2] == '+':
            value = p[1].value + p[3].value
        elif p[2] == '-':
            value = p[1].value - p[3].value
        elif p[2] == '*':
            value = p[1].value * p[3].value
        elif p[2] == '/':
            value = p[1].value / p[3].value
        elif p[2] == '%':
            value = p[1].value % p[3].value
        elif p[2] == '==':
            value = p[1].value == p[3].value
        elif p[2] == '<=':
            value = p[1].value <= p[3].value
        elif p[2] == '>=':
            value = p[1].value >= p[3].value
        elif p[2] == '<':
            value = p[1].value < p[3].value
        elif p[2] == '>':
            value = p[1].value > p[3].value
        elif p[2] == '!=':
            value = p[1].value != p[3].value
        elif p[2] == '&':
            value = p[1].value & p[3].value
        elif p[2] == '|':
            value = p[1].value | p[3].value
        p[0] = ASTNode(type ='binop', children= [p[1], p[3]], leaf = p[2], value=value)  # binop

def p_term(p):
    '''term : NUMBER
            | HEX_NUMBER
            | FLOAT
            | STR
            | BOOLEAN
            | term_vector
            | term_pair
            | term_map
            | term_path
            | term_object
            | term_template
            | var'''
    
    if isinstance(p[1], ASTNode):
        p[0] = ASTNode('term', leaf=p[1], value=p[1].value)
    else:
        p[0] = ASTNode('term', leaf=p[1], value=p[1])

def p_var(p):
    '''var : ID'''
    p[0] = ASTNode('var', leaf=p[1], value = p[1])

def p_term_vector(p):
    '''term_vector : LBRACKET RBRACKET
                   | LBRACKET term_vector_content RBRACKET'''
    if len(p) == 3:
        p[0] = ASTNode('vector', children = [], value=[])
    else:
        p[0] = ASTNode('vector', children = [p[2]], value=p[2].value)

def p_term_vector_content(p):
    '''term_vector_content : term COMMA
                           | term_vector_content term COMMA'''
    if len(p) == 2 or len(p) == 3:
        p[0] = ASTNode('vector_content', leaf = p[1], value=[p[1].value])
        # [p[1].value]
    else:
        p[0] = ASTNode('vector_content', leaf = p[1], value=p[1].value + [p[2].value])


def p_term_pair(p):
    '''term_pair : LPAREN term COMMA term RPAREN'''
    p[0] = ASTNode('pair', children = [p[2], p[4]], value=(p[2].value, p[4].value))

def p_term_map(p):
    '''term_map : MAP LBRACKET RBRACKET
                | MAP LBRACKET term_map_content RBRACKET'''
    if len(p) == 4:
        p[0] = ASTNode('map', children = [], value={})
    else:
        p[0] = ASTNode('map', children = p[3], value=p[3].value)

def p_term_map_content(p):
    '''term_map_content : term_pair COMMA
                        | term_map_content term_pair COMMA'''
    if len(p) == 3:
        p[0] = ASTNode('map_content', children = [p[1]], value=[p[1].value])
    else:
        p[0] = ASTNode('map_content', children = [p[1],p[2]], value=p[1].value + [p[2].value])

def p_type(p):
    '''type : ID
            | INT
            | STR'''
    p[0] = ASTNode(type = 'type', leaf=p[1] ,value = p[1])

def p_term_object(p):
    '''term_object : type LPAREN member_list RPAREN'''
    p[0] = ASTNode(type = "term_object",children=[p[1],p[3]], leaf=p[1], value= {
        "object_type" : p[1].value,
        "object_member_list" : p[3].value
    })

def p_member_list(p):
    '''member_list : member
                   | member_list member'''
    if len(p) == 2:
        p[0] = ASTNode(type = 'member_list',children = [p[1]], value = [p[1].value])
    else:
        p[0] = ASTNode(type = 'member_list', children = p[1].children + [p[2]], value = p[1].value + [p[2].value])

def p_member(p):
    '''member : var EQUALS expression
                | term_object
    '''
    if len(p) == 4:
        p[0] = ASTNode(type = 'member', children = [p[1], p[3]], leaf = p[2], value={
            "key": p[1].value,
            "value": p[3].value,
        })
    else:
        p[0] = ASTNode(type = 'member', children = [p[1], p[3]], leaf = p[2], value={
            "key": p[1].value["object_type"],
            "value": p[1].value,
        })

def p_term_template(p):
    '''term_template : template_name LBRACKET para_list RBRACKET'''
    p[0] = ASTNode(type = "term_object",children=[p[1],p[3]], leaf=p[1], value= {
        "template_name" : p[1].value,
        "template_para_list" : p[3].value
        })

def p_template_name(p):
    '''template_name : ID'''
    p[0] = ASTNode(type = 'template_name', children = [p[1]] , leaf=p[1], value = p[1])

def p_para_list(p):
    '''para_list : para
                 | para_list COMMA para'''
    if len(p) == 2:
        p[0] = ASTNode(type = 'para_list', children = [p[1]] , value = [p[1].value])
    else:
        p[0] = ASTNode(type = 'para_list', children = p[1].children + [p[3]], value = p[1].value + [p[2].value])

def p_para(p):
    '''para : var COLON type
            | var COLON type EQUALS expression'''
    if len(p) == 4:
        p[0] = ASTNode(type = 'para', children = [p[1], p[3]], value = {
        "key":p[1].value,
        "type":p[3].value,
    })
    else:
        p[0] = ASTNode(type = 'para', children = [p[1], p[3], p[5]] ,leaf = p[4], value = {
        "key":p[1].value,
        "type":p[3].value,
        "value":p[5].value,
    })

def p_term_path(p):
    '''term_path : ID path_part
                 | DOLLAR path_part
                 | TILDE path_part'''
    p[0] = ASTNode('term_path', children=[p[2]], leaf=p[1], value=p[1] + p[2].value)

def p_path_part(p):
    '''path_part : SLASH ID path_part
            | SLASH ID
            | SLASH'''
    if len(p) == 4:
        p[0] = ASTNode('path_part', children=[p[2], p[3]], leaf=p[1], value='/' + p[2] + p[3].value)
    elif len(p) == 3:
        p[0] = ASTNode('path_part', children=[p[2]], leaf=p[1], value='/' + p[2])
    else :
        p[0] = ASTNode('path_part', children=[], value= '/')
    # 为了与var 区分 姑且要求至少有一个路径分隔符

## 错误处理
def p_error(p):
    print(f"Syntax error at {p.value!r}")

# 构建解析器
parser = yacc.yacc(debug=True)

# 打印器
def printDict(d, indent=0):
    indent_str = '  ' * indent
    if isinstance(d, dict):
        print(indent_str + '{')
        for key, value in d.items():
            print(f'{indent_str}  "{key}": ', end='')
            if isinstance(value, (dict, list)):
                print()
                printDict(value, indent + 1)
            else:
                print(f'"{value}",')
        print(indent_str + '},')
    elif isinstance(d, list):
        print(indent_str + '[')
        for item in d:
            if isinstance(item, (dict, list)):
                printDict(item, indent + 1)
            else:
                print(f'{indent_str}  "{item}",')
        print(indent_str + '],')
    else:
        print(indent_str + f'"{d}"')

# 测试函数
def test_parser():
    def parse_file(filename):
        with open(filename, 'r') as file:
            data = file.read()
        result = parser.parse(data)
        print("ParserResult:")
        # print(result.value)
        print(printDict(result.value))

    parse_file('./Parser/test.ndf')

test_parser()
