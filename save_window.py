from PyQt6.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QLineEdit, QLabel


class SaveWindow(QMainWindow):
    def __init__(self, size, tipe, data):
        super().__init__()
        self.size = size
        self.tipe = tipe
        self.data = data
        self.setWindowTitle('Guardar')

        # variables para los layouts
        self.main_layout = QVBoxLayout()
        self.btn_layout = QHBoxLayout()

        # variables para el textbox y label
        self.text_box = QLineEdit()
        self.label = QLabel()

        # variables para los widgets
        self.main_widget = QWidget()

        # variables para los botones
        self.save_btn = QPushButton('Guardar')
        self.save_btn.clicked.connect(self.save)

        # configuracion de layouts
        self.btn_layout.addWidget(self.text_box)
        self.btn_layout.addWidget(self.save_btn)

        self.main_layout.addLayout(self.btn_layout)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

    # metodo para guardar la estructura actual
    def save(self):
        name = self.text_box.text()
        file = open(f'estructuras guardadas/{name}.txt', 'w')
        file.write(f'{self.size}={self.tipe}={self.data}')
        file.close()
        self.label.setText('Estructura guardada con exito')
        self.main_layout.addWidget(self.label)
