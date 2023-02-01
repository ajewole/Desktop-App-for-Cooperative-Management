from functools import partialmethod, partial
from PyQt5.QtWidgets import QWidget, QMessageBox, QMainWindow, QLabel, QLineEdit, \
     QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QVBoxLayout, QGridLayout, \
     QHeaderView, QAbstractItemView, QFileDialog, QDialog
from PyQt5.QtCore import Qt, QPoint, pyqtSlot
from PyQt5.QtGui import QMouseEvent, QIcon, QPixmap, QFont
import sys, random, datetime
sys.path.insert(0, 'C:/Python Apps/FOPAJ/data')
sys.path.insert(1, 'C:/Python Apps/FOPAJ/ui')
from commodities import Comm_DB
from data.members import Member_DB
from ui.add_savings_ui import Ui_Dialog
from utils import Utils
from message import MsgBox

class AddCommodityDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.dialog = Ui_Dialog()
        self.dialog.setupUi(self)
        self.member_db = Member_DB()
        self.com_db = Comm_DB()        
        self.years = Utils().generate_years()
        self.dialog.errorLbl.setVisible(False)  
        
    def initialise_add_commodity(self, id):
        self.dialog.savingsTypeCombo.clear()
        self.dialog.savingsTypeCombo.addItems(['Cash Commodity', 'FoodStuff Commodity', 'Farm Produce Commodity', 'Other Commodity'])
        # Initialise widgets
        self.memberid = id
        self.member = self.member_db.get_member(self.memberid)
        today = datetime.date.today()
        current_year = today.strftime("%Y")
        current_month = today.strftime("%B")
        self.dialog.label.setText('Add Commodity Loan for ' + self.member['fullname'] + '?')
        self.dialog.label_8.setText('Commodity Loan Type')
        self.dialog.yearCombo.addItems(self.years)
        self.dialog.yearCombo.addItems(self.years)
        self.dialog.monthCombo.setCurrentText(current_month)
        self.dialog.yearCombo.setCurrentText(current_year)
        self.dialog.addSavingsBtn.setText("Add Commodity Loan")    
        self.dialog.errorLbl.setWordWrap(True)
        self.dialog.errorLbl.setVisible(False)
    
        # Add Signals
        self.dialog.addSavingsBtn.clicked.connect(lambda: self.open_msg())
        self.dialog.resetBtn.clicked.connect(lambda: self.reset_form())
        self.dialog.cancelBtn.clicked.connect(lambda: self.close())
        self.exec_()
    
    def open_msg(self):
        self.msgbox = MsgBox()
        self.msgbox.ui.messageTitle.setText("Add Commodity Loan for " + self.member['fullname'] + '?')
        self.msgbox.ui.label.setText("Are you sure you want to add a commodity loan of N" +  str(self.dialog.doubleSpinBox_2.value()) + \
            " for " + self.member['fullname'] + "?")
        self.msgbox.ui.messageYesBtn.clicked.connect(lambda: self.add_commodity())
        self.msgbox.ui.messageNoBtn.clicked.connect(lambda: self.msgbox.close())
        self.msgbox.exec_()


    def add_commodity(self): 
        randNo = random.randint(1000, 10000)
        mem_id = MemberCommodities().memberid
        member_id = mem_id[0]
        member = self.member_db.get_member((member_id,))
        com_type = self.dialog.savingsTypeCombo.currentText().strip()
        memberID = MemberCommodities().memberID
        comID =memberID + '/COM'+ str(randNo)
        month = self.dialog.monthCombo.currentText().strip()
        year = self.dialog.yearCombo.currentText().strip()
        amount = float(self.dialog.doubleSpinBox_2.value())
        details = com_type + " for " + month + ", " + year
        date_created = datetime.datetime.now()
        date_last_modified = date_created
        mem_commodity_balance = member['commodity_balance']    
        if amount <= 0:
            self.dialog.errorLbl.setText("Repayment cannot be less than or equal to N0.00")
            self.dialog.errorLbl.setVisible(True)
            self.msgbox.close()    
        else:
            interest = 0.1 * amount
            commodity_balance = mem_commodity_balance + amount + interest
               
            com_data = (comID, com_type, month, year, details, amount, interest, \
            commodity_balance, date_created, date_last_modified, member_id)
            member_com_data = (commodity_balance, member_id)

            self.com_db.add_commodity(com_data)
            self.member_db.update_member_com(member_com_data)
            ui = MemberCommodities().ui
            MemberCommodities().loadComTable(ui, (member_id,))  
            self.msgbox.close()
            self.close()   

    
    def reset_form(self):
        print("Resetting form...")

