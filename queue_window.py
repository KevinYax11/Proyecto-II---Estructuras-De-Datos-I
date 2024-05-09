from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QFont, QPixmap
from PyQt6.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QToolBar, QLineEdit, QLabel, \
    QFileDialog, QScrollArea
from graphviz import Digraph
from queue import Queue
from communicate import Communicate
from save_window import SaveWindow
import os
os.environ['PATH'] += os.pathsep + 'D:/Graphviz/bin/'


class QueueWindow(QMainWindow):
    def __init__(self, communicate: Communicate):
        super().__init__()
        self.new_win = None
        self.dot = Digraph()
        self.dot2 = Digraph()
        self.max = 0
        self.communicate = communicate
        self.setFixedSize(400, 300)
        self.setWindowTitle('Cola')
        self.queue = Queue()

        # variables para los layouts
        self.main_layout = QVBoxLayout()
        self.btn_layout = QHBoxLayout()
        self.stack_layout = QHBoxLayout()
        self.response_layout = QHBoxLayout()

        # variables para los widgets
        self.main_widget = QWidget()
        self.stack_widget = QWidget()

        # variables para los botones
        self.insert_btn = QPushButton('Insertar')
        self.insert_btn.clicked.connect(self.insert)
        self.delete_btn = QPushButton('Eliminar')
        self.delete_btn.clicked.connect(self.delete)
        self.search_btn = QPushButton('Buscar dato')
        self.search_btn.clicked.connect(self.search)

        # variables para el textbox y labels
        self.text_box = QLineEdit()
        self.label = QLabel()
        self.label2 = QLabel()

        # variables para la barra de herramientas
        toolbar = QToolBar('queue toolbar')
        toolbar.setStyleSheet('background-color: gray')
        self.addToolBar(toolbar)

        # variables para los botones de la barra de tareas
        # boton para la volver al menu principal
        button_action1 = QAction("Menu principal", self)
        button_action1.setFont(QFont('Comic Sans MS', 9))
        button_action1.setStatusTip("Regresar a la pagina principal")
        button_action1.triggered.connect(self.main_menu)
        toolbar.addAction(button_action1)

        # boton para guardar la cola
        button_action2 = QAction("Guardar cola", self)
        button_action2.setFont(QFont('Comic Sans MS', 9))
        button_action2.setStatusTip("Guardar la cola actual")
        button_action2.triggered.connect(self.save)
        toolbar.addAction(button_action2)

        # boton para cargar una cola
        button_action3 = QAction("Cargar cola", self)
        button_action3.setFont(QFont('Comic Sans MS', 9))
        button_action3.setStatusTip("Carga una cola previa")
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
        self.btn_layout.addWidget(self.insert_btn)
        self.btn_layout.addWidget(self.delete_btn)
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
    def insert(self):
        self.queue.insert(self.text_box.text())
        self.transversal()

    # metodo para eliminar datos
    def delete(self):
        delete = self.queue.delete()
        self.label.setText(delete)
        self.response_layout.addWidget(self.label)
        if self.max != 0:
            self.max -= 1
            self.dot.clear(True)
            self.transversal()

    # metodo para mostrar la cola
    def transversal(self, pos=-1):
        self.dot.clear(True)
        for i in reversed(range(self.stack_layout.count())):
            self.stack_layout.itemAt(i).widget().deleteLater()

        for i in range(self.queue.size):
            if i != pos:
                self.dot.node(f'node{i}', self.queue.transversal().split(sep='=')[i])
            else:
                self.dot.node(f'node{i}', self.queue.transversal().split(sep='=')[i],
                              style='filled', fillcolor='green')

        self.max = 0
        while self.max != self.queue.size:
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
        data = self.queue.find_by(self.text_box.text())
        self.dot2.node('search_node', data.split(sep='=')[0])
        imagen = self.dot2.render('search_image', format='png', directory='estructuras/')
        self.dot.clear(True)
        if data != 'No se encontro el dato solicitado':
            self.transversal(int(data.split(sep='=')[1]))
        pixmap = QPixmap(imagen)
        self.label.setPixmap(pixmap)
        self.response_layout.addWidget(self.label)
        self.main_layout.addLayout(self.response_layout)

    # metodo para cargar una cola previa
    def load(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog_succesful = dialog.exec()
        if dialog_succesful:
            file_location = dialog.selectedFiles()[0]
            with open(file_location, 'rb') as file:
                text1 = str(file.read())
                queue = text1.split(sep="'")[1]
                file.close()
                if queue.split(sep='=')[1] == 'queue':
                    size = queue.split(sep='=')[0]
                    for i in reversed(range(int(size))):
                        if i != 0 and i != 1:
                            self.queue.insert(queue.split(sep='=')[i])
                    self.transversal()
                    self.label.setText('Cola cargada con exito')
                    self.main_layout.addWidget(self.label)
                else:
                    self.label.setText('La estructura seleccionada no es una cola')
                    self.main_layout.addWidget(self.label)

    def save(self):
        self.new_win = SaveWindow(self.queue.size + 2, 'queue', self.queue.transversal())
        self.new_win.show()
