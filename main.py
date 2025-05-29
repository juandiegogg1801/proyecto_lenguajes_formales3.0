from lexer_ply import lexer
from parser_ply import parser
from semantico import AnalizadorSemantico

def imprimir_tokens(tokens):
    for token in tokens:
        tipo = token.type
        valor = token.value
        if tipo == 'TEXTO' and valor.strip() == '':
            continue
        # Si es texto multilínea, imprimir con saltos de línea reales indentado
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
        # Nodo hoja (string)
        texto = nodo.strip('\r\n ')  # Quitar solo saltos y espacios en los extremos
        if texto == '':
            # No imprimir líneas vacías o solo espacios
            return

        if '\n' in nodo:
            # Si el texto tiene saltos, imprimir cada línea no vacía
            lineas = nodo.splitlines()
            for linea in lineas:
                if linea.strip() != '':
                    print(f"{indent}{linea.rstrip()}")
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

# Análisis semantico
print("\nAnálisis semántico:")
analizador = AnalizadorSemantico(arbol)
descripcion = analizador.analizar()
print(descripcion)
