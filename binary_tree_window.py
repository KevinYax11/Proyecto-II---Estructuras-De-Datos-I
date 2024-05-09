from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QFont, QPixmap
from PyQt6.QtWidgets import QMainWindow, QGridLayout, QPushButton, QHBoxLayout, QVBoxLayout,\
    QWidget, QToolBar, QLineEdit, QLabel, QFileDialog, QScrollArea
from graphviz import Digraph
from binary_tree import BinaryTree
from communicate import Communicate
from save_window import SaveWindow
import os
os.environ['PATH'] += os.pathsep + 'D:/Graphviz/bin/'


class BinaryTreeWindow(QMainWindow):
    def __init__(self, communicate: Communicate):
        super().__init__()
        self.new_win = None
        self.dot = Digraph()
        self.dot2 = Digraph()
        self.max = 0
        self.communicate = communicate
        self.setFixedSize(650, 300)
        self.setWindowTitle('Arbol binario')
        self.tree = BinaryTree()

        # variables para los layouts
        self.main_layout = QVBoxLayout()
        self.btn_layout = QGridLayout()
        self.stack_layout = QHBoxLayout()
        self.response_layout = QHBoxLayout()

        # variables para los widgets
        self.main_widget = QWidget()
        self.stack_widget = QWidget()

        # variables para los botones
        self.insert_left_btn = QPushButton('Insertar a la izquierda')
        self.insert_left_btn.clicked.connect(self.insert_left)
        self.insert_right_btn = QPushButton('Insertar a la derecha')
        self.insert_right_btn.clicked.connect(self.insert_right)
        self.search_btn = QPushButton('Buscar dato')
        self.search_btn.clicked.connect(self.search)

        # variables para el textbox y labels
        self.text_box = QLineEdit()
        self.ref_text = QLineEdit()
        self.label = QLabel()
        self.label2 = QLabel()
        self.ref_label = QLabel('Ingrese la referencia para ingresar el dato')

        # variables para la barra de herramientas
        toolbar = QToolBar('binary_tree toolbar')
        toolbar.setStyleSheet('background-color: gray')
        self.addToolBar(toolbar)

        # variables para los botones de la barra de tareas
        # boton para la volver al menu principal
        button_action1 = QAction("Menu principal", self)
        button_action1.setFont(QFont('Comic Sans MS', 9))
        button_action1.setStatusTip("Regresar a la pagina principal")
        button_action1.triggered.connect(self.main_menu)
        toolbar.addAction(button_action1)

        # boton para guardar la lista
        button_action2 = QAction("Guardar arbol", self)
        button_action2.setFont(QFont('Comic Sans MS', 9))
        button_action2.setStatusTip("Guardar el arbol actual")
        button_action2.triggered.connect(self.save)
        toolbar.addAction(button_action2)

        # boton para cargar una lista
        button_action3 = QAction("Cargar arbol", self)
        button_action3.setFont(QFont('Comic Sans MS', 9))
        button_action3.setStatusTip("Carga un arbol previo")
        button_action3.triggered.connect(self.load)
        toolbar.addAction(button_action3)

        # variables para el scrollbar
        self.scroll = QScrollArea()

        # Propiedades del scrollbar
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.stack_widget)

        # configuracion de layouts
        self.btn_layout.addWidget(self.text_box, 0, 0)
        self.btn_layout.addWidget(self.ref_label, 0, 1)
        self.btn_layout.addWidget(self.ref_text, 0, 2)
        self.btn_layout.addWidget(self.insert_left_btn, 1, 0)
        self.btn_layout.addWidget(self.insert_right_btn, 1, 1)
        self.btn_layout.addWidget(self.search_btn, 1, 2)

        self.stack_widget.setLayout(self.stack_layout)

        self.main_layout.addLayout(self.btn_layout)
        self.main_layout.addWidget(self.scroll)
        self.main_layout.addLayout(self.response_layout)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

    # metodo para volver a la pagina principal
    def main_menu(self):
        self.communicate.verify_code.emit()
        self.close()

    # metodo para insertar datos
    def insert_left(self):
        if self.ref_text.text() != '':
            self.tree.insert_left(self.text_box.text(), self.ref_text.text())
        else:
            self.tree.insert_left(self.text_box.text(), None)
        self.transversal()

    def insert_right(self):
        if self.ref_text.text() != '':
            self.tree.insert_right(self.text_box.text(), self.ref_text.text())
        else:
            self.tree.insert_right(self.text_box.text(), None)
        self.transversal()

    # metodo para mostrar el arbol
    def transversal(self, subtree=None):
        self.dot.clear(True)
        for i in reversed(range(self.stack_layout.count())):
            self.stack_layout.itemAt(i).widget().deleteLater()

        for i in range(self.tree.size):
            data = self.tree.preorder().split(sep='=')[i]
            if data != subtree:
                if data != '-':
                    self.dot.node(f'{data}', data)
            else:
                if data != '-':
                    self.dot.node(f'{data}', data, style='filled', fillcolor='green')

        current = self.tree.preorder().split(sep='=')
        self.max = 0
        for i in current:
            if i != '-':
                data = self.tree.search_node(i, self.tree.root, None)
                if self.max != 0:
                    self.dot.edge(f'{data.split(sep="=")[1]}', f'{data.split(sep="=")[0]}')
                self.max += 1

        imagen = self.dot.render('structure_image', format='png', directory='estructuras/')
        label = QLabel(self)
        pixmap = QPixmap(imagen)
        label.setPixmap(pixmap)
        self.stack_layout.addWidget(label)

    # metodo de busqueda
    def search(self):
        data = self.tree.search_node(self.text_box.text(), self.tree.root, None)
        self.dot2.node('search_node', data.split(sep='=')[0])
        imagen = self.dot2.render('search_image', format='png', directory='estructuras/')
        self.dot.clear(True)
        if data != 'No se encontro el dato solicitado':
            self.transversal(data.split(sep='=')[0])
        pixmap = QPixmap(imagen)
        self.label.setPixmap(pixmap)
        self.response_layout.addWidget(self.label)
        self.main_layout.addLayout(self.response_layout)

    # metodo para cargar un arbol previo
    def load(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog_succesful = dialog.exec()
        if dialog_succesful:
            file_location = dialog.selectedFiles()[0]
            with open(file_location, 'rb') as file:
                text1 = str(file.read())
                binary_tree = text1.split(sep="'")[1]
                file.close()
                if binary_tree.split(sep='=')[1] == 'binary_tree':
                    size = binary_tree.split(sep='=')[0]
                    for i in reversed(range(int(size))):
                        if i != 0:
                            pass
                    self.transversal()
                    self.label.setText('Arbol cargado con exito')
                    self.main_layout.addWidget(self.label)
                else:
                    self.label.setText('La estructura seleccionada no es un arbol binario')
                    self.main_layout.addWidget(self.label)

    def save(self):
        self.new_win = SaveWindow(self.tree.size + 2, 'binary_tree', self.tree.transversal())
        self.new_win.show()
