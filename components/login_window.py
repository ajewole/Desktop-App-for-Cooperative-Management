from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import Qt, QPoint, pyqtSlot, QTimer
from PyQt5.QtGui import QMouseEvent, QIcon, QPixmap
from ui.login_ui import Ui_Form
import sys, hashlib
sys.path.insert(0, 'C:/Python Apps/FOPAJ/components')
import main_window
from users import User_DB
from alert import Alert
from message import MsgBox

class LoginWindow(QWidget):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.db = User_DB()

        self._startPos = None
        self._endPos = None
        self._tracking = False


        self.ui.exitBtn.clicked.connect(self.exit_login)
        self.ui.loginBtn.clicked.connect(self.login)

        # Hide the frame and the background of the app
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
    
    def login(self):
        username = self.ui.usernameTxt.text().strip()
        password = self.ui.passwordTxt.text().strip()
        password = password + "#*129078"
        pwd = hashlib.sha256(password.encode()).hexdigest()
        user = self.db.get_login_user((username, pwd))
        self.alert = Alert()
        self.alert.ui.messageLbl.setStyleSheet("color: #ff0000")
        self.alert.ui.OKBtn.clicked.connect(self.alert.close)
        QTimer.singleShot(1500, self.alert.close)
        # if username == "" or password == "":
        #     self.alert.ui.messageLbl.setText("Username and Password cannot be empty")            
        #     self.alert.exec_()
        # elif user == {}:
        #     self.alert.ui.messageLbl.setText("Username or Password is not correct")            
        #     self.alert.exec_()
        # else:
        main_win = main_window.MainWindow(user)
        main_win.show()
        self.close()

    def exit_login(self):
        self.msgbox = MsgBox()
        self.msgbox.ui.messageTitle.setText("Exit App?")
        self.msgbox.ui.label.setText("Are you sure you want to exit this application?")
        self.msgbox.ui.messageYesBtn.clicked.connect(lambda: self.exit_finally())
        self.msgbox.ui.messageNoBtn.clicked.connect(lambda: self.msgbox.close())
        self.msgbox.exec_()
    # TODO: make the mouse movable after the window frame

    def exit_finally(self):
        self.msgbox.close()
        self.close()
    
    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        if self._tracking:
            self._endPos = a0.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        if a0.button() == Qt.LeftButton:
            self._startPos = QPoint(a0.x(), a0.y())
            self._tracking = True

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        if a0.button() == Qt.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None