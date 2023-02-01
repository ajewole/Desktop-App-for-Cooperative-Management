from functools import partialmethod, partial
import signal
from PyQt5.QtWidgets import QWidget, QMessageBox, QMainWindow, QLabel, QLineEdit, \
     QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QVBoxLayout, QGridLayout, \
     QHeaderView, QAbstractItemView, QFileDialog, QDialog
from PyQt5.QtCore import Qt, QPoint, pyqtSlot
from PyQt5.QtGui import QMouseEvent, QIcon, QPixmap, QFont
import sys, random, datetime
sys.path.insert(0, 'C:/Python Apps/FOPAJ/data')
sys.path.insert(1, 'C:/Python Apps/FOPAJ/ui')
from monthly_transactions import Monthly_DB
from data.members import Member_DB
from ui.add_savings_ui import Ui_Dialog
from ui.search_members_ui import Ui_Dialog as Search_Dialog
from common_dialog import CommonDialog
from utils import Utils
from message import MsgBox
from member_commodities import MemberCommodities
from member_xmas_savings import MemberChristmas
from member_edu_savings import MemberEducational
from member_exit_savings import MemberExit

class AddSavingsDialog():
    def __init__(self):
        super().__init__()
        # self.dialog = Ui_Dialog()
        # self.dialog.setupUi(self)
        
        self.member_db = Member_DB()
        self.trans_db = Monthly_DB()        
        self.years = Utils().generate_years()
        # self.exec_()
        
    def initialise_add_savings(self, id):
        self.dialog = CommonDialog()
        self.dialog.ui.savingsTypeCombo.clear()
        self.dialog.ui.savingsTypeCombo.addItems(['Monthly Contribution', 'Cash Deposit', 'Share Capital Fund'])
        self.dialog.ui.errorLbl.setVisible(False)  
        # Initialise widgets
        self.memberid = id
        self.member = self.member_db.get_member(self.memberid)
        today = datetime.date.today()
        current_year = today.strftime("%Y")
        current_month = today.strftime("%B")
        self.dialog.ui.label.setText('Add Savings for ' + self.member['fullname'] + '?')
        self.dialog.ui.label_8.setText('Savings Type')
        self.dialog.ui.yearCombo.addItems(self.years)
        self.dialog.ui.yearCombo.addItems(self.years)
        self.dialog.ui.monthCombo.setCurrentText(current_month)
        self.dialog.ui.yearCombo.setCurrentText(current_year)
        self.dialog.ui.addSavingsBtn.setText("Add Savings")    
        self.dialog.ui.errorLbl.setWordWrap(True)
        self.dialog.ui.errorLbl.setVisible(False)
    
        # Add Signals
        self.dialog.ui.addSavingsBtn.clicked.connect(self.open_msg)
        self.dialog.ui.resetBtn.clicked.connect(self.reset_form)
        self.dialog.ui.cancelBtn.clicked.connect(self.dialog.close)
        self.dialog.exec_() 
    
    def open_msg(self):
        self.msgbox = MsgBox()
        self.msgbox.ui.messageTitle.setText("Add Savings for " + self.member['fullname'] + '?')
        self.msgbox.ui.label.setText("Are you sure you want to add a saving of N" +  str(self.dialog.ui.doubleSpinBox_2.value()) + \
            " for " + self.member['fullname'] + "?")
        self.msgbox.ui.messageYesBtn.clicked.connect(self.add_savings)
        self.msgbox.ui.messageNoBtn.clicked.connect(self.msgbox.close)
        self.msgbox.exec_()

    def add_savings(self): 
        randNo = random.randint(1000, 10000)
        mem_id = MemberTransactions.memberid
        member_id = mem_id[0]
        member = self.member_db.get_member((member_id,))
        trans_type = self.dialog.ui.savingsTypeCombo.currentText().strip()
        memberID = MemberTransactions.memberID
        if trans_type == 'Monthly Contribution':
            transID =memberID + '/SAV'+ str(randNo)
        elif trans_type == 'Share Capital Fund':
            transID = memberID + '/SCF' + str(randNo)
        else:
            transID = memberID + '/DEP'+ str(randNo)         
        month = self.dialog.ui.monthCombo.currentText().strip()
        year = self.dialog.ui.yearCombo.currentText().strip()
        amount = float(self.dialog.ui.doubleSpinBox_2.value())
        details = trans_type + " for " + month + ", " + year
        today = datetime.datetime.now()
        date_created = today
        date_last_modified = today
        mem_total_savings = member['total_savings']
        mem_loan_balance = member['loan_balance']
        mem_total_assets = member['total_assets']
        if mem_loan_balance == 0:
            interest = 0
            total_savings = mem_total_savings + amount
            total_assets = mem_total_assets + amount
            loan_balance = mem_loan_balance
        elif mem_loan_balance > 0 and mem_loan_balance < amount:
            interest = 0.1 * amount
            total_savings = mem_total_savings + (amount - (mem_loan_balance + interest))
            total_assets = mem_total_assets + (amount - (mem_loan_balance + interest))
            loan_balance = 0
        elif mem_loan_balance > 0 and mem_loan_balance > amount:
            interest = 0.1 * amount
            total_savings = mem_total_savings
            total_assets = mem_total_assets
            loan_balance = (mem_loan_balance + interest) - amount
        
        trans_data = (transID, trans_type, month, year, details, amount, interest, total_savings, \
            loan_balance, date_created, date_last_modified, member_id)
        member_trans_data = (total_savings, total_assets, loan_balance, member_id)
        
        try:
            self.trans_db.add_transaction(trans_data)
            self.member_db.update_member_trans(member_trans_data)
            ui = MemberTransactions.ui
            MemberTransactions.loadTransTable(ui, (member_id,))  
            self.msgbox.close()
            self.dialog.close()   
        except Exception as e:
            print(e)

    
    def reset_form(self):
        print("Resetting form...")

class AddLoanDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.dialog = Ui_Dialog()
        self.dialog.setupUi(self)
        self.member_db = Member_DB()
        self.trans_db = Monthly_DB()
        
        self.years = Utils().generate_years()
        self.dialog.errorLbl.setVisible(False)
        
    def initialise_add_loan(self, id):
        self.dialog.savingsTypeCombo.clear()
        # Initialise widgets
        self.memberid = id
        self.member = self.member_db.get_member(self.memberid)
        today = datetime.date.today()
        current_year = today.strftime("%Y")
        current_month = today.strftime("%B")
        self.dialog.label.setText('Add Loan for ' + self.member['fullname'] + '?')
        self.dialog.label_8.setText('Loan Type')
        # self.dialog.savingsTypeCombo
        self.dialog.savingsTypeCombo.addItems(['Regular Loan', 'Emergency Loan', 'Special Loan'])
        self.dialog.yearCombo.addItems(self.years)
        self.dialog.monthCombo.setCurrentText(current_month)
        self.dialog.yearCombo.setCurrentText(current_year)
        self.dialog.addSavingsBtn.setText("Add Loan")    
        self.dialog.addSavingsBtn.setIcon(QIcon('./static/icon/white/folder-plus.svg'))   
        self.dialog.errorLbl.setWordWrap(True)
        self.dialog.errorLbl.setVisible(False)
    
        # Add Signals
        self.dialog.addSavingsBtn.clicked.connect(lambda: self.open_msg())
        self.dialog.resetBtn.clicked.connect(lambda: self.reset_form())
        self.dialog.cancelBtn.clicked.connect(lambda: self.close())
        self.exec_()
    
    def open_msg(self):
        self.msgbox = MsgBox()
        self.msgbox.ui.messageTitle.setText("Add Loan for " + self.member['fullname'] + '?')
        self.msgbox.ui.label.setText("Are you sure you want to add a loan of N" +  str(self.dialog.doubleSpinBox_2.value()) + \
            " for " + self.member['fullname'] + "?")
        self.msgbox.ui.messageYesBtn.clicked.connect(lambda: self.add_loan())
        self.msgbox.ui.messageNoBtn.clicked.connect(lambda: self.msgbox.close())
        self.msgbox.exec_()

    def reset_form(self):
        print("Resetting form...")

    def add_loan(self):
        randNo = random.randint(1000, 10000)
        trans_type = self.dialog.savingsTypeCombo.currentText().strip()
        memberID = self.member['memberID']
        if trans_type == 'Regular Loan':
            transID =memberID + '/REL'+ str(randNo)
        elif trans_type == 'Emergency Loan':
            transID = memberID + '/EML'+ str(randNo)
        else:
            transID = memberID + 'SPL' + str(randNo)         
        month = self.dialog.monthCombo.currentText().strip()
        year = self.dialog.yearCombo.currentText().strip()
        amount = float(self.dialog.doubleSpinBox_2.value())
        details = trans_type + " for " + month + ", " + year
        today = datetime.datetime.now()
        date_created = today
        date_last_modified = today
        mem_total_savings = self.member['total_savings']
        mem_loan_balance = self.member['loan_balance']
        mem_total_assets = self.member['total_assets']
        if trans_type == "Regular Loan" and mem_loan_balance > 0:
            self.dialog.errorLbl.setText("Regular loan cannot be given while there is an existing loan balance.")
            self.dialog.errorLbl.setVisible(True)
            self.msgbox.close()
        elif (trans_type == "Regular Loan" or trans_type == "Emergency Loan" or trans_type == "Special Loan") \
                and (mem_loan_balance + amount) > 2 * mem_total_assets:
            self.dialog.errorLbl.setText("The loan request and the existing loan balance is more than twice of the total assets.")
            self.dialog.errorLbl.setVisible(True)
            self.msgbox.close()
        else:
            interest = 0
            total_savings = mem_total_savings
            total_assets = mem_total_assets
            loan_balance = mem_loan_balance + amount
                
            mem_id = self.memberid[0]
            trans_data = (transID, trans_type, month, year, details, amount, interest, total_savings, \
                loan_balance, date_created, date_last_modified, mem_id)
            member_trans_data = (total_savings, total_assets, loan_balance, mem_id)
            
            self.trans_db.add_transaction(trans_data)
            self.member_db.update_member_trans(member_trans_data)
            ui = MemberTransactions.ui
            MemberTransactions.loadTransTable(ui, self.memberid)  
            self.msgbox.close()
            self.done(1)
            self.close() 


