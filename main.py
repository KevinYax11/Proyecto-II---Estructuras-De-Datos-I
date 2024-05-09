from PyQt6.QtWidgets import QApplication
import sys
from main_window import MainWindow


app = QApplication(sys.argv)
win = MainWindow()

win.show()
app.exec()
