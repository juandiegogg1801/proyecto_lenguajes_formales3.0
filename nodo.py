class Nodo:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor
        self.hijos = []

    def agregar_hijo(self, nodo):
        self.hijos.append(nodo)

    def __repr__(self, nivel=0):
        indent = "  " * nivel
        res = f"{indent}{self.tipo}: {self.valor}\n"
        for hijo in self.hijos:
            res += hijo.__repr__(nivel + 1)
        return res
