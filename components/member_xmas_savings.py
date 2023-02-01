from functools import partialmethod, partial
from PyQt5.QtWidgets import QWidget, QMessageBox, QMainWindow, QLabel, QLineEdit, \
     QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QVBoxLayout, QGridLayout, \
     QHeaderView, QAbstractItemView, QFileDialog, QDialog
from PyQt5.QtCore import Qt, QPoint, pyqtSlot
from PyQt5.QtGui import QMouseEvent, QIcon, QPixmap, QFont
import sys, random, datetime
sys.path.insert(0, 'C:/Python Apps/FOPAJ/data')
sys.path.insert(1, 'C:/Python Apps/FOPAJ/ui')
from xmas_savings import Xmas_DB
from data.members import Member_DB
from ui.add_savings_ui import Ui_Dialog
from utils import Utils
from message import MsgBox

class AddXmasDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.dialog = Ui_Dialog()
        self.dialog.setupUi(self)
        self.member_db = Member_DB()
        self.xmas_db = Xmas_DB()        
        self.years = Utils().generate_years()
        self.dialog.errorLbl.setVisible(False)  
        
    def initialise_add_xmas(self, id):
        self.dialog.savingsTypeCombo.clear()
        self.dialog.savingsTypeCombo.addItems(['Christmas Savings'])
        # Initialise widgets
        self.memberid = id
        self.member = self.member_db.get_member(self.memberid)
        today = datetime.date.today()
        current_year = today.strftime("%Y")
        current_month = today.strftime("%B")
        self.dialog.label.setText('Add Christmas Savings for ' + self.member['fullname'] + '?')
        self.dialog.label_8.setText('Transaction Type')
        self.dialog.yearCombo.addItems(self.years)
        self.dialog.yearCombo.addItems(self.years)
        self.dialog.monthCombo.setCurrentText(current_month)
        self.dialog.yearCombo.setCurrentText(current_year)
        self.dialog.addSavingsBtn.setText("Add Christmas Savings")    
        self.dialog.errorLbl.setWordWrap(True)
        self.dialog.errorLbl.setVisible(False)
    
        # Add Signals
        self.dialog.addSavingsBtn.clicked.connect(lambda: self.open_msg())
        self.dialog.resetBtn.clicked.connect(lambda: self.reset_form())
        self.dialog.cancelBtn.clicked.connect(lambda: self.close())
        self.exec_()
    
    def open_msg(self):
        self.msgbox = MsgBox()
        self.msgbox.ui.messageTitle.setText("Add Christmas Savings for " + self.member['fullname'] + '?')
        self.msgbox.ui.label.setText("Are you sure you want to add a christmas savings of N" +  str(self.dialog.doubleSpinBox_2.value()) + \
            " for " + self.member['fullname'] + "?")
        self.msgbox.ui.messageYesBtn.clicked.connect(lambda: self.add_xmas())
        self.msgbox.ui.messageNoBtn.clicked.connect(lambda: self.msgbox.close())
        self.msgbox.exec()


    def add_xmas(self): 
        randNo = random.randint(1000, 10000)
        mem_id = MemberChristmas().memberid
        member_id = mem_id[0]
        member = self.member_db.get_member((member_id,))
        xmas_type = self.dialog.savingsTypeCombo.currentText().strip()
        memberID = MemberChristmas().memberID
        xmasID =memberID + '/XMAS'+ str(randNo)
        month = self.dialog.monthCombo.currentText().strip()
        year = self.dialog.yearCombo.currentText().strip()
        amount = float(self.dialog.doubleSpinBox_2.value())
        details = xmas_type + " for " + month + ", " + year
        date_created = datetime.datetime.now()
        date_last_modified = date_created
        mem_total_xmas = member['total_xmas']    
        if amount <= 0:
            self.dialog.errorLbl.setText("Christmas Savings amount cannot be less than or equal to N0.00")
            self.dialog.errorLbl.setVisible(True)
            self.msgbox.close()    
        else:
            interest = 0.00
            total_xmas = mem_total_xmas + amount
               
            xmas_data = (xmasID, xmas_type, month, year, details, amount, interest, \
            total_xmas, date_created, date_last_modified, member_id)
            member_xmas_data = (total_xmas, member_id)

            self.xmas_db.add_xmas_saving(xmas_data)
            self.member_db.update_member_xmas(member_xmas_data)
            ui = MemberChristmas().ui
            MemberChristmas().loadXmasTable(ui, (member_id,))  
            self.msgbox.close()
            self.close()   

    
    def reset_form(self):
        print("Resetting form...")

