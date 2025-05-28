from lexer_ply import lexer
from parser_ply import parser

def imprimir_tokens(tokens):
    for token in tokens:
        tipo = token.type
        valor = token.value
        # Omitir texto que solo tenga espacios o saltos de línea
        if tipo == 'TEXTO' and valor.strip() == '':
            continue
        print(f"{tipo}: {repr(valor)}")

def imprimir_arbol(nodo, nivel=0):
    indent = "  " * nivel
    if isinstance(nodo, tuple):
        tipo = nodo[0]
        contenido = nodo[1]
        if isinstance(contenido, list):
            print(f"{indent}{tipo}:")
            for hijo in contenido:
                imprimir_arbol(hijo, nivel + 1)
        else:
            print(f"{indent}{tipo}: {repr(contenido)}")
    elif isinstance(nodo, list):
        for hijo in nodo:
            imprimir_arbol(hijo, nivel)
    else:
        print(f"{indent}{repr(nodo)}")

# Lee tu archivo de entrada
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
arbol = parser.parse(data)
imprimir_arbol(arbol)