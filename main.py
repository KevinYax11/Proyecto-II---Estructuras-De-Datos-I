import sys
import pickle
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QComboBox,
    QTextEdit,
    QMessageBox,
    QFileDialog,
)
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from PyQt5.QtCore import Qt


# Clase para representar un nodo en las estructuras de datos
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None
        self.left = None
        self.right = None


# Clase para la estructura de datos Pila
class Stack:
    def __init__(self):
        self.top = None

    # Método para agregar un elemento a la pila
    def push(self, data):
        new_node = Node(data)
        if self.top:
            new_node.next = self.top
        self.top = new_node

    # Método para eliminar y devolver el elemento en la cima de la pila
    def pop(self):
        if self.top:
            data = self.top.data
            self.top = self.top.next
            return data
        return None

    # Método para obtener el elemento en la cima de la pila sin eliminarlo
    def peek(self):
        if self.top:
            return self.top.data
        return None

    # Método para verificar si la pila está vacía
    def is_empty(self):
        return self.top is None


# Clase para la estructura de datos Cola
class Queue:
    def __init__(self):
        self.front = None
        self.rear = None

    # Método para agregar un elemento a la cola
    def enqueue(self, data):
        new_node = Node(data)
        if not self.front:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

    # Método para eliminar y devolver el elemento en el frente de la cola
    def dequeue(self):
        if self.front:
            data = self.front.data
            self.front = self.front.next
            if not self.front:
                self.rear = None
            return data
        return None

    # Método para obtener el elemento en el frente de la cola sin eliminarlo
    def peek(self):
        if self.front:
            return self.front.data
        return None

    # Método para verificar si la cola está vacía
    def is_empty(self):
        return self.front is None


# Clase para la estructura de datos Lista Enlazada
class LinkedList:
    def __init__(self):
        self.head = None

    # Método para insertar un elemento al final de la lista enlazada
    def insert_at_end(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    # Método para recorrer e imprimir la lista enlazada (solo para fines de prueba)
    def traverse(self):
        current = self.head
        while current:
            print(current.data)
            current = current.next


# Clase para la ventana principal de la aplicación
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.setWindowTitle("Visualizador de Estructuras")
        self.setGeometry(100, 100, 800, 600)

        # Configuración del diseño de la interfaz
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Lienzo para dibujar las estructuras de datos
        self.canvas = Canvas()
        self.layout.addWidget(self.canvas)

        # Diseño para los controles
        self.controls_layout = QHBoxLayout()
        self.layout.addLayout(self.controls_layout)

        # ComboBox para seleccionar el tipo de estructura de datos
        self.structure_combo = QComboBox()
        self.structure_combo.addItems(["Pila", "Cola", "Lista Enlazada"])
        self.controls_layout.addWidget(self.structure_combo)

        # ComboBox para seleccionar el tipo de dato
        self.data_type_combo = QComboBox()
        self.data_type_combo.addItems(["Entero", "Flotante", "Cadena de Texto"])
        self.controls_layout.addWidget(self.data_type_combo)

        # Botón para insertar datos en la estructura de datos seleccionada
        self.insert_button = QPushButton("Insertar")
        self.insert_button.clicked.connect(self.insert_data)
        self.controls_layout.addWidget(self.insert_button)

        # Botones para guardar y cargar estructuras de datos desde archivos
        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.save_structure)
        self.controls_layout.addWidget(self.save_button)

        self.load_button = QPushButton("Cargar")
        self.load_button.clicked.connect(self.load_structure)
        self.controls_layout.addWidget(self.load_button)

        # Estructura de datos actualmente seleccionada
        self.structure = None

    # Método para insertar datos en la estructura de datos seleccionada
    def insert_data(self):
        structure_type = self.structure_combo.currentText()
        data_type = self.data_type_combo.currentText()
        data = self.get_data_from_user()

        if structure_type == "Pila":
            if not self.structure:
                self.structure = Stack()
            self.structure.push(data)
        elif structure_type == "Cola":
            if not self.structure:
                self.structure = Queue()
            self.structure.enqueue(data)
        elif structure_type == "Lista Enlazada":
            if not self.structure:
                self.structure = LinkedList()
            self.structure.insert_at_end(data)

        self.canvas.update()

    # Método para guardar la estructura de datos actual en un archivo
    def save_structure(self):
        if not self.structure:
            QMessageBox.warning(self, "Advertencia", "No hay ninguna estructura de datos para guardar.")
            return

        filename, _ = QFileDialog.getSaveFileName(
            self, "Guardar estructura de datos", "", "Archivos de datos (*.dat)"
        )
        if filename:
            with open(filename, "wb") as file:
                pickle.dump(self.structure, file)
            QMessageBox.information(self, "Éxito", "La estructura de datos se ha guardado correctamente.")

    # Método para cargar una estructura de datos desde un archivo
    def load_structure(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Cargar estructura de datos", "", "Archivos de datos (*.dat)"
        )
        if filename:
            with open(filename, "rb") as file:
                self.structure = pickle.load(file)
            QMessageBox.information(self, "Éxito", "La estructura de datos se ha cargado correctamente.")
            self.canvas.update()

    # Método para obtener datos del usuario (a implementar según sea necesario)
    def get_data_from_user(self):
        # Implementar este método según sea necesario para obtener datos del usuario
        pass


