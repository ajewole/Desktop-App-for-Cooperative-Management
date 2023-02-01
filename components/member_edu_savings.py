from functools import partialmethod, partial
from PyQt5.QtWidgets import QWidget, QMessageBox, QMainWindow, QLabel, QLineEdit, \
     QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QVBoxLayout, QGridLayout, \
     QHeaderView, QAbstractItemView, QFileDialog, QDialog
from PyQt5.QtCore import Qt, QPoint, pyqtSlot
from PyQt5.QtGui import QMouseEvent, QIcon, QPixmap, QFont
import sys, random, datetime
sys.path.insert(0, 'C:/Python Apps/FOPAJ/data')
sys.path.insert(1, 'C:/Python Apps/FOPAJ/ui')
from edu_savings import Edu_DB
from data.members import Member_DB
from ui.add_savings_ui import Ui_Dialog
from utils import Utils
from message import MsgBox

class AddEduDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.dialog = Ui_Dialog()
        self.dialog.setupUi(self)
        self.member_db = Member_DB()
        self.edu_db = Edu_DB()        
        self.years = Utils().generate_years()
        self.dialog.errorLbl.setVisible(False)  
        
    def initialise_add_edu(self, id):
        self.dialog.savingsTypeCombo.clear()
        self.dialog.savingsTypeCombo.addItems(['Educational Savings'])
        # Initialise widgets
        self.memberid = id
        self.member = self.member_db.get_member(self.memberid)
        today = datetime.date.today()
        current_year = today.strftime("%Y")
        current_month = today.strftime("%B")
        self.dialog.label.setText('Add Educational Savings for ' + self.member['fullname'] + '?')
        self.dialog.label_8.setText('Transaction Type')
        self.dialog.yearCombo.addItems(self.years)
        self.dialog.yearCombo.addItems(self.years)
        self.dialog.monthCombo.setCurrentText(current_month)
        self.dialog.yearCombo.setCurrentText(current_year)
        self.dialog.addSavingsBtn.setText("Add Educational Savings")    
        self.dialog.errorLbl.setWordWrap(True)
        self.dialog.errorLbl.setVisible(False)
    
        # Add Signals
        self.dialog.addSavingsBtn.clicked.connect(lambda: self.open_msg())
        self.dialog.resetBtn.clicked.connect(lambda: self.reset_form())
        self.dialog.cancelBtn.clicked.connect(lambda: self.close())
        self.exec_()
    
    def open_msg(self):
        self.msgbox = MsgBox()
        self.msgbox.ui.messageTitle.setText("Add Educational Savings for " + self.member['fullname'] + '?')
        self.msgbox.ui.label.setText("Are you sure you want to add an educational savings of N" +  str(self.dialog.doubleSpinBox_2.value()) + \
            " for " + self.member['fullname'] + "?")
        self.msgbox.ui.messageYesBtn.clicked.connect(lambda: self.add_edu())
        self.msgbox.ui.messageNoBtn.clicked.connect(lambda: self.msgbox.close())
        self.msgbox.exec()


    def add_edu(self): 
        randNo = random.randint(1000, 10000)
        mem_id = MemberEducational().memberid
        member_id = mem_id[0]
        member = self.member_db.get_member((member_id,))
        edu_type = self.dialog.savingsTypeCombo.currentText().strip()
        memberID = MemberEducational().memberID
        eduID =memberID + '/XMAS'+ str(randNo)
        month = self.dialog.monthCombo.currentText().strip()
        year = self.dialog.yearCombo.currentText().strip()
        amount = float(self.dialog.doubleSpinBox_2.value())
        details = edu_type + " for " + month + ", " + year
        date_created = datetime.datetime.now()
        date_last_modified = date_created
        mem_total_edu = member['total_edu']    
        if amount <= 0:
            self.dialog.errorLbl.setText("Educational Savings amount cannot be less than or equal to N0.00")
            self.dialog.errorLbl.setVisible(True)
            self.msgbox.close()    
        else:
            interest = 0.00
            total_edu = mem_total_edu + amount
               
            edu_data = (eduID, edu_type, month, year, details, amount, interest, \
            total_edu, date_created, date_last_modified, member_id)
            member_edu_data = (total_edu, member_id)

            self.edu_db.add_edu_saving(edu_data)
            self.member_db.update_member_edu(member_edu_data)
            ui = MemberEducational().ui
            MemberEducational().loadEduTable(ui, (member_id,))  
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
        self.edu_db = Edu_DB()
        self.years = Utils().generate_years()
        self.dialog.errorLbl.setVisible(False)
        
    def initialise_withdrawal(self, id):
        # Initialise widgets
        self.dialog.savingsTypeCombo.clear()
        self.dialog.savingsTypeCombo.addItems(['Withdrawal From Edu Savings'])
        self.memberid = id
        self.member = self.member_db.get_member(self.memberid)
        today = datetime.date.today()
        current_year = today.strftime("%Y")
        current_month = today.strftime("%B")
        self.dialog.label.setText('Make Educational Savings Withdrawal from the account of ' + self.member['fullname'] + '?')
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
        self.msgbox.ui.messageTitle.setText("Make Educational Savings Withdrawal for " + self.member['fullname'] + '?')
        self.msgbox.ui.label.setText("Are you sure you want to make a educational savings withdrawal of N" +  str(self.dialog.doubleSpinBox_2.value()) + \
            " for " + self.member['fullname'] + "?")
        self.msgbox.ui.messageYesBtn.clicked.connect(lambda: self.make_withdrawal())
        self.msgbox.ui.messageNoBtn.clicked.connect(lambda: self.msgbox.close())
        self.msgbox.exec()

    def reset_form(self):
        print("Resetting form...")

    def make_withdrawal(self):
        randNo = random.randint(1000, 10000)
        edu_type = self.dialog.savingsTypeCombo.currentText().strip()
        memberID = self.member['memberID']
        eduID =memberID + '/XWD'+ str(randNo)
    
        month = self.dialog.monthCombo.currentText().strip()
        year = self.dialog.yearCombo.currentText().strip()
        amount = float(self.dialog.doubleSpinBox_2.value())
        details = edu_type + " for " + month + ", " + year
        date_created = datetime.datetime.now()
        date_last_modified = date_created
        mem_total_edu = self.member['total_edu']
        if amount <= 0:
            self.dialog.errorLbl.setText("Withdrawal amount cannot be less than or equal to N0.00")
            self.dialog.errorLbl.setVisible(True)
            self.msgbox.close()
        else:
            interest = 0.00
            total_edu = mem_total_edu - amount 
                
            mem_id = self.memberid[0]
            edu_data = (eduID, edu_type, month, year, details, amount, interest, \
                total_edu, date_created, date_last_modified, mem_id)
            member_edu_data = (total_edu, mem_id)
            
            self.edu_db.add_edu_saving(edu_data)
            self.member_db.update_member_edu(member_edu_data)
            ui = MemberEducational().ui
            MemberEducational().loadEduTable(ui, self.memberid)  
            self.msgbox.close()
            self.close()   

class EditEduDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.dialog = Ui_Dialog()
        self.dialog.setupUi(self)
        self.member_db = Member_DB()
        self.edu_db = Edu_DB()
    
    def initialise_edit(self, id):
        self.years = Utils().generate_years()
        self.edu = self.edu_db.get_edu_saving((id,))
    
        # Initialise Widget
        self.dialog.label.setText('Edit' + self.edu['details'] + '?')
        self.dialog.monthCombo.setCurrentText(self.edu['month'])
        self.dialog.yearCombo.setCurrentText(self.edu['year'])
        self.dialog.yearCombo.addItems(self.years)
        self.dialog.savingsTypeCombo.setCurrentText(self.edu['type'])
        self.dialog.doubleSpinBox_2.setValue(self.edu['amount'])
        self.dialog.addSavingsBtn.setText("Update")
        self.dialog.addSavingsBtn.setIcon(QIcon('./static/icon/white/refresh-cw.svg'))
        self.dialog.addSavingsBtn.clicked.connect(lambda: self.open_msg(self.edu['edu_id']))
        self.dialog.resetBtn.clicked.connect(lambda: self.reset_form())
        self.dialog.cancelBtn.clicked.connect(lambda: self.close())
        self.dialog.errorLbl.setWordWrap(True)
        self.dialog.errorLbl.setVisible(False)
        self.exec_()
    
    def open_msg(self, id):
        self.msgbox = MsgBox()
        self.msgbox.ui.messageTitle.setText("Edit Educationals Savings Transaction of " + self.member['fullname'] + '?')
        self.msgbox.ui.label.setText("Are you sure you want to edit this transaction of " + self.member['fullname'] + "?")
        self.msgbox.ui.messageYesBtn.clicked.connect(lambda: self.edit_finally(id))
        self.msgbox.ui.messageNoBtn.clicked.connect(lambda: self.msgbox.close())
        self.msgbox.exec_()

    def reset_form(self):
        print("Resetting form...")

    def edit_finally(self, id):
        # try:
        eduToEdit = self.edu_db.get_edu_saving((id,))
        memberid = eduToEdit['member_id']
        memberToEdit = self.member_db.get_member((memberid,))
        idToEdit = eduToEdit['edu_id']
        eduToEditType = eduToEdit['type']
        eduToEditAmount = eduToEdit['amount']
        eduToEditTotalEdu = eduToEdit['total_edu']
        eduToEditInterest = eduToEdit['interest']
        eduToEditDateCreated = eduToEdit['date_created']
        memberToEditTotalEdu = memberToEdit['total_edu']
        reqAmount = float(self.dialog.doubleSpinBox_2.text())
        reqMonth = self.dialog.monthCombo.currentText()
        reqYear = self.dialog.yearCombo.currentText()
        reqType = self.dialog.savingsTypeCombo.currentText()

        if eduToEditType == "Educational Savings":
            eduToEditTotalEdu = eduToEditTotalEdu + (reqAmount - eduToEditAmount)
        else:
            eduToEditTotalEdu = eduToEditTotalEdu - (reqAmount - eduToEditAmount) 

        eduToEditAmount = reqAmount
        eduToEditMonth = reqMonth
        eduToEditType = reqType
        eduToEditYear = reqYear
        details = eduToEditType + " for " + eduToEditMonth + ", " + eduToEditYear
        date_last_modified = datetime.datetime.now()
        
        edu_data = (eduToEdit['eduID'], eduToEditType, eduToEditMonth, eduToEditYear, \
            details, eduToEditAmount, eduToEditInterest, eduToEditTotalEdu, \
            eduToEditDateCreated, date_last_modified, memberid, idToEdit)
        
        self.edu_db.update_edu(edu_data)
        
        memberToEditTotalEdu = eduToEditTotalEdu
        member_edu_data = (memberToEditTotalEdu, memberid)

        self.member_db.update_member_edu(member_edu_data)

        params = (idToEdit, memberid)
        
        editableEdus = self.edu_db.get_editable_edus(params)
        
        for edu in editableEdus:
            if edu['type'] == "Educational Savings":
                edu['total_edu'] = memberToEditTotalEdu + edu['amount']
                memberToEditTotalEdu = edu['total_edu']
            else:
                edu['total_edu'] = memberToEditTotalEdu - edu['amount']
                memberToEditTotalEdu = edu['total_edu']

            date_last_modified = datetime.datetime.now()
            eduData = (edu['eduID'], edu['type'], edu['month'], edu['year'], edu['details'], \
                        edu['amount'], edu['interest'], edu['total_edu'], \
                        edu['date_created'], date_last_modified, edu['member_id'], edu['edu_id'])
            member_edu_data = (memberToEditTotalEdu, memberid)
            self.edu_db.update_edu(eduData)               
            self.member_db.update_member_edu(member_edu_data)
        
        ui = MemberEducational().ui
        id = MemberEducational().memberid
        MemberEducational().loadEduTable(ui, id)
        self.msgbox.close()
        self.close()
        # except:
            # print("An error occurred. Unable to delete the edu")    

