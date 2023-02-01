from functools import partial
from PyQt5.QtWidgets import QWidget, QMessageBox, QMainWindow, QLabel, QLineEdit, \
     QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QVBoxLayout, QGridLayout, \
     QHeaderView, QAbstractItemView, QFileDialog, QDialog
from PyQt5.QtCore import Qt, QPoint, pyqtSlot
from PyQt5.QtGui import QMouseEvent, QIcon, QPixmap
import sys
sys.path.insert(0, 'C:/Python Apps/FOPAJ/data')
from data.members import Member_DB
from view_member import ViewMember
from edit_member import EditMember
from member_transactions import MemberTransactions
from message import MsgBox

class ListMembers(QMainWindow):
    def __init__(self):
        super().__init__()        
        self.view_member = ViewMember()
        self.edit_member = EditMember()
        self.member_trans = MemberTransactions()
        self.db = Member_DB()

    def loadMembersTable(self, ui):
        self.ui = ui
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.searchMemberBtn.clicked.connect(self.search_members)
        self.ui.searchMemberBtn.setStyleSheet("QPushButton::hover{background-color: #cce0ff;}")
        self.ui.searchMemberTxt.textChanged.connect(self.restore_table)
        self.ui.searchMemberTxt.returnPressed.connect(self.search_members)
        self.ui.searchMemberTxt.setClearButtonEnabled(True)
        self.ui.searchMemberTxt.setPlaceholderText('Type search query and press enter')
        self.members = self.db.get_members()
        self.load_table(self.members)
    
    def load_table(self, members):
        # print(transactions)
        row = 0
        table = self.ui.membersListTable
        table.setObjectName("membersListTable")
        table.setRowCount(len(members))
        table.setColumnCount(8)
        table.setHorizontalHeaderLabels(["S/N", "MemberID", "Ledger No", "Full Name", "Department/Unit", "Phone Number", "", ""])
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.doubleClicked.connect(lambda: self.handle_table_dbl_click(table, self.ui))  
        table.setColumnHidden(7, True)  
     
        header = table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignLeft)
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setStretchLastSection(False)  
        vert = table.verticalHeader()   
        vert.setSectionResizeMode(QHeaderView.ResizeToContents)   

        for member in members:
            num = row + 1
            table.setItem(row, 0, QTableWidgetItem(str(num)))
            table.setItem(row, 1, QTableWidgetItem(member['memberID']))
            table.setItem(row, 2, QTableWidgetItem(member['ledger_no']))
            table.setItem(row, 3, QTableWidgetItem(member['fullname']))
            dept = member['dept']
            dept2 = dept[:20]
            table.setItem(row, 4, QTableWidgetItem(dept2))
            table.setItem(row, 5, QTableWidgetItem(member['phone_no']))
            view_button = QPushButton()
            view_button.setObjectName('view_button')
            edit_button = QPushButton()
            trans_button = QPushButton()
            delete_button = QPushButton()
            view_button.setToolTip("View Details")
            edit_button.setToolTip("Edit Details")
            trans_button.setToolTip("View Transactions")
            delete_button.setToolTip("Remove Member")
            view_button.setIcon(QIcon('./static/icon/black/eye.svg'))
            edit_button.setIcon(QIcon('./static/icon/blue/edit.svg'))
            trans_button.setIcon(QIcon('./static/icon/naira3.png'))
            delete_button.setIcon(QIcon('./static/icon/red/trash-2.svg'))
            table.setStyleSheet("QPushButton::hover{background-color: #cce0ff;}")
            view_button.clicked.connect(partial(self.view_member.get_ui, self.ui, member['member_id']))
            edit_button.clicked.connect(partial(self.edit_member.get_data, self.ui, member['member_id']))
            trans_button.clicked.connect(partial(self.member_trans.loadTransTable, self.ui, (member['member_id'],)))
            delete_button.clicked.connect(partial(self.start_delete_member, (member['member_id'],)))
            hbox = QHBoxLayout(table)
            widg = QWidget()
            hbox.addWidget(view_button)
            hbox.addWidget(edit_button)
            hbox.addWidget(trans_button)
            hbox.addWidget(delete_button)
            widg.setLayout(hbox)
            table.setCellWidget(row, 6, widg)
            table.setItem(row, 7, QTableWidgetItem(str(member['member_id'])))
            row += 1

    # Event handling double click of each member record/row  
    def handle_table_dbl_click(self, table, ui):
        index = table.selectionModel().currentIndex()
        value = index.sibling(index.row(), 7).data()
        self.view_member.get_ui(ui, value)
    
    def start_delete_member(self, id):
        self.msgbox = MsgBox()
        self.msgbox.ui.label.setText("Are you sure you want to remove this member? All their records and transactions will be deleted!")
        self.msgbox.ui.messageTitle.setText("Remove Member?")
        self.msgbox.ui.messageYesBtn.clicked.connect(lambda: self.delete_member(id))
        self.msgbox.ui.messageNoBtn.clicked.connect(self.msgbox.close)
        self.msgbox.exec_()
    
    def delete_member(self, id):
        self.db.remove_member(id)
        self.loadMembersTable(self.ui)
        self.msgbox.close()
        
    
    def search_members(self):
        searchText = (self.ui.searchMemberTxt.text()).lower()
        if searchText == "":
            self.load_table(self.members)
        else:
            new_members = [member for member in self.members if searchText in (member['memberID']).lower() or \
                searchText in (member['ledger_no']).lower() or searchText in (member['fullname']).lower() or \
                searchText in (member['dept']).lower() or searchText in (member['phone_no']).lower()]
            if new_members == []:
                self.load_table(self.members)
            else:
                self.load_table(new_members)
    
    def restore_table(self):
        searchText = (self.ui.searchMemberTxt.text()).lower()
        if searchText == "":
            self.load_table(self.members)