class MakeWithdrawal(QDialog):
    def __init__(self):
        super().__init__()
        self.dialog = Ui_Dialog()
        self.dialog.setupUi(self)
        self.member_db = Member_DB()
        self.trans_db = Monthly_DB()
        self.years = Utils().generate_years()
        self.dialog.errorLbl.setVisible(False)
        
    def initialise_withdrawal(self, id):
        # Initialise widgets
        self.dialog.savingsTypeCombo.clear()
        self.dialog.savingsTypeCombo.addItems(['Withdrawal From Savings', 'Special Deduction'])
        self.memberid = id
        self.member = self.member_db.get_member(self.memberid)
        today = datetime.date.today()
        current_year = today.strftime("%Y")
        current_month = today.strftime("%B")
        self.dialog.label.setText('Make Withdrawal from the Account of ' + self.member['fullname'] + '?')
        self.dialog.label_8.setText('Withdrawal Type')
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
        self.exec_()
    
    def open_msg(self):
        self.msgbox = MsgBox()
        self.msgbox.ui.messageTitle.setText("Make Withdrawal From Account of " + self.member['fullname'] + '?')
        self.msgbox.ui.label.setText("Are you sure you want to make a withdrawal of N" +  str(self.dialog.doubleSpinBox_2.value()) + \
            " from the account of " + self.member['fullname'] + "?")
        self.msgbox.ui.messageYesBtn.clicked.connect(lambda: self.make_withdrawal())
        self.msgbox.ui.messageNoBtn.clicked.connect(lambda: self.msgbox.close())
        self.msgbox.exec_()

    def reset_form(self):
        print("Resetting form...")

    def make_withdrawal(self):
        randNo = random.randint(1000, 10000)
        trans_type = self.dialog.savingsTypeCombo.currentText().strip()
        memberID = self.member['memberID']
        if trans_type == 'Withdrawal From Savings':
            transID =memberID + '/WFS'+ str(randNo)
        else:
            trans_type == 'Special Deduction'
            transID = memberID + '/SPD'+ str(randNo)
    
        month = self.dialog.monthCombo.currentText().strip()
        year = self.dialog.yearCombo.currentText().strip()
        amount = float(self.dialog.doubleSpinBox_2.value())
        details = trans_type + " for " + month + ", " + year
        date_created = datetime.datetime.now()
        date_last_modified = date_created
        mem_total_savings = self.member['total_savings']
        mem_loan_balance = self.member['loan_balance']
        mem_total_assets = self.member['total_assets']
        if trans_type == "Withdrawal From Savings" and mem_loan_balance > 0:
            self.dialog.errorLbl.setText("Withdrawal cannot be made while there is an existing loan balance.")
            self.dialog.errorLbl.setVisible(True)
            self.msgbox.close()
        elif amount > mem_total_assets:
            self.dialog.errorLbl.setText("Amount to be withdrawn must be less than the total assets.")
            self.dialog.errorLbl.setVisible(True)
            self.msgbox.close()
        else:
            interest = 0
            total_savings = mem_total_savings - amount
            total_assets = mem_total_assets - amount
            loan_balance = mem_loan_balance
                
            mem_id = self.memberid[0]
            trans_data = (transID, trans_type, month, year, details, amount, interest, total_savings, \
                loan_balance, date_created, date_last_modified, mem_id)
            member_trans_data = (total_savings, total_assets, loan_balance, mem_id)
            
            self.trans_db.add_transaction(trans_data)
            self.member_db.update_member_trans(member_trans_data)
            ui = MemberTransactions.ui
            MemberTransactions.loadTransTable(ui, self.memberid)  
            self.msgbox.close()
            self.close()   

class EditTransDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.dialog = Ui_Dialog()
        self.dialog.setupUi(self)
        self.member_db = Member_DB()
        self.trans_db = Monthly_DB()
    
    def initialise_edit(self, id):
        self.years = Utils().generate_years()
        self.transaction = self.trans_db.get_transaction((id,))
    
        # Initialise Widget
        self.dialog.label.setText('Edit Transaction of ' + self.transaction['details'] + '?')
        self.dialog.monthCombo.setCurrentText(self.transaction['month'])
        self.dialog.yearCombo.setCurrentText(self.transaction['year'])
        self.dialog.yearCombo.addItems(self.years)
        self.dialog.savingsTypeCombo.setCurrentText(self.transaction['type'])
        self.dialog.doubleSpinBox_2.setValue(self.transaction['amount'])
        self.dialog.addSavingsBtn.setText("Update")
        self.dialog.addSavingsBtn.setIcon(QIcon('./static/icon/white/refresh-cw.svg'))
        self.dialog.addSavingsBtn.clicked.connect(lambda: self.open_msg(self.transaction['trans_id']))
        self.dialog.resetBtn.clicked.connect(lambda: self.reset_form())
        self.dialog.cancelBtn.clicked.connect(lambda: self.close())
        self.dialog.errorLbl.setWordWrap(True)
        self.dialog.errorLbl.setVisible(False)
        self.exec_()
    
    def open_msg(self, id):
        self.msgbox = MsgBox()
        self.msgbox.ui.messageTitle.setText("Edit Transaction of " + self.member['fullname'] + '?')
        self.msgbox.ui.label.setText("Are you sure you want to edit this transaction of " + self.member['fullname'] + "?")
        self.msgbox.ui.messageYesBtn.clicked.connect(lambda: self.edit_finally(id))
        self.msgbox.ui.messageNoBtn.clicked.connect(lambda: self.msgbox.close())
        self.msgbox.exec_()

    def reset_form(self):
        print("Resetting form...")

    def edit_finally(self, id):
        # try:
        transToEdit = self.trans_db.get_transaction((id,))
        memberid = transToEdit['member_id']
        memberToEdit = self.member_db.get_member((memberid,))
        idToEdit = transToEdit['trans_id']
        transToEditType = transToEdit['type']
        transToEditAmount = transToEdit['amount']
        transToEditLoanBalance = transToEdit['loan_balance']
        transToEditInterest = transToEdit['interest']
        transToEditTotalSavings = transToEdit['total_savings']
        transToEditDateCreated = transToEdit['date_created']
        memberToEditTotalSavings = memberToEdit['total_savings']
        memberToEditLoanBalance = memberToEdit['loan_balance']
        memberToEditTotalAssets = memberToEdit['total_assets']
        memberToEditShareCapital = memberToEdit['share_capital']
        reqAmount = float(self.dialog.doubleSpinBox_2.text())
        reqMonth = self.dialog.monthCombo.currentText()
        reqYear = self.dialog.yearCombo.currentText()
        reqType = self.dialog.savingsTypeCombo.currentText()

        if transToEditType == "Monthly Contribution" or transToEditType == "Cash Deposit":
            if transToEditLoanBalance == 0.0 and transToEditInterest == 0.0:
                transToEditTotalSavings = transToEditTotalSavings + (reqAmount - transToEditAmount) 
            elif transToEditLoanBalance == 0.0 and transToEditInterest > 0.0:
                if reqAmount > (transToEditInterest * 100 + transToEditInterest):
                    transToEditTotalSavings = transToEditTotalSavings + (reqAmount - transToEditAmount)
                else:
                    transToEditLoanBalance = transToEditInterest * 100 + transToEditInterest - reqAmount
                    transToEditTotalSavings = transToEditTotalSavings - (transToEditAmount - transToEditInterest - transToEditInterest * 100)
            elif transToEditLoanBalance > 0.0 and transToEditInterest > 0.0:
                if reqAmount < (transToEditInterest * 100 + transToEditInterest):
                    transToEditLoanBalance = transToEditLoanBalance - (reqAmount - transToEditAmount)
                else:
                    transToEditTotalSavings = reqAmount - (transToEditLoanBalance - transToEditAmount)
                    transToEditLoanBalance = 0.0
        elif transToEditType == "Regular Loan" or transToEditType == "Emergency Loan" or transToEditType == "Special Loan":
            transToEditLoanBalance = transToEditLoanBalance + (reqAmount - transToEditAmount)
            memberToEditTotalSavings = transToEditTotalSavings
            memberToEditTotalAssets = memberToEditTotalSavings + memberToEditShareCapital
        elif transToEditType == "Withdrawal from Savings" or transToEditType == "Special Deduction":
            transToEditTotalSavings = transToEditTotalSavings + (transToEditAmount - reqAmount)
        elif transToEditType == "Share Capital":
            transToEditTotalSavings = transToEditTotalSavings + (reqAmount - transToEditAmount)  

        transToEditAmount = reqAmount
        transToEditMonth = reqMonth
        transToEditType = reqType
        transToEditYear = reqYear
        details = transToEditType + " for " + transToEditMonth + ", " + transToEditYear
        date_last_modified = datetime.datetime.now()
        
        trans_data = (transToEdit['transID'], transToEditType, transToEditMonth, transToEditYear, \
            details, transToEditAmount, transToEditInterest, transToEditTotalSavings, transToEditLoanBalance, \
            transToEditDateCreated, date_last_modified, memberid, idToEdit)
        
        self.trans_db.update_transaction(trans_data)
        
        memberToEditLoanBalance = transToEditLoanBalance
        memberToEditTotalSavings = transToEditTotalSavings
        memberToEditTotalAssets = memberToEditTotalSavings + memberToEditShareCapital
        member_trans_data = (memberToEditTotalSavings, memberToEditTotalAssets, memberToEditLoanBalance, memberid)

        self.member_db.update_member_trans(member_trans_data)

        params = (idToEdit, memberid)
        
        editableTransactions = self.trans_db.get_editable_trans(params)
        
        for trans in editableTransactions:
            if trans['type'] == "Monthly Contribution" or trans['type'] == "Cash Deposit":
                if memberToEditLoanBalance == 0:
                    trans['interest'] = 0.0
                    trans['total_savings'] = memberToEditTotalSavings + trans['amount']
                    trans['loan_balance'] = memberToEditLoanBalance
                elif memberToEditLoanBalance > 0 and (memberToEditLoanBalance  < trans['amount']):
                    trans['interest'] = 0.01 * memberToEditLoanBalance
                    trans['loan_balance'] = 0.0
                    trans['total_savings'] = memberToEditTotalSavings + (trans['amount'] - (trans['interest'] + memberToEditLoanBalance))
                elif memberToEditLoanBalance > 0 and memberToEditLoanBalance > trans['amount']:
                    trans['interest'] = 0.01 * memberToEditLoanBalance
                    trans['total_savings'] = memberToEditTotalSavings
                    trans['loan_balance'] = memberToEditLoanBalance - (trans['amount'] - trans['interest'])
            elif trans['type'] == "Regular Loan" or trans['type'] == "Emergency Loan" or trans['type'] == "Special Loan":
                trans['total_savings'] = memberToEditTotalSavings
                trans['loan_balance'] = memberToEditLoanBalance + trans['amount']
            elif trans['type'] == "Withdrawal from Savings" or trans['type'] == "Special Deduction":
                trans['total_savings'] = memberToEditTotalSavings - trans['amount']
                trans['loan_balance'] = memberToEditLoanBalance
            elif trans['type'] == "Share Capital":
                trans['interest'] = 0.00
                trans['total_savings'] = memberToEditTotalSavings + trans['amount']
                trans['loan_balance'] = memberToEditLoanBalance

            memberToEditTotalSavings = trans['total_savings']
            memberToEditTotalAssets = memberToEditTotalSavings + memberToEditShareCapital
            memberToEditLoanBalance = trans['loan_balance']
            date_last_modified = datetime.datetime.now()
            transData = (trans['transID'], trans['type'], trans['month'], trans['year'], trans['details'], \
                        trans['amount'], trans['interest'], trans['total_savings'], trans['loan_balance'], \
                        trans['date_created'], date_last_modified, trans['member_id'], trans['trans_id'])
            member_trans_data = (memberToEditTotalSavings, memberToEditTotalAssets, memberToEditLoanBalance, memberid)
            self.trans_db.update_transaction(transData)               
            self.member_db.update_member_trans(member_trans_data)
        
        ui = MemberTransactions.ui
        id = MemberTransactions.memberid
        MemberTransactions.loadTransTable(ui, id)
        self.msgbox.close()
        self.close()
        # except:
            # print("An error occurred. Unable to delete the transaction")    

