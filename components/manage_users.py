from functools import partial
from PyQt5.QtWidgets import QWidget, QMessageBox, QMainWindow, QLabel, QLineEdit, \
     QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QVBoxLayout, QGridLayout, \
     QHeaderView, QAbstractItemView, QFileDialog, QDialog
from PyQt5.QtCore import Qt, QPoint, pyqtSlot
from PyQt5.QtGui import QMouseEvent, QIcon, QPixmap
import sys
sys.path.insert(0, 'C:/Python Apps/FOPAJ/data')
from data.users import User_DB
from message import MsgBox
from ui.add_user_ui import Ui_Dialog
import random, datetime
import hashlib

class ManageUsers(QMainWindow):
    def __init__(self):
        super().__init__()  
        self.db = User_DB()     

    def loadUsersTable(self, ui):
        self.ui = ui
        self.ui.stackedWidget.setCurrentIndex(6)
        self.ui.searchUserBtn.clicked.connect(self.search_users)
        self.ui.searchUserBtn.setStyleSheet("QPushButton::hover{background-color: #cce0ff;}")
        self.ui.searchUserTxt.textChanged.connect(self.search_users)
        self.ui.searchUserTxt.returnPressed.connect(self.search_users)
        self.ui.searchUserTxt.setClearButtonEnabled(True)
        self.ui.addUserBtn.clicked.connect(self.initialise_add_user)
        # self.ui.searchUserTxt.setPlaceholderText('Type search query and press enter')
        self.users = self.db.get_users()
        self.load_table(self.users)
    
    def load_table(self, users):
        # print(transactions)
        row = 0
        table = self.ui.usersListTable
        table.setObjectName("usersListTable")
        table.setRowCount(len(users))
        table.setColumnCount(8)
        table.setHorizontalHeaderLabels(["S/N", "UserID", "Full Name", "Designation", "Username", "Role", "", ""])
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.doubleClicked.connect(lambda: self.handle_table_dbl_click(table, self.ui))  
        table.setColumnHidden(7, True)  
     
        header = table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignLeft)
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setStretchLastSection(False)  
        vert = table.verticalHeader()   
        vert.setSectionResizeMode(QHeaderView.ResizeToContents)   

        for user in users:
            num = row + 1
            table.setItem(row, 0, QTableWidgetItem(str(num)))
            table.setItem(row, 1, QTableWidgetItem(user['userID']))
            table.setItem(row, 2, QTableWidgetItem(user['fullname']))
            table.setItem(row, 3, QTableWidgetItem(user['designation']))
            table.setItem(row, 4, QTableWidgetItem(user['username']))
            table.setItem(row, 5, QTableWidgetItem(user['role']))
            edit_button = QPushButton()
            delete_button = QPushButton()
            edit_button.setToolTip("Edit Details")
            delete_button.setToolTip("Remove User")
            edit_button.setIcon(QIcon('./static/icon/blue/edit.svg'))
            delete_button.setIcon(QIcon('./static/icon/red/trash-2.svg'))
            table.setStyleSheet("QPushButton::hover{background-color: #cce0ff;}")
            edit_button.clicked.connect(partial(self.initialise_edit_user, user['user_id']))
            delete_button.clicked.connect(partial(self.start_delete_user, (user['user_id'],)))
            hbox = QHBoxLayout(table)
            widg = QWidget()
            hbox.addWidget(edit_button)
            hbox.addWidget(delete_button)
            widg.setLayout(hbox)
            table.setCellWidget(row, 6, widg)
            table.setItem(row, 7, QTableWidgetItem(str(user['user_id'])))
            row += 1
        
    def handle_table_dbl_click(self, table, ui):
        index = table.selectionModel().currentIndex()
        value = index.sibling(index.row(), 7).data()
        self.initialise_edit_user(value)
    
    def search_users(self):
        searchText = (self.ui.searchUserTxt.text()).lower()
        if searchText == "":
            self.load_table(self.users)
        else:
            new_users = [user for user in self.users if searchText in (user['userID']).lower() or \
                searchText in (user['designation']).lower() or searchText in (user['fullname']).lower() or \
                searchText in (user['username']).lower() or searchText in (user['role']).lower()]
            if new_users == []:
                self.load_table(self.users)
            else:
                self.load_table(new_users)
    
    def initialise_add_user(self):
        self.dialogAdd = QDialog()
        self.addUserDialog = Ui_Dialog()
        self.addUserDialog.setupUi(self.dialogAdd)
        self.addUserDialog.cancelBtn.clicked.connect(self.dialogAdd.close)
        self.addUserDialog.addUserBtn.clicked.connect(self.add_user)
        self.addUserDialog.resetBtn.clicked.connect(self.reset_add_form)
        randNo = random.randint(1000, 10000)
        self.addUserDialog.userIDTxt.setText('FOPAJ/ST.' + str(randNo))
        self.addUserDialog.userIDTxt.setDisabled(True)
        date_enrolled = datetime.datetime.now().strftime("%d/%m/%Y")
        date_last_modified = date_enrolled        
        self.addUserDialog.dateEnrolledTxt.setText(str(date_enrolled))
        self.addUserDialog.dateEnrolledTxt.setDisabled(True)
        self.addUserDialog.dateUpdatedTxt.setText(date_last_modified)
        self.addUserDialog.dateUpdatedTxt.setDisabled(True)
        self.addUserDialog.errorLbl.setVisible(False)
        self.addUserDialog.roleCombo.addItems(['Operator', 'Admin'])
        self.addUserDialog.roleCombo.setCurrentText('Operator')
        self.dialogAdd.exec_()
    
    def add_user(self):
        userID = self.addUserDialog.userIDTxt.text().strip()
        surname = self.addUserDialog.surnameTxt.text().strip()
        firstname = self.addUserDialog.firstnameTxt.text().strip()
        othername = self.addUserDialog.othernameTxt.text().strip()
        fullname = surname + " " + firstname + " " + othername
        username = self.addUserDialog.usernameTxt.text().strip()
        password = self.addUserDialog.passwordTxt.text().strip()
        confirm_password = self.addUserDialog.confirmPasswordTxt.text().strip()
        designation = self.addUserDialog.designationTxt.text().strip()
        role = self.addUserDialog.roleCombo.currentText().strip()
        errorMessage = ""
        if surname == "" or firstname == "" or username == "" or password == "" or confirm_password == "" or othername == "":
            errorMessage += "Fill all the empty fields\n"
        if len(username) < 6:
            errorMessage += "Username cannot be less than six characters\n"
        if len(password) < 6:
            errorMessage += "Password length cannot be less than six characters\n"
        if password != confirm_password:
            errorMessage += "The passwords do not match"
        if errorMessage != "":
            self.addUserDialog.errorLbl.setVisible(True)
            self.addUserDialog.errorLbl.setText(errorMessage)
        else:
            self.addUserDialog.errorLbl.setVisible(False)
            # print(fullname, userID)
            date_enrolled = datetime.datetime.now()
            date_last_modified = date_enrolled    
            password = password + "#*129078"   
            pwd = hashlib.sha256(password.encode()).hexdigest()
            user_data = (userID, surname, firstname, othername, fullname, username, pwd, designation, role, \
                   date_enrolled, date_last_modified )
            self.db.add_user(user_data)
            self.loadUsersTable(self.ui)
            self.dialogAdd.close()

    
    def reset_add_form(self):
        for widg in self.addUserDialog.addUserFrame.findChildren(QLineEdit):
            widg.clear()
        randNo = random.randint(1000, 10000)
        self.addUserDialog.userIDTxt.setText('FOPAJ/ST.' + str(randNo)) 
        date_enrolled = datetime.datetime.now().strftime("%d/%m/%Y")
        date_last_modified = date_enrolled        
        self.addUserDialog.dateEnrolledTxt.setText(str(date_enrolled))
        self.addUserDialog.dateEnrolledTxt.setDisabled(True)
        self.addUserDialog.dateUpdatedTxt.setText(date_last_modified)
        self.addUserDialog.dateUpdatedTxt.setDisabled(True)
        self.addUserDialog.roleCombo.setCurrentText('Operator')          

    def initialise_edit_user(self, id):
        self.dialogEdit = QDialog()
        self.editUserDialog = Ui_Dialog()
        self.editUserDialog.setupUi(self.dialogEdit)
        self.editUserDialog.cancelBtn.clicked.connect(self.dialogEdit.close)
        self.editUserDialog.addUserBtn.clicked.connect(lambda: self.edit_user(id))
        self.editUserDialog.resetBtn.clicked.connect(self.reset_edit_form)
        self.editUserDialog.label.setText("Edit User")
        self.editUserDialog.addUserBtn.setText("Edit User")
        
        self.user = self.db.get_user((id,))
               
        self.editUserDialog.userIDTxt.setText(self.user['userID'])
        self.editUserDialog.userIDTxt.setDisabled(True)
        self.editUserDialog.surnameTxt.setText(self.user['surname'])
        self.editUserDialog.firstnameTxt.setText(self.user['firstname'])
        self.editUserDialog.othernameTxt.setText(self.user['othername'])
        self.editUserDialog.usernameTxt.setText(self.user['username'])
        self.editUserDialog.passwordTxt.setText(self.user['password'])
        self.init_password = self.editUserDialog.passwordTxt.text().strip()
        self.editUserDialog.confirmPasswordTxt.setText(self.user['password'])
        self.init_confirm_password = self.editUserDialog.passwordTxt.text().strip()
        self.editUserDialog.dateEnrolledTxt.setText(self.user['date_enrolled'])
        self.editUserDialog.dateEnrolledTxt.setDisabled(True)
        self.editUserDialog.dateUpdatedTxt.setText(self.user['date_last_modified'])
        self.editUserDialog.dateUpdatedTxt.setDisabled(True)
        self.editUserDialog.errorLbl.setVisible(False)
        self.editUserDialog.designationTxt.setText(self.user['designation'])
        self.editUserDialog.roleCombo.addItems(['Operator', 'Admin'])
        self.editUserDialog.roleCombo.setCurrentText(self.user['role'])
        self.dialogEdit.exec_()
        print(self.init_password)
        print(self.init_confirm_password)

    def edit_user(self, id):
        surname = self.editUserDialog.surnameTxt.text().strip()
        firstname = self.editUserDialog.firstnameTxt.text().strip()
        othername = self.editUserDialog.othernameTxt.text().strip()
        fullname = surname + " " + firstname + " " + othername
        username = self.editUserDialog.usernameTxt.text().strip()
        password = self.editUserDialog.passwordTxt.text().strip()
        confirm_password = self.editUserDialog.confirmPasswordTxt.text().strip()
        designation = self.editUserDialog.designationTxt.text().strip()
        role = self.editUserDialog.roleCombo.currentText().strip()
        errorMessage = ""
        if surname == "" or firstname == "" or username == "" or password == "" or confirm_password == "" or othername == "":
            errorMessage += "Fill all the empty fields\n"
        if len(username) < 6:
            errorMessage += "Username cannot be less than six characters\n"
        if len(password) < 6:
            errorMessage += "Password length cannot be less than six characters\n"
        if password != confirm_password:
            errorMessage += "The passwords do not match"
        if errorMessage != "":
            self.editUserDialog.errorLbl.setVisible(True)
            self.editUserDialog.errorLbl.setText(errorMessage)
        else:
            self.editUserDialog.errorLbl.setVisible(False)
            # print(fullname, userID)
            date_last_modified = datetime.datetime.now()
            if self.init_password != password:
                pwd = password + "#*129078"
                password = hashlib.sha256(pwd.encode()).hexdigest()
            user_data = (surname, firstname, othername, fullname, username, password, designation, role, date_last_modified, id)
            self.db.update_user(user_data)
            self.loadUsersTable(self.ui)
            self.dialogEdit.close()  
    
    def reset_edit_form(self):
        for widg in self.editUserDialog.addUserFrame.findChildren(QLineEdit):
            widg.clear()
        self.editUserDialog.userIDTxt.setText(self.user['userID']) 
        date_last_modified = datetime.datetime.now().strftime("%d/%m/%Y")     
        self.editUserDialog.dateEnrolledTxt.setText(self.user['date_enrolled'])
        self.editUserDialog.dateEnrolledTxt.setDisabled(True)
        self.editUserDialog.dateUpdatedTxt.setText(date_last_modified)
        self.editUserDialog.dateUpdatedTxt.setDisabled(True)
        self.editUserDialog.roleCombo.setCurrentText('Operator')  
    
    def start_delete_user(self, id):
        self.msgbox = MsgBox()
        self.msgbox.ui.label.setText("Are you sure you want to remove this user? All their records will be deleted!")
        self.msgbox.ui.messageTitle.setText("Remove User?")
        self.msgbox.ui.messageYesBtn.clicked.connect(lambda: self.delete_user(id))
        self.msgbox.ui.messageNoBtn.clicked.connect(lambda: self.msgbox.close())
        self.msgbox.exec_()
    
    def delete_user(self, id):
        self.db.remove_user(id)
        self.loadUsersTable(self.ui)
        self.msgbox.close()
    
    def search_users(self):
        searchText = (self.ui.searchUserTxt.text()).lower()
        if searchText == "":
            self.load_table(self.users)
        else:
            new_users = [user for user in self.users if searchText in (user['userID']).lower() or \
                searchText in (user['username']).lower() or searchText in (user['fullname']).lower() or \
                searchText in (user['designation']).lower() or searchText in (user['role']).lower()]
            if new_users == []:
                self.load_table(self.users)
            else:
                self.load_table(new_users)