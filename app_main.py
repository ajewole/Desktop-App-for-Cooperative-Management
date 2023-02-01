import sys 
from PyQt5.QtWidgets import QApplication, QDesktopWidget
from components.login_window import LoginWindow
from main_window import MainWindow

def setQss(file_path, obj):
    with open(file_path, 'r') as rf:
        style = rf.read()
        obj.setStyleSheet(style)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    setQss('./static/style.qss', app)
    window = LoginWindow()
    qtRect = window.frameGeometry()
    centerPoint = QDesktopWidget().availableGeometry().center()
    qtRect.moveCenter(centerPoint)
    window.move(qtRect.topLeft())
    window.show()
    sys.exit(app.exec())