class HandleDeleteTrans(MsgBox):
    def __init__(self):
        super().__init__()  
        self.trans_db = Monthly_DB()
        self.member_db = Member_DB()

    def delete_trans(self, id):
        self.ui.messageTitle.setText("Delete Transaction?")
        self.ui.label.setText('''Are you sure you want to delete this transaction?''')
        self.ui.messageYesBtn.clicked.connect(lambda: self.delete_finally(id) )
        self.ui.messageNoBtn.clicked.connect(lambda: self.close() )
        self.exec()        
    
    def delete_finally(self, id):
        # try:
        transToDelete = self.trans_db.get_transaction((id,))
        memberid = transToDelete['member_id']
        memberToEdit = self.member_db.get_member((memberid,))
        idToDelete = transToDelete['trans_id']
        transToDeleteType = transToDelete['type']
        transToDeleteAmount = transToDelete['amount']
        transToDeleteLoanBalance = transToDelete['loan_balance']
        transToDeleteInterest = transToDelete['interest']
        transToDeleteTotalSavings = transToDelete['total_savings']
        memberToEditTotalSavings = memberToEdit['total_savings']
        memberToEditLoanBalance = memberToEdit['loan_balance']
        memberToEditTotalAssets = memberToEdit['total_assets']
        memberToEditShareCapital = memberToEdit['share_capital']
        if transToDeleteType == "Monthly Contribution" or transToDeleteType == "Cash Deposit":
            if transToDeleteLoanBalance == 0.0 and transToDeleteInterest == 0.0:
                memberToEditTotalSavings = transToDeleteTotalSavings - transToDeleteAmount
                memberToEditLoanBalance = 0.0
                memberToEditTotalAssets = memberToEditTotalSavings + memberToEditShareCapital
            elif transToDeleteLoanBalance == 0.0 and transToDeleteInterest > 0.0:
                memberToEditLoanBalance = transToDeleteInterest * 100
                memberToEditTotalSavings = transToDeleteTotalSavings - (transToDeleteAmount - transToDeleteInterest * 100 - transToDeleteInterest)
                memberToEditTotalAssets = memberToEditTotalSavings + memberToEditShareCapital
            elif transToDeleteLoanBalance > 0.0 and transToDeleteInterest > 0.0:
                memberToEditLoanBalance = transToDeleteInterest * 100
                memberToEditTotalSavings = transToDeleteTotalSavings
                memberToEditTotalAssets = memberToEditTotalSavings + memberToEditShareCapital
        elif transToDeleteType == "Regular Loan" or transToDeleteType == "Emergency Loan" or transToDeleteType == "Special Loan":
            memberToEditLoanBalance = transToDeleteLoanBalance - transToDeleteAmount
            memberToEditTotalSavings = transToDeleteTotalSavings
            memberToEditTotalAssets = memberToEditTotalSavings + memberToEditShareCapital
        elif transToDeleteType == "Withdrawal from Savings" or transToDeleteType == "Special Deduction":
            memberToEditTotalSavings = transToDeleteTotalSavings + transToDeleteAmount
            memberToEditTotalAssets = memberToEditTotalSavings + memberToEditShareCapital
        elif transToDeleteType == "Share Capital":
            memberToEditTotalSavings = transToDeleteTotalSavings - transToDeleteAmount
            memberToEditShareCapital = memberToEditShareCapital - transToDeleteAmount
            memberToEditTotalAssets = memberToEditTotalSavings + memberToEditShareCapital  

        member_trans_data =  (memberToEditTotalSavings, memberToEditTotalAssets, memberToEditLoanBalance, memberid)           

        self.member_db.update_member_trans(member_trans_data)

        params = (idToDelete, memberid)
        
        editableTransactions = self.trans_db.get_editable_trans(params)
        
        for trans in editableTransactions:
            if trans['type'] == "Monthly Contribution" or trans['type'] == "Cash Deposit":
                if memberToEditLoanBalance == 0:
                    trans['interest'] = 0.0
                    trans['total_savings'] = memberToEditTotalSavings + trans['amount']
                    trans['loan_balance'] = memberToEditLoanBalance
                elif memberToEditLoanBalance > 0 and (0.01 * memberToEditLoanBalance + memberToEditLoanBalance <= trans['amount']):
                    trans['interest'] = 0.01 * memberToEditLoanBalance
                    trans['loan_balance'] = 0.0
                    trans['total_savings'] = memberToEditTotalSavings + (trans['amount'] - (trans['interest'] + memberToEditLoanBalance))
                elif memberToEditLoanBalance > 0 and 0.01 * memberToEditLoanBalance + memberToEditLoanBalance > trans['amount']:
                    trans['interest'] = 0.01 * memberToEditLoanBalance
                    trans['total_savings'] = memberToEditTotalSavings
                    trans['loan_balance'] = memberToEditLoanBalance - (trans['amount'] - trans['interest'])
            elif trans['type'] == "Regular Loan" or trans['type'] == "Emergency Loan" or trans['type'] == "Special Loan":
                trans['total_savings'] = memberToEditTotalSavings
                trans['loan_balance'] = memberToEditLoanBalance + trans['amount']
            elif trans['type'] == "Withdrawal from Savings" or trans['type'] == "Special Deduction":
                trans['total_savings'] = memberToEditTotalSavings - trans['amount']
                trans['loan_balance'] = memberToEditLoanBalance
            elif trans['type'] == "Share Capital":
                trans['total_savings'] = memberToEditTotalSavings + trans['amount']
                trans['loan_balance'] = memberToEditLoanBalance

            memberToEditTotalSavings = trans['total_savings']
            memberToEditTotalAssets = memberToEditTotalSavings + memberToEditShareCapital
            memberToEditLoanBalance = trans['loan_balance']
            date_last_modified = datetime.datetime.now()
            transData = (trans['transID'], trans['type'], trans['month'], trans['year'], trans['details'], \
                        trans['amount'], trans['interest'], trans['total_savings'], trans['loan_balance'], \
                        trans['date_created'], date_last_modified, trans['member_id'], trans['trans_id'])
            member_trans_data = (memberToEditTotalSavings, memberToEditTotalAssets, memberToEditLoanBalance, memberid)
            self.trans_db.update_transaction(transData)               
            self.member_db.update_member_trans(member_trans_data)
        
        self.trans_db.remove_transaction((idToDelete,))
        ui = MemberTransactions.ui
        id = MemberTransactions.memberid
        MemberTransactions.loadTransTable(ui, id)
        self.close()
        # except:
            # print("An error occurred. Unable to delete the transaction")  