# Clase para el lienzo donde se dibujarán las estructuras de datos
class Canvas(QWidget):
    def __init__(self):
        super().__init__()

    # Método para dibujar las estructuras de datos
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if isinstance(window.structure, Stack):
            self.draw_stack(painter)
        elif isinstance(window.structure, Queue):
            self.draw_queue(painter)
        elif isinstance(window.structure, LinkedList):
            self.draw_linked_list(painter)

    # Método para dibujar la estructura de datos Pila
    def draw_stack(self, painter):
        if not window.structure:
            return

        font = QFont("Arial", 12)
        painter.setFont(font)

        node_radius = 20
        margin = 30
        x = self.width() / 2
        y = margin

        current_node = window.structure.top
        while current_node:
            painter.drawEllipse(x - node_radius, y - node_radius, 2 * node_radius, 2 * node_radius)
            painter.drawText(x - node_radius, y - node_radius, 2 * node_radius, 2 * node_radius, Qt.AlignCenter, str(current_node.data))
            y += 2 * node_radius + margin
            current_node = current_node.next

    # Método para dibujar la estructura de datos Cola
    def draw_queue(self, painter):
        if not window.structure:
            return

        font = QFont("Arial", 12)
        painter.setFont(font)

        node_radius = 20
        margin = 30
        x = self.width() / 2
        y = margin

        current_node = window.structure.front
        while current_node:
            painter.drawEllipse(x - node_radius, y - node_radius, 2 * node_radius, 2 * node_radius)
            painter.drawText(x - node_radius, y - node_radius, 2 * node_radius, 2 * node_radius, Qt.AlignCenter, str(current_node.data))
            y += 2 * node_radius + margin
            current_node = current_node.next

    # Método para dibujar la estructura de datos Lista Enlazada
    def draw_linked_list(self, painter):
        if not window.structure:
            return

        font = QFont("Arial", 12)
        painter.setFont(font)

        node_radius = 20
        margin = 30
        x = self.width() / 2
        y = margin

        current_node = window.structure.head
        while current_node:
            painter.drawEllipse(x - node_radius, y - node_radius, 2 * node_radius, 2 * node_radius)
            painter.drawText(x - node_radius, y - node_radius, 2 * node_radius, 2 * node_radius, Qt.AlignCenter, str(current_node.data))
            if current_node.next:
                painter.drawLine(x, y + node_radius, x, y + node_radius + margin / 2)
                painter.drawLine(x, y + node_radius + margin / 2, x + margin / 2, y + node_radius + margin / 2)
                painter.drawLine(x + margin / 2, y + node_radius + margin / 2, x + margin / 2, y + 3 * node_radius + margin)
                painter.drawLine(x + margin / 2, y + 3 * node_radius + margin, x, y + 3 * node_radius + margin)
                painter.drawText(x + margin / 2, y + node_radius + margin / 4, 2 * node_radius, 2 * node_radius, Qt.AlignCenter, "→")
            x += margin
            current_node = current_node.next


# Función principal para ejecutar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
