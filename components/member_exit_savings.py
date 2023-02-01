from functools import partialmethod, partial
from PyQt5.QtWidgets import QWidget, QMessageBox, QMainWindow, QLabel, QLineEdit, \
     QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QVBoxLayout, QGridLayout, \
     QHeaderView, QAbstractItemView, QFileDialog, QDialog
from PyQt5.QtCore import Qt, QPoint, pyqtSlot
from PyQt5.QtGui import QMouseEvent, QIcon, QPixmap, QFont
import sys, random, datetime
sys.path.insert(0, 'C:/Python Apps/FOPAJ/data')
sys.path.insert(1, 'C:/Python Apps/FOPAJ/ui')
from exit_savings import Exit_DB
from data.members import Member_DB
from ui.add_savings_ui import Ui_Dialog
from utils import Utils
from message import MsgBox

class AddExitDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.dialog = Ui_Dialog()
        self.dialog.setupUi(self)
        self.member_db = Member_DB()
        self.exit_db = Exit_DB()        
        self.years = Utils().generate_years()
        self.dialog.errorLbl.setVisible(False)  
        
    def initialise_add_exit(self, id):
        self.dialog.savingsTypeCombo.clear()
        self.dialog.savingsTypeCombo.addItems(['Exit Savings'])
        # Initialise widgets
        self.memberid = id
        self.member = self.member_db.get_member(self.memberid)
        today = datetime.date.today()
        current_year = today.strftime("%Y")
        current_month = today.strftime("%B")
        self.dialog.label.setText('Add Exit Savings for ' + self.member['fullname'] + '?')
        self.dialog.label_8.setText('Transaction Type')
        self.dialog.yearCombo.addItems(self.years)
        self.dialog.yearCombo.addItems(self.years)
        self.dialog.monthCombo.setCurrentText(current_month)
        self.dialog.yearCombo.setCurrentText(current_year)
        self.dialog.addSavingsBtn.setText("Add Exit Savings")    
        self.dialog.errorLbl.setWordWrap(True)
        self.dialog.errorLbl.setVisible(False)
    
        # Add Signals
        self.dialog.addSavingsBtn.clicked.connect(lambda: self.open_msg())
        self.dialog.resetBtn.clicked.connect(lambda: self.reset_form())
        self.dialog.cancelBtn.clicked.connect(lambda: self.close())
        self.exec_()
    
    def open_msg(self):
        self.msgbox = MsgBox()
        self.msgbox.ui.messageTitle.setText("Add Exit Savings for " + self.member['fullname'] + '?')
        self.msgbox.ui.label.setText("Are you sure you want to add an exit savings of N" +  str(self.dialog.doubleSpinBox_2.value()) + \
            " for " + self.member['fullname'] + "?")
        self.msgbox.ui.messageYesBtn.clicked.connect(lambda: self.add_exit())
        self.msgbox.ui.messageNoBtn.clicked.connect(lambda: self.msgbox.close())
        self.msgbox.exec()


    def add_exit(self): 
        randNo = random.randint(1000, 10000)
        mem_id = MemberExit().memberid
        member_id = mem_id[0]
        member = self.member_db.get_member((member_id,))
        exit_type = self.dialog.savingsTypeCombo.currentText().strip()
        memberID = MemberExit().memberID
        exitID =memberID + '/EXIT'+ str(randNo)
        month = self.dialog.monthCombo.currentText().strip()
        year = self.dialog.yearCombo.currentText().strip()
        amount = float(self.dialog.doubleSpinBox_2.value())
        details = exit_type + " for " + month + ", " + year
        date_created = datetime.datetime.now()
        date_last_modified = date_created
        mem_total_exit = member['total_exit']    
        if amount <= 0:
            self.dialog.errorLbl.setText("Exit Savings amount cannot be less than or equal to N0.00")
            self.dialog.errorLbl.setVisible(True)
            self.msgbox.close()    
        else:
            interest = 0.00
            total_exit = mem_total_exit + amount
               
            exit_data = (exitID, exit_type, month, year, details, amount, interest, \
            total_exit, date_created, date_last_modified, member_id)
            member_exit_data = (total_exit, member_id)

            self.exit_db.add_exit_saving(exit_data)
            self.member_db.update_member_exit(member_exit_data)
            ui = MemberExit().ui
            MemberExit().loadExitTable(ui, (member_id,))  
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
        self.exit_db = Exit_DB()
        self.years = Utils().generate_years()
        self.dialog.errorLbl.setVisible(False)
        
    def initialise_withdrawal(self, id):
        # Initialise widgets
        self.dialog.savingsTypeCombo.clear()
        self.dialog.savingsTypeCombo.addItems(['Withdrawal From Exit Savings'])
        self.memberid = id
        self.member = self.member_db.get_member(self.memberid)
        today = datetime.date.today()
        current_year = today.strftime("%Y")
        current_month = today.strftime("%B")
        self.dialog.label.setText('Make Exit Savings Withdrawal from the account of ' + self.member['fullname'] + '?')
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
        self.msgbox.ui.messageTitle.setText("Make Exit Savings Withdrawal for " + self.member['fullname'] + '?')
        self.msgbox.ui.label.setText("Are you sure you want to make a exit savings withdrawal of N" +  str(self.dialog.doubleSpinBox_2.value()) + \
            " for " + self.member['fullname'] + "?")
        self.msgbox.ui.messageYesBtn.clicked.connect(lambda: self.make_withdrawal())
        self.msgbox.ui.messageNoBtn.clicked.connect(lambda: self.msgbox.close())
        self.msgbox.exec()

    def reset_form(self):
        print("Resetting form...")

    def make_withdrawal(self):
        randNo = random.randint(1000, 10000)
        exit_type = self.dialog.savingsTypeCombo.currentText().strip()
        memberID = self.member['memberID']
        exitID =memberID + '/XWD'+ str(randNo)
    
        month = self.dialog.monthCombo.currentText().strip()
        year = self.dialog.yearCombo.currentText().strip()
        amount = float(self.dialog.doubleSpinBox_2.value())
        details = exit_type + " for " + month + ", " + year
        date_created = datetime.datetime.now()
        date_last_modified = date_created
        mem_total_exit = self.member['total_exit']
        if amount <= 0:
            self.dialog.errorLbl.setText("Withdrawal amount cannot be less than or equal to N0.00")
            self.dialog.errorLbl.setVisible(True)
            self.msgbox.close()
        else:
            interest = 0.00
            total_exit = mem_total_exit - amount 
                
            mem_id = self.memberid[0]
            exit_data = (exitID, exit_type, month, year, details, amount, interest, \
                total_exit, date_created, date_last_modified, mem_id)
            member_exit_data = (total_exit, mem_id)
            
            self.exit_db.add_exit_saving(exit_data)
            self.member_db.update_member_exit(member_exit_data)
            ui = MemberExit().ui
            MemberExit().loadExitTable(ui, self.memberid)  
            self.msgbox.close()
            self.close()   

class EditExitDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.dialog = Ui_Dialog()
        self.dialog.setupUi(self)
        self.member_db = Member_DB()
        self.exit_db = Exit_DB()
    
    def initialise_edit(self, id):
        self.years = Utils().generate_years()
        self.exit = self.exit_db.get_exit_saving((id,))
    
        # Initialise Widget
        self.dialog.label.setText('Edit' + self.exit['details'] + '?')
        self.dialog.monthCombo.setCurrentText(self.exit['month'])
        self.dialog.yearCombo.setCurrentText(self.exit['year'])
        self.dialog.yearCombo.addItems(self.years)
        self.dialog.savingsTypeCombo.setCurrentText(self.exit['type'])
        self.dialog.doubleSpinBox_2.setValue(self.exit['amount'])
        self.dialog.addSavingsBtn.setText("Update")
        self.dialog.addSavingsBtn.setIcon(QIcon('./static/icon/white/refresh-cw.svg'))
        self.dialog.addSavingsBtn.clicked.connect(lambda: self.open_msg(self.exit['exit_id']))
        self.dialog.resetBtn.clicked.connect(lambda: self.reset_form())
        self.dialog.cancelBtn.clicked.connect(lambda: self.close())
        self.dialog.errorLbl.setWordWrap(True)
        self.dialog.errorLbl.setVisible(False)
        self.exec_()
    
    def open_msg(self, id):
        self.msgbox = MsgBox()
        self.msgbox.ui.messageTitle.setText("Edit Exits Savings Transaction of " + self.member['fullname'] + '?')
        self.msgbox.ui.label.setText("Are you sure you want to edit this transaction of " + self.member['fullname'] + "?")
        self.msgbox.ui.messageYesBtn.clicked.connect(lambda: self.edit_finally(id))
        self.msgbox.ui.messageNoBtn.clicked.connect(lambda: self.msgbox.close())
        self.msgbox.exec_()

    def reset_form(self):
        print("Resetting form...")

    def edit_finally(self, id):
        # try:
        exitToEdit = self.exit_db.get_exit_saving((id,))
        memberid = exitToEdit['member_id']
        memberToEdit = self.member_db.get_member((memberid,))
        idToEdit = exitToEdit['exit_id']
        exitToEditType = exitToEdit['type']
        exitToEditAmount = exitToEdit['amount']
        exitToEditTotalExit = exitToEdit['total_exit']
        exitToEditInterest = exitToEdit['interest']
        exitToEditDateCreated = exitToEdit['date_created']
        memberToEditTotalExit = memberToEdit['total_exit']
        reqAmount = float(self.dialog.doubleSpinBox_2.text())
        reqMonth = self.dialog.monthCombo.currentText()
        reqYear = self.dialog.yearCombo.currentText()
        reqType = self.dialog.savingsTypeCombo.currentText()

        if exitToEditType == "Exit Savings":
            exitToEditTotalExit = exitToEditTotalExit + (reqAmount - exitToEditAmount)
        else:
            exitToEditTotalExit = exitToEditTotalExit - (reqAmount - exitToEditAmount) 

        exitToEditAmount = reqAmount
        exitToEditMonth = reqMonth
        exitToEditType = reqType
        exitToEditYear = reqYear
        details = exitToEditType + " for " + exitToEditMonth + ", " + exitToEditYear
        date_last_modified = datetime.datetime.now()
        
        exit_data = (exitToEdit['exitID'], exitToEditType, exitToEditMonth, exitToEditYear, \
            details, exitToEditAmount, exitToEditInterest, exitToEditTotalExit, \
            exitToEditDateCreated, date_last_modified, memberid, idToEdit)
        
        self.exit_db.update_exit(exit_data)
        
        memberToEditTotalExit = exitToEditTotalExit
        member_exit_data = (memberToEditTotalExit, memberid)

        self.member_db.update_member_exit(member_exit_data)

        params = (idToEdit, memberid)
        
        editableExits = self.exit_db.get_editable_exits(params)
        
        for exit in editableExits:
            if exit['type'] == "Exit Savings":
                exit['total_exit'] = memberToEditTotalExit + exit['amount']
                memberToEditTotalExit = exit['total_exit']
            else:
                exit['total_exit'] = memberToEditTotalExit - exit['amount']
                memberToEditTotalExit = exit['total_exit']

            today = datetime.date.today()
            date_last_modified = today.strftime("%d/%m/%Y")
            exitData = (exit['exitID'], exit['type'], exit['month'], exit['year'], exit['details'], \
                        exit['amount'], exit['interest'], exit['total_exit'], \
                        exit['date_created'], date_last_modified, exit['member_id'], exit['exit_id'])
            member_exit_data = (memberToEditTotalExit, memberid)
            self.exit_db.update_exit(exitData)               
            self.member_db.update_member_exit(member_exit_data)
        
        ui = MemberExit().ui
        id = MemberExit().memberid
        MemberExit().loadExitTable(ui, id)
        self.msgbox.close()
        self.close()
        # except:
            # print("An error occurred. Unable to delete the exit")    