class HandleRefresh():
    def handle_table_dbl_click(self, table):
        index = table.selectionModel().currentIndex()
        value = index.sibling(index.row(), 9).data()
        # print(value)
        EditTransDialog().initialise_edit(value)
        # self.view_member.get_ui(ui, (value,))
    
    def refresh_trans(self, transactions):
       LoadTable().load_table(transactions)

class MemberTransactions(QMainWindow):
    def __init__(self):
        super().__init__()  
              
    @classmethod
    def loadTransTable(self, ui, id):
        self.member_db = Member_DB()
        self.trans_db = Monthly_DB()
        self.ui = ui
        self.memberid = id
        self.addSavingsDialog = None
                        
        # Initialise widgets      
        self.ui.searchTransTxt.setPlaceholderText("Search transactions by amount, date, details or id")
        self.ui.stackedWidget.setCurrentIndex(5)
        self.ui.memberTransTab.setCurrentIndex(0)

        self.transactions = self.trans_db.get_member_transactions(self.memberid)
        # print(self.transactions)
        self.member = self.member_db.get_member(self.memberid)
        self.memberID = self.member['memberID']
        self.ui.titleLbl.setText("Account Details - " + self.member['title'] + " " + self.member['fullname'])
        self.ui.montlySavingsLbl.setText(str(self.member['monthly_savings']))
        self.ui.totalSavingsLbl.setText(str(self.member['total_savings']))
        self.ui.shareCapitalLbl.setText(str(self.member['share_capital']))
        self.ui.totalAssetsLbl.setText(str(self.member['total_assets']))
        self.ui.commodityBalanceLbl.setText(str(self.member['commodity_balance']))
        self.ui.loanBalanceLbl.setText(str(self.member['loan_balance']))
        self.ui.addSavingsBtn.clicked.connect(lambda: AddSavingsDialog().initialise_add_savings(self.memberid))
        self.ui.addLoanBtn.clicked.connect(lambda: AddLoanDialog().initialise_add_loan(self.memberid))
        self.ui.makeWithdrawalBtn.clicked.connect(lambda: MakeWithdrawal().initialise_withdrawal(self.memberid))
        self.ui.refreshTransBtn.clicked.connect(lambda: HandleRefresh().refresh_trans(self.transactions))
        self.ui.searchTransBtn.clicked.connect(lambda: SearchTransactions().search_trans())
        self.ui.searchTransBtn.setStyleSheet("QPushButton::hover{background-color: #cce0ff;}")
        self.ui.changeMemberBtn.clicked.connect(lambda: ChangeMember().load_dialog())
        self.ui.searchTransTxt.textChanged.connect(lambda: SearchTransactions().search_trans())
        # self.ui.searchTransTxt.setPlaceholderText('Type search query and press enter')
        self.ui.searchTransTxt.returnPressed.connect(lambda: SearchTransactions().search_trans())
        self.ui.searchTransTxt.setClearButtonEnabled(True)
        LoadTable().load_table(self.transactions)

    def change_tab(self, i):
        if i == 1:
            self.ui.memberTransTab.setCurrentIndex(1)
            MemberCommodities().loadComTable(self.ui, self.memberid)
        elif i == 2:
            self.ui.memberTransTab.setCurrentIndex(2)
            MemberChristmas().loadXmasTable(self.ui, self.memberid)
        elif i == 3:
            self.ui.memberTransTab.setCurrentIndex(3)
            MemberEducational().loadEduTable(self.ui, self.memberid)
        elif i == 4:
            self.ui.memberTransTab.setCurrentIndex(4)
            MemberExit().loadExitTable(self.ui, self.memberid)