class MakeWithdrawal(QDialog):
    def __init__(self):
        super().__init__()
        self.dialog = Ui_Dialog()
        self.dialog.setupUi(self)
        self.member_db = Member_DB()
        self.xmas_db = Xmas_DB()
        self.years = Utils().generate_years()
        self.dialog.errorLbl.setVisible(False)
        
    def initialise_withdrawal(self, id):
        # Initialise widgets
        self.dialog.savingsTypeCombo.clear()
        self.dialog.savingsTypeCombo.addItems(['Withdrawal From Xmas Savings'])
        self.memberid = id
        self.member = self.member_db.get_member(self.memberid)
        today = datetime.date.today()
        current_year = today.strftime("%Y")
        current_month = today.strftime("%B")
        self.dialog.label.setText('Make Christmas Savings Withdrawal from the account of ' + self.member['fullname'] + '?')
        self.dialog.label_8.setText('Transaction Type')
        self.dialog.yearCombo.addItems(self.years)
        self.dialog.monthCombo.setCurrentText(current_month)
        self.dialog.yearCombo.setCurrentText(current_year)
        self.dialog.addSavingsBtn.setText("Make Withdrawal")    
        self.dialog.addSavingsBtn.setIcon(QIcon('./static/icon/white/file-minus.svg'))   
        self.dialog.errorLbl.setWordWrap(True)
        self.dialog.errorLbl.setVisible(False)
    
        # Add Signals
        self.dialog.addSavingsBtn.clicked.connect(lambda: self.open_msg())
        self.dialog.resetBtn.clicked.connect(lambda: self.reset_form())
        self.dialog.cancelBtn.clicked.connect(lambda: self.close())
        self.exec()
    
    def open_msg(self):
        self.msgbox = MsgBox()
        self.msgbox.ui.messageTitle.setText("Make Christmas Savings Withdrawal for " + self.member['fullname'] + '?')
        self.msgbox.ui.label.setText("Are you sure you want to make a christmas savings withdrawal of N" +  str(self.dialog.doubleSpinBox_2.value()) + \
            " for " + self.member['fullname'] + "?")
        self.msgbox.ui.messageYesBtn.clicked.connect(lambda: self.make_withdrawal())
        self.msgbox.ui.messageNoBtn.clicked.connect(lambda: self.msgbox.close())
        self.msgbox.exec()

    def reset_form(self):
        print("Resetting form...")

    def make_withdrawal(self):
        randNo = random.randint(1000, 10000)
        xmas_type = self.dialog.savingsTypeCombo.currentText().strip()
        memberID = self.member['memberID']
        xmasID =memberID + '/XWD'+ str(randNo)
    
        month = self.dialog.monthCombo.currentText().strip()
        year = self.dialog.yearCombo.currentText().strip()
        amount = float(self.dialog.doubleSpinBox_2.value())
        details = xmas_type + " for " + month + ", " + year
        date_created = datetime.datetime.now()
        date_last_modified = date_created
        mem_total_xmas = self.member['total_xmas']
        if amount <= 0:
            self.dialog.errorLbl.setText("Withdrawal amount cannot be less than or equal to N0.00")
            self.dialog.errorLbl.setVisible(True)
            self.msgbox.close()
        else:
            interest = 0.00
            total_xmas = mem_total_xmas - amount 
                
            mem_id = self.memberid[0]
            xmas_data = (xmasID, xmas_type, month, year, details, amount, interest, \
                total_xmas, date_created, date_last_modified, mem_id)
            member_xmas_data = (total_xmas, mem_id)
            
            self.xmas_db.add_xmas_saving(xmas_data)
            self.member_db.update_member_xmas(member_xmas_data)
            ui = MemberChristmas().ui
            MemberChristmas().loadXmasTable(ui, self.memberid)  
            self.msgbox.close()
            self.close()   

class EditXmasDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.dialog = Ui_Dialog()
        self.dialog.setupUi(self)
        self.member_db = Member_DB()
        self.member = MemberChristmas.member
        self.xmas_db = Xmas_DB()
    
    def initialise_edit(self, id):
        self.years = Utils().generate_years()
        self.xmas = self.xmas_db.get_xmas_saving((id,))
    
        # Initialise Widget
        self.dialog.label.setText('Edit' + self.xmas['details'] + '?')
        self.dialog.monthCombo.setCurrentText(self.xmas['month'])
        self.dialog.yearCombo.setCurrentText(self.xmas['year'])
        self.dialog.yearCombo.addItems(self.years)
        self.dialog.savingsTypeCombo.clear()
        self.dialog.savingsTypeCombo.addItems([self.xmas['type']])
        self.dialog.savingsTypeCombo.setCurrentText(self.xmas['type'])
        self.dialog.doubleSpinBox_2.setValue(self.xmas['amount'])
        self.dialog.addSavingsBtn.setText("Update")
        self.dialog.addSavingsBtn.setIcon(QIcon('./static/icon/white/refresh-cw.svg'))
        self.dialog.addSavingsBtn.clicked.connect(lambda: self.open_msg(self.xmas['xmas_id']))
        self.dialog.resetBtn.clicked.connect(lambda: self.reset_form())
        self.dialog.cancelBtn.clicked.connect(lambda: self.close())
        self.dialog.errorLbl.setWordWrap(True)
        self.dialog.errorLbl.setVisible(False)
        self.exec_()
    
    def open_msg(self, id):
        self.msgbox = MsgBox()
        self.msgbox.ui.messageTitle.setText("Edit Christmas Savings Transaction of " + self.member['fullname'] + '?')
        self.msgbox.ui.label.setText("Are you sure you want to edit this transaction of " + self.member['fullname'] + "?")
        self.msgbox.ui.messageYesBtn.clicked.connect(lambda: self.edit_finally(id))
        self.msgbox.ui.messageNoBtn.clicked.connect(lambda: self.msgbox.close())
        self.msgbox.exec_()

    def reset_form(self):
        print("Resetting form...")

    def edit_finally(self, id):
        # try:
        xmasToEdit = self.xmas_db.get_xmas_saving((id,))
        memberid = xmasToEdit['member_id']
        memberToEdit = self.member_db.get_member((memberid,))
        idToEdit = xmasToEdit['xmas_id']
        xmasToEditType = xmasToEdit['type']
        xmasToEditAmount = xmasToEdit['amount']
        xmasToEditTotalXmas = xmasToEdit['total_xmas']
        xmasToEditInterest = xmasToEdit['interest']
        xmasToEditDateCreated = xmasToEdit['date_created']
        memberToEditTotalXmas = memberToEdit['total_xmas']
        reqAmount = float(self.dialog.doubleSpinBox_2.text())
        reqMonth = self.dialog.monthCombo.currentText()
        reqYear = self.dialog.yearCombo.currentText()
        reqType = self.dialog.savingsTypeCombo.currentText()

        if xmasToEditType == "Christmas Savings":
            xmasToEditTotalXmas = xmasToEditTotalXmas + (reqAmount - xmasToEditAmount)
        else:
            xmasToEditTotalXmas = xmasToEditTotalXmas - (reqAmount - xmasToEditAmount) 

        xmasToEditAmount = reqAmount
        xmasToEditMonth = reqMonth
        xmasToEditType = reqType
        xmasToEditYear = reqYear
        details = xmasToEditType + " for " + xmasToEditMonth + ", " + xmasToEditYear
        date_last_modified = datetime.datetime.now()
        
        xmas_data = (xmasToEdit['xmasID'], xmasToEditType, xmasToEditMonth, xmasToEditYear, \
            details, xmasToEditAmount, xmasToEditInterest, xmasToEditTotalXmas, \
            xmasToEditDateCreated, date_last_modified, memberid, idToEdit)
        
        self.xmas_db.update_xmas_saving(xmas_data)
        
        memberToEditTotalXmas = xmasToEditTotalXmas
        member_xmas_data = (memberToEditTotalXmas, memberid)

        self.member_db.update_member_xmas(member_xmas_data)

        params = (idToEdit, memberid)
        
        editableXmass = self.xmas_db.get_editable_xmass(params)
        
        for xmas in editableXmass:
            if xmas['type'] == "Christmas Savings":
                xmas['total_xmas'] = memberToEditTotalXmas + xmas['amount']
                memberToEditTotalXmas = xmas['total_xmas']
            else:
                xmas['total_xmas'] = memberToEditTotalXmas - xmas['amount']
                memberToEditTotalXmas = xmas['total_xmas']

            date_last_modified = datetime.datetime.now()
            xmasData = (xmas['xmasID'], xmas['type'], xmas['month'], xmas['year'], xmas['details'], \
                        xmas['amount'], xmas['interest'], xmas['total_xmas'], \
                        xmas['date_created'], date_last_modified, xmas['member_id'], xmas['xmas_id'])
            member_xmas_data = (memberToEditTotalXmas, memberid)
            self.xmas_db.update_xmas(xmasData)               
            self.member_db.update_member_xmas(member_xmas_data)
        
        ui = MemberChristmas().ui
        id = MemberChristmas().memberid
        MemberChristmas().loadXmasTable(ui, id)
        self.msgbox.close()
        self.close()
        # except:
            # print("An error occurred. Unable to delete the xmas")    