class HandleDeleteEdu(MsgBox):
    def __init__(self):
        super().__init__()  
        self.edu_db = Edu_DB()
        self.member_db = Member_DB()

    def delete_edu(self, id):
        self.ui.messageTitle.setText("Delete Educational Savings Transaction?")
        self.ui.label.setText('''Are you sure you want to delete this transaction?''')
        self.ui.messageYesBtn.clicked.connect(lambda: self.delete_finally(id) )
        self.ui.messageNoBtn.clicked.connect(lambda: self.close() )
        self.exec()        
    
    def delete_finally(self, id):
        # try:
        eduToDelete = self.edu_db.get_edu_saving((id,))
        memberid = eduToDelete['member_id']
        memberToEdit = self.member_db.get_member((memberid,))
        idToDelete = eduToDelete['edu_id']
        eduToDeleteType = eduToDelete['type']
        eduToDeleteAmount = eduToDelete['amount']
        eduToDeleteTotalEdu = eduToDelete['total_edu']
        eduToDeleteInterest = eduToDelete['interest']
        memberToEditTotalEdu = memberToEdit['total_edu']
        if eduToDeleteType == "Educational Savings":
            memberToEditTotalEdu = eduToDeleteTotalEdu - eduToDeleteAmount
        else:
            memberToEditTotalEdu = eduToDeleteTotalEdu + eduToDeleteAmount
       
        member_edu_data =  (memberToEditTotalEdu, memberid)        
        self.member_db.update_member_edu(member_edu_data)

        params = (idToDelete, memberid)        
        editableEdus = self.edu_db.get_editable_edus(params)
        
        for edu in editableEdus:
            if edu['type'] == "Educational Savings":
                edu['total_edu'] = memberToEditTotalEdu + edu['amount']
                memberToEditTotalEdu = edu['total_edu']
            else:
                edu['total_edu'] = memberToEditTotalEdu - (edu['amount'] + edu['interest'])
                memberToEditTotalEdu = edu['total_edu']

            date_last_modified = datetime.datetime.now()
            eduData = (edu['eduID'], edu['type'], edu['month'], edu['year'], edu['details'], \
                        edu['amount'], edu['interest'], edu['total_edu'], \
                        edu['date_created'], date_last_modified, edu['member_id'], edu['edu_id'])
            member_edu_data = (memberToEditTotalEdu, memberid)
            self.edu_db.update_edu_saving(eduData)               
            self.member_db.update_member_edu(member_edu_data)
        
        self.edu_db.remove_edu_saving((idToDelete,))
        ui = MemberEducational().ui
        id = MemberEducational().memberid
        MemberEducational().loadEduTable(ui, id)
        self.close()
        # except:
            # print("An error occurred. Unable to delete the edu")  