class AddRepayment(QDialog):
    def __init__(self):
        super().__init__()
        self.dialog = Ui_Dialog()
        self.dialog.setupUi(self)
        self.member_db = Member_DB()
        self.com_db = Comm_DB()
        self.years = Utils().generate_years()
        self.dialog.errorLbl.setVisible(False)
        
    def initialise_repayment(self, id):
        # Initialise widgets
        self.dialog.savingsTypeCombo.clear()
        self.dialog.savingsTypeCombo.addItems(['Commodity Repayment'])
        self.memberid = id
        self.member = self.member_db.get_member(self.memberid)
        today = datetime.date.today()
        current_year = today.strftime("%Y")
        current_month = today.strftime("%B")
        self.dialog.label.setText('Add Commodity Repayment to account of ' + self.member['fullname'] + '?')
        self.dialog.label_8.setText('Transaction Type')
        self.dialog.yearCombo.addItems(self.years)
        self.dialog.monthCombo.setCurrentText(current_month)
        self.dialog.yearCombo.setCurrentText(current_year)
        self.dialog.addSavingsBtn.setText("Add Repayment")    
        self.dialog.addSavingsBtn.setIcon(QIcon('./static/icon/white/file-plus.svg'))   
        self.dialog.errorLbl.setWordWrap(True)
        self.dialog.errorLbl.setVisible(False)
    
        # Add Signals
        self.dialog.addSavingsBtn.clicked.connect(lambda: self.open_msg())
        self.dialog.resetBtn.clicked.connect(lambda: self.reset_form())
        self.dialog.cancelBtn.clicked.connect(lambda: self.close())
        self.exec_()
    
    def open_msg(self):
        self.msgbox = MsgBox()
        self.msgbox.ui.messageTitle.setText("Add Commodity Loan Repayment for " + self.member['fullname'] + '?')
        self.msgbox.ui.label.setText("Are you sure you want to add a commodity loan repayment of N" +  str(self.dialog.doubleSpinBox_2.value()) + \
            " for " + self.member['fullname'] + "?")
        self.msgbox.ui.messageYesBtn.clicked.connect(lambda: self.make_repayment())
        self.msgbox.ui.messageNoBtn.clicked.connect(lambda: self.msgbox.close())
        self.msgbox.exec_()

    def reset_form(self):
        print("Resetting form...")

    def make_repayment(self):
        randNo = random.randint(1000, 10000)
        com_type = self.dialog.savingsTypeCombo.currentText().strip()
        memberID = self.member['memberID']
        comID =memberID + '/REP'+ str(randNo)
    
        month = self.dialog.monthCombo.currentText().strip()
        year = self.dialog.yearCombo.currentText().strip()
        amount = float(self.dialog.doubleSpinBox_2.value())
        details = com_type + " for " + month + ", " + year
        date_created = datetime.datetime.now()
        date_last_modified = date_created
        mem_commodity_balance = self.member['commodity_balance']
        if amount <= 0:
            self.dialog.errorLbl.setText("Repayment cannot be less than or equal to N0.00")
            self.dialog.errorLbl.setVisible(True)
            self.msgbox.close()
        else:
            interest = 0.00
            commodity_balance = mem_commodity_balance - amount 
                
            mem_id = self.memberid[0]
            com_data = (comID, com_type, month, year, details, amount, interest, \
                commodity_balance, date_created, date_last_modified, mem_id)
            member_com_data = (commodity_balance, mem_id)
            
            self.com_db.add_commodity(com_data)
            self.member_db.update_member_com(member_com_data)
            ui = MemberCommodities().ui
            MemberCommodities().loadComTable(ui, self.memberid)  
            self.msgbox.close()
            self.close()   

class EditComDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.dialog = Ui_Dialog()
        self.dialog.setupUi(self)
        self.member_db = Member_DB()
        self.com_db = Comm_DB()
    
    def initialise_edit(self, id):
        self.years = Utils().generate_years()
        self.commodity = self.com_db.get_commodity((id,))
    
        # Initialise Widget
        self.dialog.label.setText('Edit Commodity of ' + self.commodity['details'] + '?')
        self.dialog.monthCombo.setCurrentText(self.commodity['month'])
        self.dialog.yearCombo.setCurrentText(self.commodity['year'])
        self.dialog.yearCombo.addItems(self.years)
        self.dialog.savingsTypeCombo.setCurrentText(self.commodity['type'])
        self.dialog.doubleSpinBox_2.setValue(self.commodity['amount'])
        self.dialog.addSavingsBtn.setText("Update")
        self.dialog.addSavingsBtn.setIcon(QIcon('./static/icon/white/refresh-cw.svg'))
        self.dialog.addSavingsBtn.clicked.connect(lambda: self.open_msg(self.commodity['com_id']))
        self.dialog.resetBtn.clicked.connect(lambda: self.reset_form())
        self.dialog.cancelBtn.clicked.connect(lambda: self.close())
        self.dialog.errorLbl.setWordWrap(True)
        self.dialog.errorLbl.setVisible(False)
        self.exec_()
    
    def open_msg(self, id):
        self.msgbox = MsgBox()
        self.msgbox.ui.messageTitle.setText("Edit Commodity Loan Transaction of " + self.member['fullname'] + '?')
        self.msgbox.ui.label.setText("Are you sure you want to edit this transaction of " + self.member['fullname'] + "?")
        self.msgbox.ui.messageYesBtn.clicked.connect(lambda: self.edit_finally(id))
        self.msgbox.ui.messageNoBtn.clicked.connect(lambda: self.msgbox.close())
        self.msgbox.exec_()

    def reset_form(self):
        print("Resetting form...")

    def edit_finally(self, id):
        # try:
        comToEdit = self.com_db.get_commodity((id,))
        memberid = comToEdit['member_id']
        memberToEdit = self.member_db.get_member((memberid,))
        idToEdit = comToEdit['com_id']
        comToEditType = comToEdit['type']
        comToEditAmount = comToEdit['amount']
        comToEditCommodityBalance = comToEdit['commodity_balance']
        comToEditInterest = comToEdit['interest']
        comToEditDateCreated = comToEdit['date_created']
        memberToEditCommodityBalance = memberToEdit['commodity_balance']
        reqAmount = float(self.dialog.doubleSpinBox_2.text())
        reqMonth = self.dialog.monthCombo.currentText()
        reqYear = self.dialog.yearCombo.currentText()
        reqType = self.dialog.savingsTypeCombo.currentText()

        if comToEditType == "Commodity Repayment":
            comToEditCommodityBalance = comToEditCommodityBalance - (reqAmount - comToEditAmount)
        else:
            comToEditCommodityBalance = comToEditCommodityBalance + (0.1 * reqAmount + reqAmount-(comToEditInterest + comToEditAmount)) 
            comToEditInterest = 0.1 * reqAmount 

        comToEditAmount = reqAmount
        comToEditMonth = reqMonth
        comToEditType = reqType
        comToEditYear = reqYear
        details = comToEditType + " for " + comToEditMonth + ", " + comToEditYear
        date_last_modified = datetime.datetime.now()
        
        com_data = (comToEdit['comID'], comToEditType, comToEditMonth, comToEditYear, \
            details, comToEditAmount, comToEditInterest, comToEditCommodityBalance, \
            comToEditDateCreated, date_last_modified, memberid, idToEdit)
        
        self.com_db.update_commodity(com_data)
        
        memberToEditCommodityBalance = comToEditCommodityBalance
        member_com_data = (memberToEditCommodityBalance, memberid)

        self.member_db.update_member_com(member_com_data)

        params = (idToEdit, memberid)
        
        editableComs = self.com_db.get_editable_coms(params)
        
        for com in editableComs:
            if com['type'] == "Commodity Repayment":
                com['commodity_balance'] = memberToEditCommodityBalance - com['amount']
                memberToEditCommodityBalance = com['commodity_balance']
            else:
                com['commodity_balance'] = memberToEditCommodityBalance + (com['amount'] + com['interest'])
                memberToEditCommodityBalance = com['commodity_balance']

            date_last_modified = datetime.datetime.now()
            comData = (com['comID'], com['type'], com['month'], com['year'], com['details'], \
                        com['amount'], com['interest'], com['commodity_balance'], \
                        com['date_created'], date_last_modified, com['member_id'], com['com_id'])
            member_com_data = (memberToEditCommodityBalance, memberid)
            self.com_db.update_commodity(comData)               
            self.member_db.update_member_com(member_com_data)
        
        ui = MemberCommodities().ui
        id = MemberCommodities().memberid
        MemberCommodities().loadComTable(ui, id)
        self.msgbox.close()
        self.close()
        # except:
            # print("An error occurred. Unable to delete the commodity")    

