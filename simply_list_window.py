from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QFont, QPixmap
from PyQt6.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QToolBar, QLineEdit, QLabel, \
    QFileDialog, QScrollArea
from graphviz import Digraph
from simply_linked_list import SimplyLinkedList
from communicate import Communicate
from save_window import SaveWindow
import os
os.environ['PATH'] += os.pathsep + 'D:/Graphviz/bin/'


class SimplyListWindow(QMainWindow):
    def __init__(self, communicate: Communicate):
        super().__init__()
        self.new_win = None
        self.dot = Digraph()
        self.dot2 = Digraph()
        self.max = 0
        self.communicate = communicate
        self.setFixedSize(650, 300)
        self.setWindowTitle('Lista simple')
        self.list = SimplyLinkedList()

        # variables para los layouts
        self.main_layout = QVBoxLayout()
        self.btn_layout = QHBoxLayout()
        self.stack_layout = QHBoxLayout()
        self.response_layout = QHBoxLayout()

        # variables para los widgets
        self.main_widget = QWidget()
        self.stack_widget = QWidget()

        # variables para los botones
        self.insert_head_btn = QPushButton('Insertar en la cabeza')
        self.insert_head_btn.clicked.connect(self.insert_head)
        self.delete_head_btn = QPushButton('Eliminar en la cabeza')
        self.delete_head_btn.clicked.connect(self.delete_head)
        self.insert_tail_btn = QPushButton('Insertar en la cola')
        self.insert_tail_btn.clicked.connect(self.insert_tail)
        self.delete_tail_btn = QPushButton('Eliminar en la cola')
        self.delete_tail_btn.clicked.connect(self.delete_tail)
        self.search_btn = QPushButton('Buscar dato')
        self.search_btn.clicked.connect(self.search)

        # variables para el textbox y labels
        self.text_box = QLineEdit()
        self.label = QLabel()
        self.label2 = QLabel()

        # variables para la barra de herramientas
        toolbar = QToolBar('simply_list toolbar')
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
        button_action2 = QAction("Guardar lista", self)
        button_action2.setFont(QFont('Comic Sans MS', 9))
        button_action2.setStatusTip("Guardar la lista actual")
        button_action2.triggered.connect(self.save)
        toolbar.addAction(button_action2)

        # boton para cargar una lista
        button_action3 = QAction("Cargar lista", self)
        button_action3.setFont(QFont('Comic Sans MS', 9))
        button_action3.setStatusTip("Carga una lista previa")
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
        self.btn_layout.addWidget(self.text_box)
        self.btn_layout.addWidget(self.insert_head_btn)
        self.btn_layout.addWidget(self.insert_tail_btn)
        self.btn_layout.addWidget(self.delete_head_btn)
        self.btn_layout.addWidget(self.delete_tail_btn)
        self.btn_layout.addWidget(self.search_btn)

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
    def insert_head(self):
        self.list.unshift(self.text_box.text())
        self.transversal()

    def insert_tail(self):
        self.list.appen(self.text_box.text())
        self.transversal()

    # metodo para eliminar datos
    def delete_head(self):
        delete = self.list.shift()
        self.label.setText(delete)
        self.response_layout.addWidget(self.label)
        if self.max != 0:
            self.max -= 1
            self.dot.clear(True)
            self.transversal()

    def delete_tail(self):
        delete = self.list.pop()
        self.label.setText(delete)
        self.response_layout.addWidget(self.label)
        if self.max != 0:
            self.max -= 1
            self.dot.clear(True)
            self.transversal()

    # metodo para mostrar la lista
    def transversal(self, pos=-1):
        self.dot.clear(True)
        for i in reversed(range(self.stack_layout.count())):
            self.stack_layout.itemAt(i).widget().deleteLater()

        for i in range(self.list.size):
            if i != pos:
                self.dot.node(f'node{i}', self.list.transversal().split(sep='=')[i])
            else:
                self.dot.node(f'node{i}', self.list.transversal().split(sep='=')[i],
                              style='filled', fillcolor='green')

        self.max = 0
        while self.max != self.list.size:
            if self.max != 0:
                self.dot.edge(f'node{self.max-1}', f'node{self.max}', constraint='false')
            self.max += 1

        imagen = self.dot.render('structure_image', format='png', directory='estructuras/')
        label = QLabel(self)
        pixmap = QPixmap(imagen)
        label.setPixmap(pixmap)
        self.stack_layout.addWidget(label)

    # metodo de busqueda
    def search(self):
        data = self.list.find_by(self.text_box.text())
        self.dot2.node('search_node', data.split(sep='=')[0])
        imagen = self.dot2.render('search_image', format='png', directory='estructuras/')
        self.dot.clear(True)
        if data != 'No se encontro el dato solicitado':
            self.transversal(int(data.split(sep='=')[1]))
        pixmap = QPixmap(imagen)
        self.label.setPixmap(pixmap)
        self.response_layout.addWidget(self.label)
        self.main_layout.addLayout(self.response_layout)

    # metodo para cargar una lista previa
    def load(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog_succesful = dialog.exec()
        if dialog_succesful:
            file_location = dialog.selectedFiles()[0]
            with open(file_location, 'rb') as file:
                text1 = str(file.read())
                simply_list = text1.split(sep="'")[1]
                file.close()
                if simply_list.split(sep='=')[1] == 'simply_list':
                    size = simply_list.split(sep='=')[0]
                    for i in reversed(range(int(size))):
                        if i != 0 and i != 1:
                            self.list.unshift(simply_list.split(sep='=')[i])
                    self.transversal()
                    self.label.setText('Lista cargada con exito')
                    self.main_layout.addWidget(self.label)
                else:
                    self.label.setText('La estructura seleccionada no es una lista')
                    self.main_layout.addWidget(self.label)

    def save(self):
        self.new_win = SaveWindow(self.list.size + 2, 'simply_list', self.list.transversal())
        self.new_win.show()
