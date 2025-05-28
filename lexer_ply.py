import ply.lex as lex

tokens = (
    'DECLARACION_XML',
    'DOCTYPE',
    'COMENTARIO_HTML',
    'ETIQUETA_APERTURA',
    'ETIQUETA_CIERRE',
    'ETIQUETA_VACIA',
    'TEXTO',
)

t_ignore = ' \t\r'

def t_DECLARACION_XML(t):
    r'<\?xml\s+version\s*=\s*".*?"\s+encoding\s*=\s*".*?"\s*\?>'
    return t

def t_DOCTYPE(t):
    r'<!DOCTYPE[^>]*>'
    return t

def t_COMENTARIO_HTML(t):
    r'<!--(.|\n)*?-->'
    return t

def t_ETIQUETA_VACIA(t):
    r'<[a-zA-Z][a-zA-Z0-9:_\-\.]*(\s+[a-zA-Z_:][a-zA-Z0-9_\-:\.]*\s*=\s*"[^"]*")*\s*/>'
    return t

def t_ETIQUETA_APERTURA(t):
    r'<[a-zA-Z][a-zA-Z0-9:_\-\.]*(\s+[a-zA-Z_:][a-zA-Z0-9_\-:\.]*\s*=\s*"[^"]*")*\s*>'
    return t

def t_ETIQUETA_CIERRE(t):
    r'</[a-zA-Z][a-zA-Z0-9:_\-\.]*\s*>'
    return t

def t_TEXTO(t):
    r'[^<]+'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Error léxico: carácter ilegal '{t.value[0]}' en línea {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()
