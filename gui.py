from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QGraphicsView, QGraphicsScene, QLabel,
    QScrollBar
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPen, QColor
from parser import SANParser
from tree import ChessGameTree

class ChessGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Árbol de Ajedrez')
        self.setGeometry(100, 100, 1200, 700)
        self.init_ui()
        self.parser = SANParser()
        self.tree = None

    def init_ui(self):
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal vertical
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Área de texto para la partida
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText('Pega aquí la partida en notación SAN...')
        main_layout.addWidget(self.text_edit)

        # Botón para analizar
        button_layout = QHBoxLayout()
        self.analyze_button = QPushButton('Analizar Partida')
        self.analyze_button.clicked.connect(self.analyze_game)
        button_layout.addStretch()
        button_layout.addWidget(self.analyze_button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        # Área de dibujo para el árbol
        self.graphics_view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)
        # Forzar scrollbars siempre visibles si es necesario
        self.graphics_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.graphics_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        main_layout.addWidget(self.graphics_view, stretch=1)

        # Etiqueta de estado
        self.status_label = QLabel('')
        main_layout.addWidget(self.status_label)

    def analyze_game(self):
        san_text = self.text_edit.toPlainText()
        moves = self.parser.parse(san_text)
        if isinstance(moves, list):
            self.tree = ChessGameTree()
            self.tree.build_from_moves(moves)
            self.status_label.setText(f'Partida válida. Turnos: {len(moves)}')
            self.draw_tree()
        else:
            self.tree = None
            self.status_label.setText(f'Error: {moves}')

    def draw_tree(self):
        # Limpiar la escena
        self.scene.clear()
        if not self.tree or not self.tree.root:
            return
        # Parámetros de dibujo (restaurados a valores anteriores)
        node_radius = 30
        x_center = 800
        y_start = 50
        x_offset = 200  # Separación horizontal
        y_step = 100    # Separación vertical
        max_depth = 0

        # Brushes y pens para colores
        brush_default = QBrush(Qt.white)
        pen_default = QPen(Qt.black)
        brush_capture = QBrush(Qt.red)
        pen_capture = QPen(Qt.black)
        brush_black = QBrush(QColor(80, 80, 80))
        pen_black = QPen(Qt.black)

        # Dibujar nodo raíz "Partida"
        partida_x = x_center
        partida_y = y_start
        partida_ellipse = self.scene.addEllipse(partida_x - node_radius, partida_y - node_radius, node_radius * 2, node_radius * 2, pen_default, brush_default)
        self.scene.addText("Partida").setPos(partida_x - node_radius + 5, partida_y - 10)

        # Recorrer el árbol y dibujar nodos blancos y negros
        def draw_turns(node, x, y, depth, move_number):
            nonlocal max_depth
            if node is None:
                return
            max_depth = max(max_depth, depth)
            # Nodo blanca
            blanca_x = x
            blanca_y = y + y_step
            blanca_text = node.value.get('blanca', '')
            # Detectar captura en jugada blanca
            if 'x' in blanca_text:
                brush_b = brush_capture
                pen_b = pen_capture
            else:
                brush_b = brush_default
                pen_b = pen_default
            blanca_ellipse = self.scene.addEllipse(blanca_x - node_radius, blanca_y - node_radius, node_radius * 2, node_radius * 2, pen_b, brush_b)
            self.scene.addLine(x, y + node_radius, blanca_x, blanca_y - node_radius)
            # Enumerar jugada blanca
            self.scene.addText(f"{move_number}. {blanca_text}").setPos(blanca_x - node_radius + 5, blanca_y - 10)
            # Nodo negra (si existe)
            negra_text = node.value.get('negra', '')
            if negra_text:
                negra_x = x + x_offset
                negra_y = blanca_y
                # Detectar captura en jugada negra
                if 'x' in negra_text:
                    brush_n = brush_capture
                    pen_n = pen_capture
                else:
                    brush_n = brush_black
                    pen_n = pen_black
                negra_ellipse = self.scene.addEllipse(negra_x - node_radius, negra_y - node_radius, node_radius * 2, node_radius * 2, pen_n, brush_n)
                self.scene.addLine(blanca_x + node_radius, blanca_y, negra_x - node_radius, negra_y)
                # Enumerar jugada negra
                self.scene.addText(f"{move_number}... {negra_text}").setPos(negra_x - node_radius + 5, negra_y - 10)
                # El siguiente turno (hijo izquierdo) parte del nodo negra
                draw_turns(node.left, negra_x, negra_y, depth + 1, move_number + 1)
            else:
                # Si no hay jugada negra, el siguiente turno parte del nodo blanca
                draw_turns(node.left, blanca_x, blanca_y, depth + 1, move_number + 1)

        # Comenzar desde el primer turno (hijo izquierdo de la raíz)
        draw_turns(self.tree.root.left, partida_x, partida_y, 1, 1)
        # Mucho más scroll horizontal (reducido a dos tercios)
        self.graphics_view.setSceneRect(0, 0, x_center + 20 * x_offset + 4000, y_start + (max_depth + 3) * y_step)
        # (fitInView eliminado)

# Para probar la GUI independientemente
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = ChessGUI()
    window.show()
    sys.exit(app.exec_()) 