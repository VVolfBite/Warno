## 词法分析部分 

**词法分析Token设计**:

Token:

1. 关键字部分：

```python
   {
   'export': 'EXPORT', 'is': 'IS','template': 'TEMPLATE','unnamed': 'UNNAMED','nil': 'NIL',
   'private': 'PRIVATE','int': 'INT', 'string':'STRING' ,'true': 'TRUE','false': 'FALSE', 'div': 'DIV','map': 'MAP'
   }
```

2. 基本类型部分：

```python
   {
   'integer':'NUMBER','HEX_NUMBER', 'floating point':'FLOAT', 'character 	 string':'STR', 'boolean':'BOOLEAN'
   }    
```

3. 运算符号部分:
```python
   {
      '=':'EQUALS', '+':'PLUS', '-':'MINUS', '*':'TIMES', 'div':'DIVIDE', '%':'MODULO'
   }
```
4. 布尔符号部分:
```python
   {
        '<':'LT', '>':'GT', '<=':'LE', '>=':'GE', '!=':'NE',
       '&':'AMPERSAND', '|':'AMPERSOR'
   }
```
5. 块号部分：
```python
   {
       '(':'LPAREN', ')':'RPAREN', '{':'LBRACE', '}':'RBRACE', '[':'LBRACKET', ']':'RBRACKET', '<':'LANGLE', '>':'RANGLE',
   }
```
6. 其他符号部分：
```python
   {
       ',':'COMMA', '.':'DOT', ':':'COLON', '~':'TILDE' ,'/':'SLASH', '?':'QUESTION',
       '$':'DOLLAR'
   }
```
## 语法分析部分

**语法分析推导式**：

1. 值、类型与表达式部分
```python
expression : expression PLUS expression
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
    | term

term : NUMBER
    | HEX_NUMBER
    | FLOAT
    | STR
    | BOOLEAN
    | var
    | term_vector
    | term_pair
    | term_map
    | term_object
    | term_template
    | term_path

var : ID

term_vector : LBRACKET RBRACKET
    | LBRACKET term_vector_content RBRACKET
term_vector_content : term
    | term_vector_content COMMA term

term_pair : LPAREN term COMMA term RPAREN

term_map : MAP LBRACKET RBRACKET
    | MAP LBRACKET term_map_content RBRACKET
term_map_content : term_map_content COMMA term_pair

term_object : type_name LPAREN member_list RPAREN
term_path : ID path_part
    | DOLLAR path_part
    | TILDE path_part
path_part : SLASH ID
    | SLASH ID path_part
type_name : ID
    | INT
    | STR
member_list : member
    | member_list member
member : var EQUALS expression

term_template : template_name LBRACKET para_list RBRACKET
template_name : ID
para_list : para
    : para_list COMMA para
para : var COLON type
    |  var COLON type EQUAL experssion
    
```
2. 基本结构部分
program : statement_list

statement_list : statement
    | statement_list statement

statement : normal_definition
    | unnamed_definition
    | template_definition

normal_definition : var IS expression
unnamed_definition : UNNAMED term_object
template_definition : TEMPLATE term_template IS term_object

# 语义制导最终目标
整理数据为列表和字典嵌套的内存结构：

expression : expression PLUS expression
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
    | term
计算为目标值

term : NUMBER
    | HEX_NUMBER
    | FLOAT
    | STR
    | BOOLEAN
    | var
    | term_vector
    | term_pair
    | term_map
    | term_object
    | term_template

term_vector : LBRACKET RBRACKET
    | LBRACKET term_vector_content RBRACKET
term_vector_content : term
    | term_vector_content COMMA term

term_pair : LPAREN term COMMA term RPAREN

term_map : MAP LBRACKET RBRACKET
    | MAP LBRACKET term_map_content RBRACKET
term_map_content : term_map_content COMMA term_pair

term_object : type LPAREN member_list RPAREN

term_template : template_name LBRACKET para_list RBRACKET

计算为目标值

var : ID
保存目标的字符标识

program : statement_list
保存为statement_list本身

statement_list : statement
    | statement_list statement
保存为列表，即[statement1, statement2, ...]

statement :normal_definition
    | unnamed_definition
    | template_definition
保存为对目标本身，目标本身应该总结为字典
### Objection definition / Prototypes
type : ID
    | INT
    | STR
保存为目标的类型，如TypeID，int，string

object_definition : var IS expression
保存为格式
{
    "statementType" : "definition",
    "key" : var.value,
    "members": expression.value,
}

unnamed_definition : UNNAMED type term_object
保存为格式
{
    "statementType" : "definition",
    "key": nil,
    "value": term_object.value,
}

member_list : member
    | member_list member
保存为格式 [member.value, member.value]

member : var EQUALS expression
    | term_object
保存为格式 
{
    "key": var.value,
    "value": expression.value,
}
或
{
    "key" : term_object.value["object_type"],
    "value" : term_object.value
}

## Templates
template_name : ID
保存目标的字符标识
template_definition : TEMPLATE term_template IS term_object
保存为
{
    "statementType" : "definition",
    "key" : term_template.value,
    "value" : term_object.value,
}
para_list : para
    : para_list COMMA para
保存为[para1, para2]
para : var COLON type
    |  var COLON type EQUAL experssion
保存为
{
    "key":var.value,
    "type":type.value,
    "value":expression.value,
}


额外规则：
1. type LPAREN member_list RPAREN 可以直接作为一种值或者表达式使用
2. 有一种新的term ，路径path_term, 如 $/SoundSettings/soundServicesVolumesDescriptor
3. 在部分定义前可以使用 export 关键字
4. map vector等的最后一个元素可以以多余逗号结束
5. {}可以用于GUID:{878a7fc2-aa73-405f-bdf3-fe6fbf2e8342}