class HandleDeleteCom(MsgBox):
    def __init__(self):
        super().__init__()  
        self.xmas_db = Xmas_DB()
        self.member_db = Member_DB()

    def delete_xmas(self, id):
        self.ui.messageTitle.setText("Delete Christmas Savings Transaction?")
        self.ui.label.setText('''Are you sure you want to delete this transaction?''')
        self.ui.messageYesBtn.clicked.connect(lambda: self.delete_finally(id) )
        self.ui.messageNoBtn.clicked.connect(lambda: self.close() )
        self.exec()        
    
    def delete_finally(self, id):
        # try:
        xmasToDelete = self.xmas_db.get_xmas_saving((id,))
        memberid = xmasToDelete['member_id']
        memberToEdit = self.member_db.get_member((memberid,))
        idToDelete = xmasToDelete['xmas_id']
        xmasToDeleteType = xmasToDelete['type']
        xmasToDeleteAmount = xmasToDelete['amount']
        xmasToDeleteTotalXmas = xmasToDelete['total_xmas']
        xmasToDeleteInterest = xmasToDelete['interest']
        memberToEditTotalXmas = memberToEdit['total_xmas']
        if xmasToDeleteType == "Christmas Savings":
            memberToEditTotalXmas = xmasToDeleteTotalXmas - xmasToDeleteAmount
        else:
            memberToEditTotalXmas = xmasToDeleteTotalXmas + xmasToDeleteAmount
       
        member_xmas_data =  (memberToEditTotalXmas, memberid)        
        self.member_db.update_member_xmas(member_xmas_data)

        params = (idToDelete, memberid)        
        editableXmass = self.xmas_db.get_editable_xmass(params)
        
        for xmas in editableXmass:
            if xmas['type'] == "Christmas Savings":
                xmas['total_xmas'] = memberToEditTotalXmas + xmas['amount']
                memberToEditTotalXmas = xmas['total_xmas']
            else:
                xmas['total_xmas'] = memberToEditTotalXmas - (xmas['amount'] + xmas['interest'])
                memberToEditTotalXmas = xmas['total_xmas']

            date_last_modified = datetime.datetime.now()
            xmasData = (xmas['xmasID'], xmas['type'], xmas['month'], xmas['year'], xmas['details'], \
                        xmas['amount'], xmas['interest'], xmas['total_xmas'], \
                        xmas['date_created'], date_last_modified, xmas['member_id'], xmas['xmas_id'])
            member_xmas_data = (memberToEditTotalXmas, memberid)
            self.xmas_db.update_xmas_saving(xmasData)               
            self.member_db.update_member_xmas(member_xmas_data)
        
        self.xmas_db.remove_xmas_saving((idToDelete,))
        ui = MemberChristmas().ui
        id = MemberChristmas().memberid
        MemberChristmas().loadXmasTable(ui, id)
        self.close()
        # except:
            # print("An error occurred. Unable to delete the xmas")  

class HandleRefresh():
    def handle_table_dbl_click(self, table):
        index = table.selectionModel().currentIndex()
        value = index.sibling(index.row(), 8).data()
        # print(value)
        EditXmasDialog().initialise_edit(value)
        # self.view_member.get_ui(ui, (value,))
    
    def refresh_xmas(self, ui, id):
        MemberChristmas().loadXmasTable(ui, id)

class MemberChristmas(QMainWindow):
    def __init__(self):
        super().__init__()  
              
    @classmethod
    def loadXmasTable(self, ui, id):
        self.member_db = Member_DB()
        self.xmas_db = Xmas_DB()
        self.ui = ui
        self.memberid = id
                        
        # Initialise widgets      
        self.ui.searchXmasTxt.setPlaceholderText("Search xmas savings by amount, date, details or id")
        self.ui.stackedWidget.setCurrentIndex(5)
        self.ui.memberTransTab.setCurrentIndex(2)
        self.xmas_savings = self.xmas_db.get_member_xmas_savings(self.memberid)
        self.member = self.member_db.get_member(self.memberid)
        self.memberID = self.member['memberID']
        # self.ui.titleLbl.setText("Account Details - " + self.member['title'] + " " + self.member['fullname'])
        self.ui.xmasBalanceLbl.setText(str(self.member['total_xmas']))
        self.ui.addXmasBtn.clicked.connect(lambda: AddXmasDialog().initialise_add_xmas(self.memberid))
        self.ui.withdrawXmasBtn.clicked.connect(lambda: MakeWithdrawal().initialise_withdrawal(self.memberid))
        self.ui.refreshXmasBtn.clicked.connect(lambda: HandleRefresh().refresh_xmas(self.ui, self.memberid))

        self.ui.searchXmasTxt.textChanged.connect(lambda: SearchXmasSavings().search_xmas())
        # self.ui.searchXmasTxt.setPlaceholderText('Type search query and press enter')
        self.ui.searchXmasTxt.returnPressed.connect(lambda: SearchXmasSavings().search_xmas())
        self.ui.searchXmasTxt.setClearButtonEnabled(True)
        self.ui.searchXmasBtn.clicked.connect(lambda: SearchXmasSavings().search_xmas())
        self.ui.searchXmasBtn.setStyleSheet("QPushButton::hover{background-color: #cce0ff;}")
        LoadTable().load_table(self.xmas_savings)

        