class HandleDeleteCom(MsgBox):
    def __init__(self):
        super().__init__()  
        self.exit_db = Exit_DB()
        self.member_db = Member_DB()

    def delete_exit(self, id):
        self.ui.messageTitle.setText("Delete Exit Savings Transaction?")
        self.ui.label.setText('''Are you sure you want to delete this transaction?''')
        self.ui.messageYesBtn.clicked.connect(lambda: self.delete_finally(id) )
        self.ui.messageNoBtn.clicked.connect(lambda: self.close() )
        self.exec()        
    
    def delete_finally(self, id):
        # try:
        exitToDelete = self.exit_db.get_exit_saving((id,))
        memberid = exitToDelete['member_id']
        memberToEdit = self.member_db.get_member((memberid,))
        idToDelete = exitToDelete['exit_id']
        exitToDeleteType = exitToDelete['type']
        exitToDeleteAmount = exitToDelete['amount']
        exitToDeleteTotalExit = exitToDelete['total_exit']
        exitToDeleteInterest = exitToDelete['interest']
        memberToEditTotalExit = memberToEdit['total_exit']
        if exitToDeleteType == "Exit Savings":
            memberToEditTotalExit = exitToDeleteTotalExit - exitToDeleteAmount
        else:
            memberToEditTotalExit = exitToDeleteTotalExit + exitToDeleteAmount
       
        member_exit_data =  (memberToEditTotalExit, memberid)        
        self.member_db.update_member_exit(member_exit_data)

        params = (idToDelete, memberid)        
        editableExits = self.exit_db.get_editable_exits(params)
        
        for exit in editableExits:
            if exit['type'] == "Exit Savings":
                exit['total_exit'] = memberToEditTotalExit + exit['amount']
                memberToEditTotalExit = exit['total_exit']
            else:
                exit['total_exit'] = memberToEditTotalExit - (exit['amount'] + exit['interest'])
                memberToEditTotalExit = exit['total_exit']

            date_last_modified = datetime.datetime.now()
            exitData = (exit['exitID'], exit['type'], exit['month'], exit['year'], exit['details'], \
                        exit['amount'], exit['interest'], exit['total_exit'], \
                        exit['date_created'], date_last_modified, exit['member_id'], exit['exit_id'])
            member_exit_data = (memberToEditTotalExit, memberid)
            self.exit_db.update_exit_saving(exitData)               
            self.member_db.update_member_exit(member_exit_data)
        
        self.exit_db.remove_exit_saving((idToDelete,))
        ui = MemberExit().ui
        id = MemberExit().memberid
        MemberExit().loadExitTable(ui, id)
        self.close()
        # except:
            # print("An error occurred. Unable to delete the exit")  