class HandleRefresh():
    def handle_table_dbl_click(self, table):
        index = table.selectionModel().currentIndex()
        value = index.sibling(index.row(), 8).data()
        # print(value)
        EditEduDialog().initialise_edit(value)
        # self.view_member.get_ui(ui, (value,))
    
    def refresh_edu(self, ui, id):
        MemberEducational().loadEduTable(ui, id)

class MemberEducational(QMainWindow):
    def __init__(self):
        super().__init__()  
              
    @classmethod
    def loadEduTable(self, ui, id):
        self.member_db = Member_DB()
        self.edu_db = Edu_DB()
        self.ui = ui
        self.memberid = id
                        
        # Initialise widgets      
        self.ui.searchEduTxt.setPlaceholderText("Search educational savings by amount, date, details or id")
        self.ui.stackedWidget.setCurrentIndex(5)
        self.ui.memberTransTab.setCurrentIndex(3)
        self.edu_savings = self.edu_db.get_member_edu_savings(self.memberid)
        self.member = self.member_db.get_member(self.memberid)
        self.memberID = self.member['memberID']
        # self.ui.titleLbl.setText("Account Details - " + self.member['title'] + " " + self.member['fullname'])
        self.ui.eduBalanceLbl.setText(str(self.member['total_edu']))
        self.ui.addEduBtn.clicked.connect(lambda: AddEduDialog().initialise_add_edu(self.memberid))
        self.ui.withdrawEduBtn.clicked.connect(lambda: MakeWithdrawal().initialise_withdrawal(self.memberid))
        self.ui.refreshEduBtn.clicked.connect(lambda: HandleRefresh().refresh_edu(self.ui, self.memberid))

        self.ui.searchEduTxt.textChanged.connect(lambda: SearchEduSavings().search_edu())
        # self.ui.searchEduTxt.setPlaceholderText('Type search query and press enter')
        self.ui.searchEduTxt.returnPressed.connect(lambda: SearchEduSavings().search_edu())
        self.ui.searchEduTxt.setClearButtonEnabled(True)
        self.ui.searchEduBtn.clicked.connect(lambda: SearchEduSavings().search_edu())
        self.ui.searchEduBtn.setStyleSheet("QPushButton::hover{background-color: #cce0ff;}")
        LoadTable().load_table(self.edu_savings)
        
