import ply.yacc as yacc
from lexer_ply import tokens
import re

def get_tag_name(etiqueta):
    m = re.match(r'<\s*/?\s*([a-zA-Z0-9]+)', etiqueta)
    if m:
        return m.group(1)
    return None

def p_documento(p):
    '''documento : elementos'''
    p[0] = ('DOCUMENTO', p[1])

def p_elementos(p):
    '''elementos : elementos elemento
                 | elemento'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_elemento(p):
    '''elemento : comentario
                | etiqueta
                | texto
                | DECLARACION_XML
                | DOCTYPE'''
    p[0] = p[1]

def p_comentario(p):
    'comentario : COMENTARIO_HTML'
    p[0] = ('COMENTARIO', p[1])

def p_texto(p):
    'texto : TEXTO'
    p[0] = ('TEXTO', p[1])

def p_etiqueta(p):
    '''etiqueta : ETIQUETA_APERTURA elementos ETIQUETA_CIERRE
                | ETIQUETA_VACIA'''
    if len(p) == 4:
        nombre_abr = get_tag_name(p[1])
        nombre_cie = get_tag_name(p[3])
        if nombre_abr != nombre_cie:
            print(f"Error: etiqueta de apertura {nombre_abr} no coincide con cierre {nombre_cie}")
        p[0] = ('ETIQUETA', p[1], p[2], p[3])
    else:
        p[0] = ('ETIQUETA_VACIA', p[1])

def p_error(p):
    if p:
        print(f"Error sintáctico en token '{p.value}' (línea {p.lineno})")
    else:
        print("Error sintáctico en EOF")

parser = yacc.yacc()