class HandleDeleteCom(MsgBox):
    def __init__(self):
        super().__init__()  
        self.com_db = Comm_DB()
        self.member_db = Member_DB()

    def delete_com(self, id):
        self.ui.messageTitle.setText("Delete Commodity Loan?")
        self.ui.label.setText('''Are you sure you want to delete this commodity loan?''')
        self.ui.messageYesBtn.clicked.connect(lambda: self.delete_finally(id) )
        self.ui.messageNoBtn.clicked.connect(lambda: self.close() )
        self.exec()        
    
    def delete_finally(self, id):
        # try:
        comToDelete = self.com_db.get_commodity((id,))
        memberid = comToDelete['member_id']
        memberToEdit = self.member_db.get_member((memberid,))
        idToDelete = comToDelete['com_id']
        comToDeleteType = comToDelete['type']
        comToDeleteAmount = comToDelete['amount']
        comToDeleteCommodityBalance = comToDelete['commodity_balance']
        comToDeleteInterest = comToDelete['interest']
        memberToEditCommodityBalance = memberToEdit['commodity_balance']
        if comToDeleteType == "Commodity Repayment":
            memberToEditCommodityBalance = comToDeleteCommodityBalance + comToDeleteAmount
        else:
            memberToEditCommodityBalance = comToDeleteCommodityBalance - (comToDeleteAmount + comToDeleteInterest)
       
        member_com_data =  (memberToEditCommodityBalance, memberid)           

        self.member_db.update_member_com(member_com_data)

        params = (idToDelete, memberid)
        
        editableComs = self.com_db.get_editable_coms(params)
        
        for com in editableComs:
            if com['type'] == "Commodity Repayment":
                com['commodity_balance'] = memberToEditCommodityBalance - com['amount']
                memberToEditCommodityBalance = com['commodity_balance']
            else:
                com['commodity_balance'] = memberToEditCommodityBalance + (com['amount'] + com['interest'])
                memberToEditCommodityBalance = com['commodity_balance']

            date_last_modified = datetime.datetime.now()
            comData = (com['comID'], com['type'], com['month'], com['year'], com['details'], \
                        com['amount'], com['interest'], com['commodity_balance'], \
                        com['date_created'], date_last_modified, com['member_id'], com['com_id'])
            member_com_data = (memberToEditCommodityBalance, memberid)
            self.com_db.update_commodity(comData)               
            self.member_db.update_member_com(member_com_data)
        
        self.com_db.remove_commodity((idToDelete,))
        ui = MemberCommodities().ui
        id = MemberCommodities().memberid
        MemberCommodities().loadComTable(ui, id)
        self.close()
        # except:
            # print("An error occurred. Unable to delete the commodity")  

class HandleRefresh():
    def handle_table_dbl_click(self, table):
        index = table.selectionModel().currentIndex()
        value = index.sibling(index.row(), 9).data()
        # print(value)
        EditComDialog().initialise_edit(value)
        # self.view_member.get_ui(ui, (value,))
    
    def refresh_com(self, ui, id):
        MemberCommodities().loadComTable(ui, id)

