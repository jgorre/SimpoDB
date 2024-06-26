import ply.lex as lex

# Reserved words
reserved_keywords = [
   'SELECT',
   'FROM',
   'CREATE',
   'SCHEMA',
   'TABLE',
   'INT',
   'STRING',
   'VALUES',
   'INSERT',
   'INTO',
   'PRIMARY',
   'KEY',
   'WHERE',
   'AND',
   'OR'
]

# List of token names including reserved words
tokens = [
   'STAR',
   'COMMA',
   'IDENTIFIER',
   'NUMBER',
   'LPAREN',
   'RPAREN',
   'EQUALS',
   'NOT_EQUALS',   
   'GREATER_THAN',
   'GREATER_THAN_OR_EQUAL',
   'LESS_THAN',
   'LESS_THAN_OR_EQUAL',   
] + reserved_keywords

# Regular expression rules for simple tokens
t_STAR   = r'\*'
t_COMMA  = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'='
t_NOT_EQUALS = r'!='
t_GREATER_THAN = r'>'
t_GREATER_THAN_OR_EQUAL = r'>='
t_LESS_THAN = r'<'
t_LESS_THAN_OR_EQUAL = r'<='

# A rule for identifiers and reserved words
def t_IDENTIFIER(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    t.type = t.value.upper() if t.value.upper() in reserved_keywords else 'IDENTIFIER'  # Check for reserved words
    return t

def t_NUMBER(t):
    r'\d+'
    return t

def t_STRING(t):
    r"'[^']*'"
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])

lexer = lex.lex()