class LoadTable():
    def load_table(self, xmas_savings):
        # Initialise xmas_savubgs table
        table = MemberChristmas.ui.xmasSavingsTable
        table.setObjectName("xmasTable")
        table.setRowCount(len(xmas_savings))
        table.setColumnCount(9)
        table.setHorizontalHeaderLabels(["Transaction ID", "Date Created", "Details", "Amount", "Interest", "Total Xmas Savings", "Last Updated", "", ""])
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.doubleClicked.connect(lambda: HandleRefresh().handle_table_dbl_click(table))  
        table.setColumnHidden(8, True)  
     
        header = table.horizontalHeader()
        vert = table.verticalHeader()
        # header.setDefaultAlignment(Qt.AlignLeft)
        # header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)  
        vert.setSectionResizeMode(QHeaderView.ResizeToContents)

        row = 0
        for xmas in xmas_savings:
            format = '%Y-%m-%d %H:%M:%S.%f'
            date_created = datetime.datetime.strptime((xmas['date_created']), format).strftime("%d/%m/%Y")
            date_last_modified = datetime.datetime.strptime((xmas['date_last_modified']), format).strftime("%d/%m/%Y")
            table.setItem(row, 0, QTableWidgetItem(xmas['xmasID']))
            table.setItem(row, 1, QTableWidgetItem(date_created))
            table.setItem(row, 2, QTableWidgetItem(xmas['details']))
            table.setItem(row, 3, QTableWidgetItem(str(xmas['amount'])))
            table.setItem(row, 4, QTableWidgetItem(str(xmas['interest'])))
            table.setItem(row, 5, QTableWidgetItem(str(xmas['total_xmas'])))
            table.setItem(row, 6, QTableWidgetItem(date_last_modified))
            table.setStyleSheet("QPushButton::hover{background-color: #cce0ff;}")
            edit_button = QPushButton()
            delete_button = QPushButton()
            edit_button.setIcon(QIcon('./static/icon/blue/edit.svg'))
            delete_button.setIcon(QIcon('./static/icon/red/trash-2.svg'))
            edit_button.setToolTip("Edit Transaction")
            delete_button.setToolTip("Delete Transaction")
            edit_button.clicked.connect(partial(EditXmasDialog().initialise_edit, xmas['xmas_id']))
            delete_button.clicked.connect(partial(HandleDeleteCom().delete_xmas, xmas['xmas_id']))
            hbox = QHBoxLayout(table)
            widg = QWidget()
            hbox.addWidget(edit_button)
            hbox.addWidget(delete_button)
            widg.setLayout(hbox)
            table.setCellWidget(row, 7, widg)
            table.setItem(row, 8, QTableWidgetItem(str(xmas['xmas_id'])))
            row += 1        
    
class SearchXmasSavings():
    def search_xmas(self):
        searchText = (MemberChristmas.ui.searchXmasTxt.text()).lower()
        if searchText == "":
            LoadTable().load_table(MemberChristmas.xmas_savings)
        else:
            new_xmas_savings = [xmas for xmas in MemberChristmas.xmas_savings if searchText in (xmas['month']).lower() or \
            searchText in (str(xmas['amount'])).lower() or searchText in (xmas['year']).lower() or \
            searchText in (xmas['date_created']).lower() or searchText in (xmas['date_last_modified']).lower() or \
            searchText in (xmas['details']).lower() or searchText in (str(xmas['total_xmas'])).lower()]

            if new_xmas_savings == []:
                LoadTable().load_table(MemberChristmas.xmas_savings)
            else:
                LoadTable().load_table(new_xmas_savings)  
    

   
    
    

