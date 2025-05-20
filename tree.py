class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

class ChessGameTree:
    def __init__(self):
        # Inicializar el árbol con un nodo raíz (por ejemplo, "Partida")
        self.root = TreeNode({ "blanca": "Partida", "negra": "" })

    def build_from_moves(self, moves):
        """
        Construye el árbol a partir de la lista de jugadas (tuplas (num_turno, jugada_blanca, jugada_negra)).
        Cada nodo hijo izquierdo es el siguiente turno.
        """
        if not moves:
            return
        # Construir el árbol: el hijo izquierdo de cada nodo es el siguiente turno
        nodo_actual = self.root
        for (num, blanca, negra) in moves:
            nuevo_nodo = TreeNode({ "blanca": blanca, "negra": negra })
            nodo_actual.left = nuevo_nodo
            nodo_actual = nuevo_nodo 

    def print_tree(self):
        """
        Recorre el árbol en orden (inorden) e imprime cada nodo (jugada blanca y negra) en consola.
        """
        def inorden(nodo):
            if nodo is None:
                return
            inorden(nodo.left)
            print(f"Blanca: {nodo.value['blanca']}, Negra: {nodo.value['negra']}")
            inorden(nodo.right)
        inorden(self.root) 