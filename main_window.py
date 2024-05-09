from PyQt6.QtWidgets import QMainWindow, QLabel, QGridLayout, QPushButton, QVBoxLayout, QWidget
from stack_window import StackWindow
from communicate import Communicate
from queue_window import QueueWindow
from simply_list_window import SimplyListWindow
from doubly_list_window import DoublyListWindow
from circular_list_window import CircularListWindow
from doubly_circular_list_window import DoublyCircularListWindow
from binary_tree_window import BinaryTreeWindow
from binary_search_tree_window import BinarySearchTreeWindow


communicate = Communicate()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Menu principal')
        self.setFixedWidth(400)
        self.new_win = None

        # variables para los labels
        self.label1 = QLabel('Bienvenido')
        self.label2 = QLabel('Seleccione la estructura de datos que desea:')
        # variables para los botones de cada estructura de datos
        self.btn1 = QPushButton('Pila')
        self.btn1.clicked.connect(self.stack)
        self.btn2 = QPushButton('Cola')
        self.btn2.clicked.connect(self.queue)
        self.btn3 = QPushButton('Lista simplemente ligada')
        self.btn3.clicked.connect(self.simply_list)
        self.btn4 = QPushButton('Lista doblemente enlazada')
        self.btn4.clicked.connect(self.double_list)
        self.btn5 = QPushButton('Lista circular')
        self.btn5.clicked.connect(self.circular_list)
        self.btn6 = QPushButton('Lista circular doble')
        self.btn6.clicked.connect(self.double_circular_list)
        self.btn7 = QPushButton('Arbol binario')
        self.btn7.clicked.connect(self.binary_tree)
        self.btn8 = QPushButton('Arbol de busqueda')
        self.btn8.clicked.connect(self.search_tree)

        # variables para los layout
        self.main_layout = QVBoxLayout()
        self.layout1 = QGridLayout()

        # configuracion de layouts
        # layout de botones
        self.layout1.addWidget(self.btn1, 0, 0)
        self.layout1.addWidget(self.btn2, 1, 0)
        self.layout1.addWidget(self.btn3, 2, 0)
        self.layout1.addWidget(self.btn4, 3, 0)
        self.layout1.addWidget(self.btn5, 0, 1)
        self.layout1.addWidget(self.btn6, 1, 1)
        self.layout1.addWidget(self.btn7, 2, 1)
        self.layout1.addWidget(self.btn8, 3, 1)

        # layout principal
        self.main_layout.addWidget(self.label1)
        self.main_layout.addWidget(self.label2)
        self.main_layout.addLayout(self.layout1)

        # variables para el widget principal
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        
        # funcionamiento para el communicate
        communicate.verify_code.connect(self.open)

    # metodo para volver a abrir la pagina principal
    def open(self):
        self.show()

    # metodo para abrir la pagina de la pila
    def stack(self):
        self.new_win = StackWindow(communicate)
        self.new_win.show()
        self.close()

    # metodo para abrir la pagina de la cola
    def queue(self):
        self.new_win = QueueWindow(communicate)
        self.new_win.show()
        self.close()

    # metodo para abrir la pagina de la lista simple
    def simply_list(self):
        self.new_win = SimplyListWindow(communicate)
        self.new_win.show()
        self.close()

    # metodo para abrir la pagina de la lista doble
    def double_list(self):
        self.new_win = DoublyListWindow(communicate)
        self.new_win.show()
        self.close()

    # metodo para abrir la pagina de la lista circular
    def circular_list(self):
        self.new_win = CircularListWindow(communicate)
        self.new_win.show()
        self.close()

    # metodo para abrir la pagina de la lista circular doble
    def double_circular_list(self):
        self.new_win = DoublyCircularListWindow(communicate)
        self.new_win.show()
        self.close()

    # metodo para abrir la pagina del arbol binario
    def binary_tree(self):
        self.new_win = BinaryTreeWindow(communicate)
        self.new_win.show()
        self.close()

    # metodo para abrir la pagina del arbol de busqueda
    def search_tree(self):
        self.new_win = BinarySearchTreeWindow(communicate)
        self.new_win.show()
        self.close()