class HandleRefresh():
    def handle_table_dbl_click(self, table):
        index = table.selectionModel().currentIndex()
        value = index.sibling(index.row(), 8).data()
        # print(value)
        EditExitDialog().initialise_edit(value)
        # self.view_member.get_ui(ui, (value,))
    
    def refresh_exit(self, ui, id):
        MemberExit().loadExitTable(ui, id)

class MemberExit(QMainWindow):
    def __init__(self):
        super().__init__()  
              
    @classmethod
    def loadExitTable(self, ui, id):
        self.member_db = Member_DB()
        self.exit_db = Exit_DB()
        self.ui = ui
        self.memberid = id
                        
        # Initialise widgets      
        self.ui.searchExitTxt.setPlaceholderText("Search exit savings by amount, date, details or id")
        self.ui.stackedWidget.setCurrentIndex(5)
        self.ui.memberTransTab.setCurrentIndex(4)
        self.exit_savings = self.exit_db.get_member_exit_savings(self.memberid)
        self.member = self.member_db.get_member(self.memberid)
        self.memberID = self.member['memberID']
        # self.ui.titleLbl.setText("Account Details - " + self.member['title'] + " " + self.member['fullname'])
        self.ui.exitBalanceLbl.setText(str(self.member['total_exit']))
        self.ui.addExitBtn.clicked.connect(lambda: AddExitDialog().initialise_add_exit(self.memberid))
        self.ui.withdrawExitBtn.clicked.connect(lambda: MakeWithdrawal().initialise_withdrawal(self.memberid))
        self.ui.refreshExitBtn.clicked.connect(lambda: HandleRefresh().refresh_exit(self.ui, self.memberid))
        self.ui.searchExitTxt.textChanged.connect(lambda: SearchExitSavings().search_exit())
        # self.ui.searchExitTxt.setPlaceholderText('Type search query and press enter')
        self.ui.searchExitTxt.returnPressed.connect(lambda: SearchExitSavings().search_exit())
        self.ui.searchExitTxt.setClearButtonEnabled(True)
        self.ui.searchExitBtn.clicked.connect(lambda: SearchExitSavings().search_exit())
        self.ui.searchExitBtn.setStyleSheet("QPushButton::hover{background-color: #cce0ff;}")
        LoadTable().load_table(self.exit_savings)
        
