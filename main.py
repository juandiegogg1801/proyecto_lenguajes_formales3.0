from lexer_ply import lexer
from parser_ply import parser

# Lee tu archivo de entrada
with open('entrada.txt', 'r', encoding='utf-8') as f:
    data = f.read()

# Análisis léxico
lexer.input(data)
print("Tokens lexicos:")
while True:
    tok = lexer.token()
    if not tok:
        break
    print(f"{tok.type}: '{tok.value}'")

# Análisis sintáctico
print("\nÁrbol sintáctico:")
arbol = parser.parse(data)
print(arbol)
