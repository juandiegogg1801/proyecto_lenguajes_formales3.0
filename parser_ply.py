import ply.yacc as yacc
from lexer_ply import tokens

class Nodo:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor
        self.hijos = []

    def agregar_hijo(self, nodo):
        self.hijos.append(nodo)

    def __repr__(self, nivel=0):
        ret = "\t"*nivel + f"{self.tipo}: {self.valor}\n"
        for hijo in self.hijos:
            ret += hijo.__repr__(nivel+1)
        return ret

def p_documento(p):
    '''documento : elementos'''
    p[0] = Nodo("DOCUMENTO")
    for elem in p[1]:
        p[0].agregar_hijo(elem)

def p_elementos_lista(p):
    '''elementos : elementos elemento'''
    p[0] = p[1]
    p[0].append(p[2])

def p_elementos_uno(p):
    '''elementos : elemento'''
    p[0] = [p[1]]

def p_elemento_etiqueta(p):
    '''elemento : ETIQUETA_APERTURA elementos ETIQUETA_CIERRE'''
    # Para simplificar, no validamos que etiquetas de apertura y cierre coincidan
    nodo = Nodo("ETIQUETA", p[1])
    for hijo in p[2]:
        nodo.agregar_hijo(hijo)
    p[0] = nodo

def p_elemento_texto(p):
    '''elemento : TEXTO'''
    p[0] = Nodo("TEXTO", p[1].strip())

def p_elemento_comentario(p):
    '''elemento : COMENTARIO_HTML'''
    p[0] = Nodo("COMENTARIO", p[1])

def p_error(p):
    if p:
        print(f"Error sintáctico en token {p.value!r} (línea {p.lineno})")
    else:
        print("Error sintáctico en EOF")

parser = yacc.yacc()
