import re

class AnalizadorSemantico:
    def __init__(self, arbol):
        self.arbol = arbol
        self.resultado = []
        self.css_properties_validas = {
            "color", "background-color", "font-family", "font-size", "text-align",
            "margin", "padding", "border", "width", "height", "line-height",
            "text-decoration", "display", "position", "top", "left", "right",
            "bottom", "z-index", "overflow", "visibility", "opacity", "float", "clear"
        }

    def analizar(self):
        self._analizar_nodo(self.arbol)
        return "\n".join(self.resultado)

    def _analizar_nodo(self, nodo, nivel=0):
        if isinstance(nodo, list):
            for subnodo in nodo:
                self._analizar_nodo(subnodo, nivel)
        elif isinstance(nodo, tuple):
            tipo = nodo[0]
            if tipo == 'DOCUMENTO':
                self.resultado.append("Documento XML/HTML estructurado correctamente.")
                self._analizar_nodo(nodo[1], nivel + 1)

            elif tipo == 'DECLARACION_XML':
                self.resultado.append("Declaración XML encontrada. Establece la versión y la codificación del documento.")

            elif tipo == 'DOCTYPE':
                self.resultado.append("Declaración DOCTYPE: Define el tipo de documento y la DTD usada.")

            elif tipo == 'COMENTARIO':
                self.resultado.append("Comentario HTML: contiene información no visible en la página.")

            elif tipo == 'TEXTO':
                contenido = nodo[1].strip()
                if contenido:
                    self.resultado.append(f"Texto: '{contenido}'")

            elif tipo == 'ETIQUETA':
                apertura, hijos, cierre = nodo[1], nodo[2], nodo[3]
                nombre = self._extraer_nombre_etiqueta(apertura)
                self.resultado.append(f"Etiqueta <{nombre}>: contiene elementos anidados.")
                self._analizar_nodo(hijos, nivel + 1)

                # Detectar CSS embebido y validarlo dentro de <style>
                if nombre.lower() == "style":
                    texto_css = self._extraer_texto_css(hijos)
                    if texto_css.strip():
                        self.resultado.append("Bloque CSS embebido encontrado. Validando propiedades...")
                        errores_css = self._analizar_css(texto_css)
                        if errores_css:
                            self.resultado.append("Errores en el bloque CSS:")
                            self.resultado.extend(errores_css)
                        else:
                            self.resultado.append("✔ Todas las propiedades CSS son válidas.")

                self.resultado.append(f"Fin de etiqueta </{nombre}>.")

            elif tipo == 'ETIQUETA_VACIA':
                nombre = self._extraer_nombre_etiqueta(nodo[1])
                self.resultado.append(f"Etiqueta vacía <{nombre}/> encontrada. No contiene contenido interno.")

        else:
            pass  # nodo tipo string o irrelevante

    def _extraer_nombre_etiqueta(self, etiqueta):
        m = re.match(r'<\s*/?\s*([a-zA-Z0-9]+)', etiqueta)
        return m.group(1) if m else "desconocido"

    def _extraer_texto_css(self, hijos):
        """Busca el contenido de tipo TEXTO dentro de la etiqueta <style>"""
        for hijo in hijos:
            if isinstance(hijo, tuple) and hijo[0] == 'TEXTO':
                return hijo[1]
        return ""

    def _analizar_css(self, texto_css):
        errores = []
        # Extraer bloques CSS: selector { reglas }
        bloques_css = re.findall(r'([^{]+)\{([^}]+)\}', texto_css)
        for selector, reglas in bloques_css:
            propiedades = re.findall(r'([a-zA-Z\-]+)\s*:', reglas)
            for prop in propiedades:
                prop_limpio = prop.strip()
                if prop_limpio not in self.css_properties_validas:
                    errores.append(f"Propiedad CSS inválida: '{prop_limpio}' en selector '{selector.strip()}'")
        return errores
