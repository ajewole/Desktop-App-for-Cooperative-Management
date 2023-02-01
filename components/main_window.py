from PyQt5.QtWidgets import QWidget, QMessageBox, QMainWindow, QLabel, QLineEdit, \
     QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QVBoxLayout, QGridLayout, \
     QHeaderView, QAbstractItemView, QFileDialog, QDialog, QDesktopWidget
from PyQt5.QtCore import Qt, QPoint, pyqtSlot
from PyQt5.QtGui import QMouseEvent, QIcon, QPixmap
from ui.main_window_ui import Ui_MainWindow
from add_member import AddMember
from list_members import ListMembers
from member_transactions import MemberTransactions
from manage_users import ManageUsers
import sys
sys.path.insert(0, 'C:/Python Apps/FOPAJ/data')
from members import Member_DB
from monthly_transactions import Monthly_DB
from message import MsgBox
from functools import partial
import login_window 
from manage_settings import ManageSettings

class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.showMaximized()
        self.addMember = AddMember()
        self.listMembers = ListMembers()
        self.memberTransactions = MemberTransactions()       
        self.manageUsers = ManageUsers()    
        self.manageSettings = ManageSettings()   
        self.ui.memberTransTab.currentChanged.connect(self.memberTransactions.change_tab)
        # Initialise widgets
        self.dashboardBtn = self.ui.dashboardBtn
        self.membersBtn = self.ui.membersBtn
        self.loansSavingsBtn = self.ui.loansSavingsBtn
        self.usersBtn = self.ui.usersBtn
        self.reportsBtn = self.ui.reportsBtn
        self.syncDataBtn = self.ui.syncDataBtn
        self.settingsBtn = self.ui.settingsBtn
        self.pages = self.ui.stackedWidget
        self.resultFrame = self.ui.transFrame
        self.addMemberBtn = self.ui.addMemberBtn
        self.exitBtn = self.ui.exitBtn
        self.logOutBtn = self.ui.logOutBtn
        # Set initial page
        self.pages.setCurrentIndex(0)

        # Disable buttons for non-admin users
        # if user['role'] != 'Admin':
            # self.settingsBtn.setVisible(False)
            # self.usersBtn.setVisible(False)

        # Connect signals and slots
        self.dashboardBtn.toggled.connect(lambda: self.change_pages(self.dashboardBtn))
        self.dashboardBtn.clicked.connect(lambda: self.load_dashboard())
        self.membersBtn.toggled.connect(lambda: self.change_pages(self.membersBtn))
        self.loansSavingsBtn.toggled.connect(lambda: self.change_pages(self.loansSavingsBtn))
        self.usersBtn.toggled.connect(lambda: self.change_pages(self.usersBtn))
        self.reportsBtn.toggled.connect(lambda: self.change_pages(self.reportsBtn))
        self.syncDataBtn.toggled.connect(lambda: self.change_pages(self.syncDataBtn))
        self.settingsBtn.toggled.connect(lambda: self.change_pages(self.settingsBtn))
       
        self.addMemberBtn.clicked.connect(lambda: self.addMember.load_ui(self.ui))
        self.loansSavingsBtn.clicked.connect(lambda: self.memberTransactions.loadTransTable(self.ui, (self.members[0]['member_id'],)))
        self.membersBtn.clicked.connect(lambda: self.listMembers.loadMembersTable(self.ui))
        self.usersBtn.clicked.connect(lambda: self.manageUsers.loadUsersTable(self.ui))
        self.settingsBtn.clicked.connect(lambda: self.manageSettings.get_ui(self.ui))
        self.exitBtn.clicked.connect(lambda: self.exit_app())
        # self.logOutBtn.clicked.connect(self.log_out)
        self.ui.searchBtn.clicked.connect(lambda: self.search_trans())
        self.ui.searchBtn.setStyleSheet("QPushButton::hover{background-color: #cce0ff;}")
        self.ui.searchTxt.textChanged.connect(lambda: self.search_trans())
        self.ui.searchTxt.returnPressed.connect(lambda: self.search_trans())
        self.ui.searchTxt.setClearButtonEnabled(True)
        self.ui.searchTxt.setPlaceholderText('Type search query and press enter')

        self.get_data()
        self.loadLatestTransTable(self.transactions)

    def get_data(self):
        self.members = Member_DB().get_members()
        self.transactions = Monthly_DB().get_all_transactions()
        self.members_count = Member_DB().get_members_count()
        self.ui.lineEdit.setText(str(self.members_count))
        self.share_capital = Member_DB().get_total_share_capital()
        self.ui.lineEdit_11.setText('N' + str(self.share_capital))
        self.total_assets = Member_DB().get_total_assets()
        self.ui.lineEdit_12.setText('N' + str(self.total_assets))
        self.total_savings = Member_DB().get_total_savings()
        self.ui.lineEdit_13.setText('N' + str(self.total_savings))
        self.total_loan_balance = Member_DB().get_total_loan_balance()
        self.ui.lineEdit_14.setText('N' + str(self.total_loan_balance))
        self.total_xmas = Member_DB().get_total_xmas()
        self.ui.lineEdit_15.setText('N' + str(self.total_xmas))
        self.total_edu = Member_DB().get_total_edu()
        self.ui.lineEdit_16.setText('N' + str(self.total_edu))
        self.total_exit = Member_DB().get_total_exit()
        self.ui.lineEdit_17.setText('N' + str(self.total_exit))
    
    def loadLatestTransTable(self, transactions):
        # print(transactions)
        table = self.ui.latestTransTable
        table.setObjectName("transTable")
        table.setRowCount(len(transactions))
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Transaction ID", "Transaction Details", "Amount", "Member", "", ""])
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # table.doubleClicked.connect(lambda: HandleRefresh().handle_table_dbl_click(table))  
        table.setColumnHidden(5, True)  
     
        header = table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignLeft)
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setStretchLastSection(False)   
             

        row = 0
        for trans in transactions:
            table.setItem(row, 0, QTableWidgetItem(trans['transID']))
            table.setItem(row, 1, QTableWidgetItem(trans['type'] + ' for the month of ' + trans['month'] + ', ' + trans['year']))
            table.setItem(row, 2, QTableWidgetItem(str(trans['amount'])))
            table.setItem(row, 3, QTableWidgetItem(trans['fullname']))
            view_button = QPushButton()
            view_button.setIcon(QIcon('./static/icon/blue/edit.svg'))
            view_button.clicked.connect(partial(self.memberTransactions.loadTransTable, self.ui, (trans['member_id'],)))
            table.setStyleSheet("QPushButton::hover{background-color: #cce0ff;}")
            table.setCellWidget(row, 4, view_button)
            table.setItem(row, 5, QTableWidgetItem(str(trans['trans_id'])))
            row += 1
    
    def change_pages(self, btn):
        btn_text = btn.text().strip()
        if btn_text == self.dashboardBtn.text().strip():
            self.pages.setCurrentIndex(0)
        elif btn_text == self.membersBtn.text().strip():
            self.pages.setCurrentIndex(1)
        elif btn_text == self.loansSavingsBtn.text().strip():
            self.pages.setCurrentIndex(5)
        elif btn_text == self.usersBtn.text().strip():
            self.pages.setCurrentIndex(6)
        elif btn_text == self.settingsBtn.text().strip():
            self.pages.setCurrentIndex(7)
        else:
            self.pages.setCurrentIndex(0)
    
    def load_dashboard(self):
        self.pages.setCurrentIndex(0)
        self.get_data()
        self.loadLatestTransTable(self.transactions)
    
    @pyqtSlot()
    def on_logOutBtn_clicked(self):
        self.close()
        self.login = login_window.LoginWindow()
        qtRect = self.login.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRect.moveCenter(centerPoint)
        self.login.move(qtRect.topLeft())
        self.login.show()
        # login.show()
        # self.close()
    
    def exit_app(self):
        self.msgbox = MsgBox()
        self.msgbox.ui.messageTitle.setText("Exit App?")
        self.msgbox.ui.label.setText("Are you sure you want to exit this application?")
        self.msgbox.ui.messageYesBtn.clicked.connect(lambda: self.exit_finally())
        self.msgbox.ui.messageNoBtn.clicked.connect(lambda: self.msgbox.close())
        self.msgbox.exec_()
    
    def exit_finally(self):
        self.msgbox.close()
        self.close()
    
# class SearchTransaction():
    def search_trans(self):
        searchText = (self.ui.searchTxt.text()).lower()
        if searchText == "":
            self.loadLatestTransTable(self.transactions)
        else:
            new_trans = [trans for trans in self.transactions if searchText in (trans['transID']).lower() or \
                searchText in (str(trans['amount'])).lower() or searchText in (trans['year']).lower() or \
                searchText in (trans['month']).lower() or searchText in (trans['type']).lower() or \
                searchText in (trans['details']).lower() or searchText in (trans['fullname']).lower()]
            if new_trans == []:
                self.loadLatestTransTable(self.transactions)
            else:
                self.loadLatestTransTable(new_trans)
        

    


