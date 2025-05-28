import ply.lex as lex

tokens = [
    'COMENTARIO_HTML',
    'ETIQUETA_APERTURA',
    'ETIQUETA_CIERRE',
    'TEXTO',
]

t_ignore = ' \t\n'

def t_COMENTARIO_HTML(t):
    r'<!--(.|\n)*?-->'
    return t

def t_ETIQUETA_APERTURA(t):
    r'<[a-zA-Z][a-zA-Z0-9\s=\'"-]*?>'
    return t

def t_ETIQUETA_CIERRE(t):
    r'</[a-zA-Z][a-zA-Z0-9]*>'
    return t

def t_TEXTO(t):
    r'[^<]+'
    # Todo lo que no es una etiqueta se considera texto
    return t

def t_error(t):
    print(f"Error léxico en {t.value[0]!r}")
    t.lexer.skip(1)

lexer = lex.lex()
