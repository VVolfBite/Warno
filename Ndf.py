import ply.lex as lex
import ply.yacc as yacc

import ply.lex as lex
reserves = (
    'is',
    'export',
    'private',
    'template',
    'MAP'
)
tokens = (
    'IDENTIFIER',
    'STRING',
    'NUMBER',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'COMMA',
    'IS',
    'MAP',
    'EXPORT',
    'PRIVATE',
    'TEMPLATE',
    'EQUALS',
)

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','
t_IS = r'is'
t_MAP = r'MAP'
t_EXPORT = r'export'
t_PRIVATE = r'private'
t_TEMPLATE = r'template'
t_EQUALS = r'='

t_ignore = ' \t\n'

def t_COMMENT(t):
    r'\/\/[^\n]*'
    pass  

def t_IDENTIFIER(t):
    r'[-a-zA-Z_~/:<>${}][-a-zA-Z0-9_~/:<>${}]*'
    t.type = 'IDENTIFIER'
    if t.value in reserves:
        t.type = t.value.upper()
    return t


def t_STRING(t):
    r'\'[^\']*\'|\"[^\"]*\"'
    t.type = 'STRING'
    return t

def t_NUMBER(t):
    r'-?\d+(\.\d+)?'
    t.type = 'NUMBER'
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# [{'a': 'b','c':'d'},[{'a':'b','c':{'d':'e'},'d':['h','i']},'c','d']]

# [
#     {
#         'a':'b',
#         'c':'d'
#     },
#     [
#         {
#             'a':'b',
#             'c':{
#                     'd':'e'
#                 }
#             'd':[
#                     'h','i'
#                 ]
#         },
#         'c',
#         'd'
#     ]
# ]

def print_nested_structure(structure, indent=0, is_last=False):
    if isinstance(structure, list):
        print("  " * indent + "[")
        for i, item in enumerate(structure):
            is_last_item = i == len(structure) - 1
            print_nested_structure(item, indent + 1, is_last=is_last_item)
        print("  " * indent + "]" + ("," if not is_last else ""))
    elif isinstance(structure, dict):
        print("  " * indent + "{")
        for i, (key, value) in enumerate(structure.items()):
            is_last_item = i == len(structure) - 1
            print(f"{'  ' * (indent + 1)}'{key}': ", end="")
            print_nested_structure(value, indent + 2, is_last=is_last_item)
        print("  " * indent + "}" + ("," if not is_last else ""))
    else:
        print(f"{'  ' * indent}'{structure}'", end="")
        print("," if not is_last else "")

# 示例
# p = [{'a': 'b', 'c': 'd'}, [{'a': 'b'}, 'c', 'd']]
# print_nested_structure(p)


def p_record_list(p):
    '''
    record_list : record_list record
                | record
                | empty
    '''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]
    print_nested_structure(p[0])
    

def p_record(p):
    '''
    record : modifiers record_name IS record_type LPAREN property_list RPAREN
           | modifiers record_name IS value
           | record_name IS record_type LPAREN property_list RPAREN
           | record_name IS value
           | record_type LPAREN property_list RPAREN
    '''
    if len(p) == 8:
        p[0] = {'record_name': p[2], 'record_type': p[4], 'record_property_list': p[6]}
    elif len(p) == 7:
        p[0] = {'record_name': p[1], 'record_type': p[3], 'record_property_list': p[5]}
    elif len(p) == 5 and p[2] == '(' and p[4] == ')':
        p[0] = {'record_type': p[1], 'record_property_list': p[3]}
    elif len(p) == 5 and p[3] == 'is':
        p[0] = {'record_name': p[2], 'record_value': p[4]}
    elif len(p) == 4:
        p[0] = {'record_name': p[1], 'record_value': p[3]}

def p_modifiers(p):
    '''
    modifiers : EXPORT
              | PRIVATE
              | TEMPLATE
    '''
    p[0] = p[1]

def p_record_name(p):
    '''
    record_name : IDENTIFIER
    '''
    p[0] = p[1]
    

def p_record_type(p):
    '''
    record_type : IDENTIFIER
    '''
    p[0] = p[1]

def p_property_list(p):
    '''
    property_list : property_list property
                  | property
                  | empty
    '''
    if len(p) == 3:
        p[1].update(p[2])
        p[0] = p[1]
    else:
        p[0] = p[1]
    
def p_property(p):
    '''
    property : property_key EQUALS property_value
    '''
    p[0] = {p[1]: p[3]}
    
    
