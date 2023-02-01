
from ui.add_savings_ui import Ui_Dialog
from PyQt5.QtWidgets import QDialog

class CommonDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
    