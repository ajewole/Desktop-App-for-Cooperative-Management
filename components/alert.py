from ui.alert_ui import Ui_AlertDialog
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt

class Alert(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AlertDialog()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)