class LoadTable():
    def load_table(self, transactions):   
        # Initialise transaction table
        table = MemberTransactions.ui.monthlySavingsTable
        table.setObjectName("transTable")
        table.setRowCount(len(transactions))
        table.setColumnCount(10)
        table.setHorizontalHeaderLabels(["Transaction ID", "Date Created", "Details", "Amount", "Interest Paid", "Loan Balance", "Total Savings", "Last Updated", "", ""])
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.doubleClicked.connect(lambda: HandleRefresh().handle_table_dbl_click(table))  
        table.setColumnHidden(9, True)  
     
        header = table.horizontalHeader()
        vert = table.verticalHeader()
        # header.setDefaultAlignment(Qt.AlignLeft)
        # header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setStretchLastSection(False)  
        vert.setSectionResizeMode(QHeaderView.ResizeToContents)

        row = 0
        for trans in transactions:
            table.setItem(row, 0, QTableWidgetItem(trans['transID']))
            table.setItem(row, 1, QTableWidgetItem(trans['date_created']))
            table.setItem(row, 2, QTableWidgetItem(trans['details']))
            table.setItem(row, 3, QTableWidgetItem(str(trans['amount'])))
            table.setItem(row, 4, QTableWidgetItem(str(trans['interest'])))
            table.setItem(row, 5, QTableWidgetItem(str(trans['loan_balance'])))
            table.setItem(row, 6, QTableWidgetItem(str(trans['total_savings'])))
            table.setItem(row, 7, QTableWidgetItem(trans['date_last_modified']))
            table.setStyleSheet("QPushButton::hover{background-color: #cce0ff;}")
            edit_button = QPushButton()
            delete_button = QPushButton()
            edit_button.setIcon(QIcon('./static/icon/blue/edit.svg'))
            delete_button.setIcon(QIcon('./static/icon/red/trash-2.svg'))
            edit_button.setToolTip("Edit Transaction")
            delete_button.setToolTip("Delete Transaction")
            edit_button.clicked.connect(partial(EditTransDialog().initialise_edit, trans['trans_id']))
            delete_button.clicked.connect(partial(HandleDeleteTrans().delete_trans, trans['trans_id']))
            hbox = QHBoxLayout(table)
            widg = QWidget()
            hbox.addWidget(edit_button)
            hbox.addWidget(delete_button)
            widg.setLayout(hbox)
            table.setCellWidget(row, 8, widg)
            table.setItem(row, 9, QTableWidgetItem(str(trans['trans_id'])))
            row += 1        
    