class LoadTable():
    def load_table(self, exit_savings):        
        # Initialise exitaction table
        table = MemberExit.ui.exitSavingsTable
        table.setObjectName("exitTable")
        table.setRowCount(len(exit_savings))
        table.setColumnCount(9)
        table.setHorizontalHeaderLabels(["Transaction ID", "Date Created", "Details", "Amount", "Interest", "Total Exit Savings", "Last Updated", "", ""])
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
        for exit in exit_savings:
            format = '%Y-%m-%d %H:%M:%S.%f'
            date_created = datetime.datetime.strptime((exit['date_created']), format).strftime("%d/%m/%Y")
            date_last_modified = datetime.datetime.strptime((exit['date_last_modified']), format).strftime("%d/%m/%Y")
            table.setItem(row, 0, QTableWidgetItem(exit['exitID']))
            table.setItem(row, 1, QTableWidgetItem(date_created))
            table.setItem(row, 2, QTableWidgetItem(exit['details']))
            table.setItem(row, 3, QTableWidgetItem(str(exit['amount'])))
            table.setItem(row, 4, QTableWidgetItem(str(exit['interest'])))
            table.setItem(row, 5, QTableWidgetItem(str(exit['total_exit'])))
            table.setItem(row, 6, QTableWidgetItem(date_last_modified))
            table.setStyleSheet("QPushButton::hover{background-color: #cce0ff;}")
            edit_button = QPushButton()
            delete_button = QPushButton()
            edit_button.setIcon(QIcon('./static/icon/blue/edit.svg'))
            delete_button.setIcon(QIcon('./static/icon/red/trash-2.svg'))
            edit_button.setToolTip("Edit Transaction")
            delete_button.setToolTip("Delete Transaction")
            edit_button.clicked.connect(partial(EditExitDialog().initialise_edit, exit['exit_id']))
            delete_button.clicked.connect(partial(HandleDeleteCom().delete_exit, exit['exit_id']))
            hbox = QHBoxLayout(table)
            widg = QWidget()
            hbox.addWidget(edit_button)
            hbox.addWidget(delete_button)
            widg.setLayout(hbox)
            table.setCellWidget(row, 7, widg)
            table.setItem(row, 8, QTableWidgetItem(str(exit['exit_id'])))
            row += 1        

class SearchExitSavings():
    def search_exit(self):
        searchText = (MemberExit.ui.searchExitTxt.text()).lower()
        if searchText == "":
            LoadTable().load_table(MemberExit.exit_savings)
        else:
            new_exit_savings = [exit for exit in MemberExit.exit_savings if searchText in (exit['month']).lower() or \
            searchText in (str(exit['amount'])).lower() or searchText in (exit['year']).lower() or \
            searchText in (exit['date_created']).lower() or searchText in (exit['date_last_modified']).lower() or \
            searchText in (exit['details']).lower() or searchText in (str(exit['total_exit'])).lower()]

            if new_exit_savings == []:
                LoadTable().load_table(MemberExit.exit_savings)
            else:
                LoadTable().load_table(new_exit_savings)      

    

   
    
    