def p_property_key(p):
    '''
    property_key : IDENTIFIER
    '''
    p[0] = p[1]
    

def p_property_value(p):
    '''
    property_value : value
    '''
    p[0] = p[1]
    

def p_value(p):
    '''
    value : NUMBER
          | STRING
          | IDENTIFIER
          | MAP list
          | record
          | list
          | pair
    '''
    p[0] = p[1]
    

def p_list(p):
    '''
    list : LBRACKET list_values RBRACKET
        | LBRACKET list_values COMMA RBRACKET
    '''
    p[0] = p[2]
    
    

def p_list_values(p):
    '''
    list_values : list_values COMMA value
                | value
                | empty
    '''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]

    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_pair(p):
    '''
    pair : LPAREN value COMMA value RPAREN
    '''
    p[0] = (p[2], p[4])

def p_empty(p):
    '''
    empty :
    '''
    pass

def p_error(p):
    print(f"Syntax error at line {p.lineno}, position {p.lexpos}: Unexpected token '{p.value}' in production {p.type}")




parser = yacc.yacc()


example_input = '''
export Descriptor_ShowRoomUnit_Su_25_rkt_SOV is TEntityDescriptor
(
    DescriptorId        = GUID:{83bf50d6-8de0-4b97-82ec-76a2256405f2}
    ClassNameForDebug   = "ShowRoomUnit_Su_25_rkt_SOV"
    ModulesDescriptors = [
        TTypeUnitModuleDescriptor
        (
            Nationalite                      = ENationalite/Axis
            MotherCountry                    = 'SOV'
            AcknowUnitType                   = ~/TAcknowUnitType_GroundAtk
            TypeUnitFormation                = 'None'
        ),
        ~/ShowroomPositionModuleDescriptor,
        TApparenceModelModuleDescriptor
        (
            PickableObject                     = True
            Depiction                          = ~/Gfx_Su_25_rkt_SOV_Showroom_Autogen
            GameplayBBoxBoneName               = ''
        ),
        $/GFX/Everything/WeaponDescriptor_Su_25_rkt_SOV,
        ~/LinkTeamModuleDescriptor,
        ~/EffectApplierModuleDescriptor,
        TExperienceModuleDescriptor
        (
            ExperienceLevelsPackDescriptor = ~/ExperienceLevelsPackDescriptor_XP_pack_simple_v2
            CanWinExperience = True
            ExperienceGainBySecond = ~/ExperienceGainBySecond
            ExperienceMultiplierBonusOnKill = ~/ExperienceMultiplierBonusOnKill
        ),
        TCameraShowroomModuleDescriptor
        (
            Token = 'BigVehicle'
            SpawnType = EShowroomSpawnType/Airplane
        ),
    ]
)
export Descriptor_ShowRoomUnit_Su_27S_SOV is TEntityDescriptor
(
    DescriptorId        = GUID:{5dc2ed7d-7a81-4a14-a6ad-635d0eeb7de1}
    ClassNameForDebug   = "ShowRoomUnit_Su_27S_SOV"
    ModulesDescriptors = [
        TTypeUnitModuleDescriptor
        (
            Nationalite                      = ENationalite/Axis
            MotherCountry                    = 'SOV'
            AcknowUnitType                   = ~/TAcknowUnitType_AirSup
            TypeUnitFormation                = 'None'
        ),
        ~/ShowroomPositionModuleDescriptor,
        TApparenceModelModuleDescriptor
        (
            PickableObject                     = True
            Depiction                          = ~/Gfx_Su_27S_SOV_Showroom_Autogen
            GameplayBBoxBoneName               = ''
        ),
        $/GFX/Everything/WeaponDescriptor_Su_27S_SOV,
        ~/LinkTeamModuleDescriptor,
        ~/EffectApplierModuleDescriptor,
        TExperienceModuleDescriptor
        (
            ExperienceLevelsPackDescriptor = ~/ExperienceLevelsPackDescriptor_XP_pack_simple_v2
            CanWinExperience = True
            ExperienceGainBySecond = ~/ExperienceGainBySecond
            ExperienceMultiplierBonusOnKill = ~/ExperienceMultiplierBonusOnKill
        ),
        TCameraShowroomModuleDescriptor
        (
            Token = 'BigVehicle'
            SpawnType = EShowroomSpawnType/Airplane
        ),
    ]
)
'''
result = parser.parse(example_input)