class LoadTable():
    def load_table(self, edu_savings):
        # Initialise eduaction table
        table = MemberEducational.ui.eduSavingsTable
        table.setObjectName("eduTable")
        table.setRowCount(len(edu_savings))
        table.setColumnCount(9)
        table.setHorizontalHeaderLabels(["Transaction ID", "Date Created", "Details", "Amount", "Interest", "Total Edu Savings", "Last Updated", "", ""])
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
        for edu in edu_savings:
            format = '%Y-%m-%d %H:%M:%S.%f'
            date_created = datetime.datetime.strptime((edu['date_created']), format).strftime("%d/%m/%Y")
            date_last_modified = datetime.datetime.strptime((edu['date_last_modified']), format).strftime("%d/%m/%Y")
            table.setItem(row, 0, QTableWidgetItem(edu['eduID']))
            table.setItem(row, 1, QTableWidgetItem(date_created))
            table.setItem(row, 2, QTableWidgetItem(edu['details']))
            table.setItem(row, 3, QTableWidgetItem(str(edu['amount'])))
            table.setItem(row, 4, QTableWidgetItem(str(edu['interest'])))
            table.setItem(row, 5, QTableWidgetItem(str(edu['total_edu'])))
            table.setItem(row, 6, QTableWidgetItem(date_last_modified))
            table.setStyleSheet("QPushButton::hover{background-color: #cce0ff;}")
            edit_button = QPushButton()
            delete_button = QPushButton()
            edit_button.setIcon(QIcon('./static/icon/blue/edit.svg'))
            delete_button.setIcon(QIcon('./static/icon/red/trash-2.svg'))
            edit_button.setToolTip("Edit Transaction")
            delete_button.setToolTip("Delete Transaction")
            edit_button.clicked.connect(partial(EditEduDialog().initialise_edit, edu['edu_id']))
            delete_button.clicked.connect(partial(HandleDeleteEdu().delete_edu, edu['edu_id']))
            hbox = QHBoxLayout(table)
            widg = QWidget()
            hbox.addWidget(edit_button)
            hbox.addWidget(delete_button)
            widg.setLayout(hbox)
            table.setCellWidget(row, 7, widg)
            table.setItem(row, 8, QTableWidgetItem(str(edu['edu_id'])))
            row += 1    

class SearchEduSavings():
    def search_edu(self):
        searchText = (MemberEducational.ui.searchEduTxt.text()).lower()
        if searchText == "":
            LoadTable().load_table(MemberEducational.edu_savings)
        else:
            new_edu_savings = [edu for edu in MemberEducational.edu_savings if searchText in (edu['month']).lower() or \
            searchText in (str(edu['amount'])).lower() or searchText in (edu['year']).lower() or \
            searchText in (edu['date_created']).lower() or searchText in (edu['date_last_modified']).lower() or \
            searchText in (edu['details']).lower() or searchText in (str(edu['total_edu'])).lower()]

            if new_edu_savings == []:
                LoadTable().load_table(MemberEducational.edu_savings)
            else:
                LoadTable().load_table(new_edu_savings)      
    
    

   
    
    

