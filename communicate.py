from PyQt6.QtCore import QObject, pyqtSignal


class Communicate(QObject):
    verify_code = pyqtSignal()
