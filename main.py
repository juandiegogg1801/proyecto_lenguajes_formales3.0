from lexer_ply import lexer
from parser_ply import parser
from semantico import AnalizadorSemantico

def imprimir_tokens(tokens):
    for token in tokens:
        tipo = token.type
        valor = token.value
        if tipo == 'TEXTO' and valor.strip() == '':
            continue
        if tipo == 'TEXTO' and '\n' in valor:
            print(f"{tipo}:")
            for linea in valor.splitlines():
                print(f"    {linea}")
        else:
            print(f"{tipo}: {repr(valor)}")

def imprimir_arbol(nodo, nivel=0):
    indent = '  ' * nivel
    if isinstance(nodo, tuple):
        etiqueta = nodo[0]
        contenido = nodo[1:]
        print(f"{indent}{etiqueta}:")
        for elem in contenido:
            imprimir_arbol(elem, nivel + 1)
    elif isinstance(nodo, list):
        for elem in nodo:
            imprimir_arbol(elem, nivel)
    else:
        if nodo is None:
            return
        texto = nodo.strip('\r\n ')
        if texto == '':
            return
        if '\n' in nodo:
            for linea in nodo.splitlines():
                if linea.strip() != '':
                    print(f"{indent}{linea.rstrip()}")
        else:
            print(f"{indent}{repr(nodo)}")

# Leer archivo
with open('entrada.txt', 'r', encoding='utf-8') as f:
    data = f.read()

# Análisis léxico
lexer.input(data)
tokens = []
while True:
    tok = lexer.token()
    if not tok:
        break
    tokens.append(tok)

print("Tokens léxicos (filtrados):")
imprimir_tokens(tokens)

# Análisis sintáctico
print("\nÁrbol sintáctico:")
parser.error = False  # ← reiniciar bandera de error

try:
    arbol = parser.parse(data)
except SyntaxError as e:
    print(f"Se detuvo el análisis por error: {e}")
    arbol = None

if not parser.error and arbol is not None:
    imprimir_arbol(arbol)

    # Análisis semántico
    print("\nAnálisis semántico:")
    analizador = AnalizadorSemantico(arbol)
    descripcion = analizador.analizar()
    print(descripcion)
else:
    print("No se pudo generar el árbol sintáctico ni se realizó el análisis semántico.")
