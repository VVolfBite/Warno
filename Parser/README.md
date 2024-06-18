词法分析Token:
## Build-In-Types
Token:
关键字部分：
{
    'export': 'EXPORT','is': 'IS','template': 'TEMPLATE','unnamed': 'UNNAMED','nil': 'NIL',
    'private': 'PRIVATE','int': 'INT', 'string':'STRING' ,'true': 'TRUE','false': 'FALSE','div': 'DIV','map': 'MAP'
}
基本类型部分：
{
    'integer':'NUMBER','HEX_NUMBER', 'floating point':'FLOAT', 'character string':'STR', 'boolean':'BOOLEAN'
}    
运算符号部分:
{
   '=':'EQUALS', '+':'PLUS', '-':'MINUS', '*':'TIMES', 'div':'DIVIDE', '%':'MODULO'
}
布尔符号部分:
{
     '<':'LT', '>':'GT', '<=':'LE', '>=':'GE', '!=':'NE',
    '&':'AMPERSAND', '|':'AMPERSOR'
}
块号部分：
{
    '(':'LPAREN', ')':'RPAREN', '{':'LBRACE', '}':'RBRACE', '[':'LBRACKET', ']':'RBRACKET', '<':'LANGLE', '>':'RANGLE',
}
其他符号部分：
{
    ',':'COMMA', '.':'DOT', ':':'COLON', '~':'TILDE' ,'/':'SLASH', '?':'QUESTION'
}

语法分析推导式：
## Build-In-Types
expression : term
    | expression PLUS expression
    | expression MINUS expression
    | expression TIMES expression
    | expression DIVIDE expression
    | expression MODULO expression
    | LPAREN experssion RPAREN

term : NUMBER
    | HEX_NUMBER
    | FLOAT
    | STR
    | BOOLEAN
    | var
    | term_vector
    | term_pair
    | term_map

var : ID

term_vector : LBRACKET RBRACKET
    | LBRACKET term_vector_content RBRACKET
term_vector_content : term
    | term_vector_content COMMA term

term_pair : LPAREN term COMMA term RPAREN

term_map : MAP LBRACKET RBRACKET
    | MAP LBRACKET term_map_content RBRACKET
term_map_content : term_map_content COMMA term_pair
## Objects
program : statement_list

statement_list : statement
    | statement_list statement

statement : object_assignment
    | object_definition
    | unnamed_object_definition
    | template_definition
### Naming a built-in-value
object_assignment : var IS expression

### Objection definition / Prototypes
type : ID
    | INT
    | STR
object_definition : var IS type LPAREN member_list RPAREN
unnamed_object_definition : UNNAMED type LPAREN member_list RPARE

member_list : member
    | member_list member

member : var EQUALS expression
    | object_definition

## Templates
template_name : ID
template_definition : TEMPLATE template_name LBRACKET para_list RBRACKET IS type LPAREN member_list RPAREN
para_list : para
    : para_list COMMA para
para : var COLON type
    |  var COLON type EQUAL experssion