class MemberCommodities(QMainWindow):
    def __init__(self):
        super().__init__()  
              
    @classmethod
    def loadComTable(self, ui, id):
        self.member_db = Member_DB()
        self.com_db = Comm_DB()
        self.ui = ui
        self.memberid = id
                        
        # Initialise widgets      
        self.ui.searchCommodityTxt.setPlaceholderText("Search commodities by amount, date, details or id")
        self.ui.stackedWidget.setCurrentIndex(5)
        self.ui.memberTransTab.setCurrentIndex(1)
        self.commodities = self.com_db.get_member_commodities(self.memberid)
        self.member = self.member_db.get_member(self.memberid)
        self.memberID = self.member['memberID']
        # self.ui.titleLbl.setText("Account Details - " + self.member['title'] + " " + self.member['fullname'])
        self.ui.commodityBalanceLbl_2.setText(str(self.member['commodity_balance']))
        self.ui.addCommodityBtn.clicked.connect(lambda: AddCommodityDialog().initialise_add_commodity(self.memberid))
        self.ui.commodityRepaymentBtn.clicked.connect(lambda: AddRepayment().initialise_repayment(self.memberid))
        self.ui.refreshCommodityBtn.clicked.connect(lambda: HandleRefresh().refresh_com(self.ui, self.memberid))
        self.ui.searchCommodityTxt.textChanged.connect(lambda: SearchCommodities().search_com())
        # self.ui.searchCommodityTxt.setPlaceholderText('Type search query and press enter')
        self.ui.searchCommodityTxt.returnPressed.connect(lambda: SearchCommodities().search_com())
        self.ui.searchCommodityTxt.setClearButtonEnabled(True)
        self.ui.searchCommodityBtn.clicked.connect(lambda: SearchCommodities().search_com())
        self.ui.searchCommodityBtn.setStyleSheet("QPushButton::hover{background-color: #cce0ff;}")
        LoadTable().load_table(self.commodities)

class LoadTable():
    def load_table(self, commodities):       
       # Initialise comaction table
        table = MemberCommodities.ui.commodityTable
        table.setObjectName("comTable")
        table.setRowCount(len(commodities))
        table.setColumnCount(9)
        table.setHorizontalHeaderLabels(["Transaction ID", "Date Created", "Details", "Amount", "Interest", "Commodity Loan Balance", "Last Updated", "", ""])
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
        for com in commodities:
            format = '%Y-%m-%d %H:%M:%S.%f'
            date_created = datetime.datetime.strptime((com['date_created']), format).strftime("%d/%m/%Y")
            date_last_modified = datetime.datetime.strptime((com['date_last_modified']), format).strftime("%d/%m/%Y")
            table.setItem(row, 0, QTableWidgetItem(com['comID']))
            table.setItem(row, 1, QTableWidgetItem(date_created))
            table.setItem(row, 2, QTableWidgetItem(com['details']))
            table.setItem(row, 3, QTableWidgetItem(str(com['amount'])))
            table.setItem(row, 4, QTableWidgetItem(str(com['interest'])))
            table.setItem(row, 5, QTableWidgetItem(str(com['commodity_balance'])))
            table.setItem(row, 6, QTableWidgetItem(date_last_modified))
            table.setStyleSheet("QPushButton::hover{background-color: #cce0ff;}")
            edit_button = QPushButton()
            delete_button = QPushButton()
            edit_button.setIcon(QIcon('./static/icon/blue/edit.svg'))
            delete_button.setIcon(QIcon('./static/icon/red/trash-2.svg'))
            edit_button.setToolTip("Edit Transaction")
            delete_button.setToolTip("Delete Transaction")
            edit_button.clicked.connect(partial(EditComDialog().initialise_edit, com['com_id']))
            delete_button.clicked.connect(partial(HandleDeleteCom().delete_com, com['com_id']))
            hbox = QHBoxLayout(table)
            widg = QWidget()
            hbox.addWidget(edit_button)
            hbox.addWidget(delete_button)
            widg.setLayout(hbox)
            table.setCellWidget(row, 7, widg)
            table.setItem(row, 8, QTableWidgetItem(str(com['com_id'])))
            row += 1 

class SearchCommodities():
    def search_com(self):
        searchText = (MemberCommodities.ui.searchCommodityTxt.text()).lower()
        if searchText == "":
            LoadTable().load_table(MemberCommodities.commodities)
        else:
            new_coms = [com for com in MemberCommodities.commodities if searchText in (com['month']).lower() or \
            searchText in (str(com['amount'])).lower() or searchText in (com['year']).lower() or \
            searchText in (com['date_created']).lower() or searchText in (com['date_last_modified']).lower() or \
            searchText in (com['details']).lower() or searchText in (str(com['commodity_balance'])).lower()]

            if new_coms == []:
                LoadTable().load_table(MemberCommodities.commodities)
            else:
                LoadTable().load_table(new_coms)    