class SearchTransactions():
    def search_trans(self):
        searchText = (MemberTransactions.ui.searchTransTxt.text()).lower()
        if searchText == "":
            LoadTable().load_table(MemberTransactions.transactions)
        else:
            new_trans = [trans for trans in MemberTransactions.transactions if searchText in (trans['month']).lower() or \
            searchText in (str(trans['amount'])).lower() or searchText in (trans['year']).lower() or \
            searchText in (trans['date_created']).lower() or searchText in (trans['date_last_modified']).lower() or \
            searchText in (trans['details']).lower() or searchText in (str(trans['total_savings'])).lower()]

            if new_trans == []:
                LoadTable().load_table(MemberTransactions.transactions)
            else:
                LoadTable().load_table(new_trans)


class ChangeMember(QDialog):
    def __init__(self):
        super().__init__()
    
    def load_dialog(self):
        self.dialog = Search_Dialog()
        self.dialog.setupUi(self)
        self.member_db = Member_DB()
        self.members = self.member_db.get_searched_members()
        self.dialog.membersList.clear()
        self.dialog.membersList.setVisible(False)
        self.dialog.searchMemberTxt.returnPressed.connect(self.search_member)
        self.dialog.searchMemberTxt.textChanged.connect(self.search_member)
        self.dialog.searchMemberTxt.setClearButtonEnabled(True)
        self.dialog.membersList.itemClicked.connect(self.change_member)
        self.exec_()
    
    def search_member(self):
        self.dialog.membersList.clear()
        self.dialog.membersList.setVisible(False)
        searchText = (self.dialog.searchMemberTxt.text()).lower()
        if searchText == "":
            self.dialog.membersList.clear()
        else:
            new_member = [member['fullname'] + " - " + (str(member['member_id'])) for member in self.members if searchText in (member['fullname']).lower() or \
                searchText in (str(member['memberID'])).lower() or searchText in (member['ledger_no']).lower()]
            
            if new_member == []:
                self.dialog.membersList.setVisible(True)
                self.dialog.membersList.addItems(["No member found"])
            else:
                self.dialog.membersList.setVisible(True)
                self.dialog.membersList.addItems(new_member)
    
    def change_member(self, item):
        item = item.text()
        id = item[-1]
        ui = MemberTransactions.ui
        memberid = id
        MemberTransactions.loadTransTable(ui, memberid)
        self.close()


    
        



   
    
    

