from flask import Flask, render_template, request
from functools import cmp_to_key

app = Flask(__name__)

# =====================================================
# NODO
# =====================================================

class Nodo:

    def __init__(self, datos):

        self.datos = datos
        self.hijos = []
        self.padre = None
        self.costo = 0

    def get_datos(self):
        return self.datos

    def get_hijos(self):
        return self.hijos

    def get_padre(self):
        return self.padre

    def get_costo(self):
        return self.costo

    def set_hijos(self, hijos):

        self.hijos = hijos

        for h in hijos:
            h.padre = self

    def set_padre(self, padre):
        self.padre = padre

    def set_costo(self, costo):
        self.costo = costo

    def igual(self, nodo):
        return self.datos == nodo.get_datos()

    def en_lista(self, lista_nodos):

        for n in lista_nodos:

            if self.igual(n):
                return True

        return False


# =====================================================
# UCS
# =====================================================

def compara(x, y):
    return x.get_costo() - y.get_costo()


def buscar_solucion_UCS(conexiones, inicio, solucion):

    nodo_inicial = Nodo(inicio)

    nodo_inicial.set_costo(0)

    frontera = [nodo_inicial]

    visitados = []

    while len(frontera) != 0:

        frontera = sorted(
            frontera,
            key=cmp_to_key(compara)
        )

        nodo_actual = frontera.pop(0)

        visitados.append(nodo_actual)

        if nodo_actual.get_datos() == solucion:
            return nodo_actual

        for destino in conexiones.get(
            nodo_actual.get_datos(),
            {}
        ):

            hijo = Nodo(destino)

            costo = conexiones[
                nodo_actual.get_datos()
            ][destino]

            hijo.set_costo(
                nodo_actual.get_costo() + costo
            )

            hijo.set_padre(nodo_actual)

            if not hijo.en_lista(visitados):

                if not hijo.en_lista(frontera):

                    frontera.append(hijo)

    return None


# =====================================================
# BFS
# =====================================================

def buscar_solucion_BFS(conexiones, inicio, solucion):

    visitados = []

    frontera = []

    nodoInicial = Nodo(inicio)

    frontera.append(nodoInicial)

    while len(frontera) != 0:

        nodo = frontera.pop(0)

        visitados.append(nodo)

        if nodo.get_datos() == solucion:

            return nodo

        else:

            dato_nodo = nodo.get_datos()

            hijos = []

            for un_hijo in conexiones.get(
                dato_nodo,
                []
            ):

                hijo = Nodo(un_hijo)

                hijo.set_padre(nodo)

                hijos.append(hijo)

                if not hijo.en_lista(
                    visitados
                ) and not hijo.en_lista(
                    frontera
                ):

                    frontera.append(hijo)

            nodo.set_hijos(hijos)

    return None


# =====================================================
# DFS
# =====================================================

def buscar_solucion_DFS(
        estado_inicial,
        solucion
):

    solucionado = False

    visitados = []

    frontera = []

    nodo_inicial = Nodo(estado_inicial)

    frontera.append(nodo_inicial)

    while (
        not solucionado
    ) and len(frontera) != 0:

        nodo = frontera.pop()

        visitados.append(nodo)

        if nodo.get_datos() == solucion:

            solucionado = True

            return nodo

        else:

            dato = nodo.get_datos()

            hijo = [
                dato[1],
                dato[0],
                dato[2],
                dato[3]
            ]

            izquierdo = Nodo(hijo)

            hijo = [
                dato[0],
                dato[1],
                dato[3],
                dato[2]
            ]

            derecho = Nodo(hijo)

            hijo = [
                dato[2],
                dato[1],
                dato[0],
                dato[3]
            ]

            central = Nodo(hijo)

            nodo.set_hijos([
                izquierdo,
                central,
                derecho
            ])

            for h in nodo.get_hijos():

                if not h.en_lista(visitados):

                    frontera.append(h)

    return None


# =====================================================
# DATOS
# =====================================================

conexiones_ucs = {

    'JILOYORK': {
        'CDMX': 125,
        'QRO': 513
    },

    'CDMX': {
        'QRO': 433
    },

    'QRO': {
        'MONTERREY': 603
    },

    'MONTERREY': {}
}


conexiones_bfs = {

    'JILOYORK': {
        'CDMX',
        'QUERETARO'
    },

    'QUERETARO': {
        'OAXACA'
    },

    'OAXACA': {}
}


# =====================================================
# WEB
# =====================================================

@app.route("/", methods=["GET", "POST"])
def index():

    resultado_ucs = ""

    resultado_bfs = ""

    resultado_dfs = ""

    if request.method == "POST":

        # =================================================
        # UCS
        # =================================================

        nodo_ucs = buscar_solucion_UCS(
            conexiones_ucs,
            "JILOYORK",
            "MONTERREY"
        )

        if nodo_ucs:

            ruta = []

            while nodo_ucs is not None:

                ruta.append(
                    nodo_ucs.get_datos()
                )

                nodo_ucs = nodo_ucs.get_padre()

            ruta.reverse()

            resultado_ucs = (
                " → ".join(ruta)
            )

        else:

            resultado_ucs = "Sin solución"

        # =================================================
        # BFS
        # =================================================

        nodo_bfs = buscar_solucion_BFS(
            conexiones_bfs,
            "JILOYORK",
            "OAXACA"
        )

        if nodo_bfs:

            ruta = []

            while nodo_bfs is not None:

                ruta.append(
                    nodo_bfs.get_datos()
                )

                nodo_bfs = nodo_bfs.get_padre()

            ruta.reverse()

            resultado_bfs = (
                " → ".join(ruta)
            )

        else:

            resultado_bfs = "Sin solución"

        # =================================================
        # DFS
        # =================================================

        estado_inicial = [4,2,3,1]

        solucion = [1,2,3,4]

        nodo_dfs = buscar_solucion_DFS(
            estado_inicial,
            solucion
        )

        if nodo_dfs:

            resultado = []

            while nodo_dfs is not None:

                resultado.append(
                    str(nodo_dfs.get_datos())
                )

                nodo_dfs = nodo_dfs.get_padre()

            resultado.reverse()

            resultado_dfs = (
                " → ".join(resultado)
            )

        else:

            resultado_dfs = "Sin solución"

    return render_template(

        "index.html",

        resultado_ucs=resultado_ucs,

        resultado_bfs=resultado_bfs,

        resultado_dfs=resultado_dfs
    )
    
if __name__ == "__main__":
  app.run(debug=True)