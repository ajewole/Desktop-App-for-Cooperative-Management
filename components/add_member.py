from PyQt5.QtWidgets import QMainWindow, QLineEdit, QFileDialog
from PyQt5.QtGui import QPixmap
import sys
sys.path.insert(0, 'C:/Python Apps/FOPAJ/data')
from dummyData import transactions
from data.members import Member_DB
import random
import datetime
from list_members import ListMembers

class AddMember(QMainWindow):
    def __init__(self):
        super().__init__() 
        self.db = Member_DB()
    
    def load_ui(self, ui):
        # Initialise widgets
        self.ui = ui
        self.nextPageBtn = self.ui.nextPageBtn
        self.nokPrevPageBtn = self.ui.nokPrevPageBtn
        self.nokNextPageBtn = self.ui.nokNextPageBtn
        self.acctPrevPageBtn = self.ui.acctPrevPageBtn
        self.resetFormBtn = self.ui.resetFormBtn
        self.cancelFormBtn = self.ui.cancelFormBtn
        self.submitFormBtn = self.ui.submitFormBtn
        self.personalClearBtn = self.ui.personalClearBtn
        self.nokClearBtn = self.ui.nokClearBtn
        self.accountClearBtn = self.ui.accountClearBtn
        
        self.pages = self.ui.stackedWidget
        self.addMemberTab = self.ui.addMemberTab
        self.personalTab = self.ui.personalTab
        self.nokTab = self.ui.nokTab
        self.accountTab = self.ui.accountTab
        self.backToMemberListBtn = self.ui.backToMemberListBtn

        self.uploadPicBtn = self.ui.uploadPicBtn
        self.picLabel = self.ui.picLabel
        self.picNameLabel = self.ui.picNameLabel

        # Set page
        self.ui.stackedWidget.setCurrentIndex(2)

        # Set initial tab
        self.addMemberTab.setCurrentIndex(0)

        # Set New Member ID
        randNo = random.randint(1000, 10000)
        self.ui.memberIDTxt.setText('FOPAJ' + str(randNo))
        self.ui.memberIDTxt.isReadOnly()
        self.ui.memberIDTxt.setDisabled(True)

        # Add Member Page Signals
        self.uploadPicBtn.clicked.connect(lambda: self.upload_picture(self.picLabel, self.picNameLabel))
        self.resetFormBtn.clicked.connect(lambda: self.reset_form(self.ui))
        self.personalClearBtn.clicked.connect(lambda: self.clear_page(self.addMemberTab.widget(0), self.ui))
        self.nokClearBtn.clicked.connect(lambda: self.clear_page(self.addMemberTab.widget(1), self.ui))
        self.accountClearBtn.clicked.connect(lambda: self.clear_page(self.addMemberTab.widget(2), self.ui))
        self.backToMemberListBtn.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        
        self.submitFormBtn.clicked.connect(lambda: self.submit_form(self.ui))     
        self.nextPageBtn.clicked.connect(lambda: self.change_tabs("nextPageBtn"))
        self.nokPrevPageBtn.clicked.connect(lambda: self.change_tabs("nokPrevPageBtn"))
        self.nokNextPageBtn.clicked.connect(lambda: self.change_tabs("nokNextPageBtn"))
        self.acctPrevPageBtn.clicked.connect(lambda: self.change_tabs("acctPrevPageBtn"))    



    # Upload member picture    
    def upload_picture(self, picLabel, picNameLabel):
        fname = QFileDialog.getOpenFileName(self, 'Select Picture', 'C\\', 'Image Files(*.jpg *.gif *.png)')
        imagePath = fname[0]
        pixmap = QPixmap(imagePath)
        picLabel.setPixmap(QPixmap(pixmap))
        picLabel.setScaledContents(True)
        picNameLabel.setText(imagePath)
    
    # Clear add member form data
    def reset_form(self, ui):
        for widg in ui.addMemberPage.findChildren(QLineEdit):
            widg.clear()
        ui.addMemberTab.setCurrentIndex(0)
        randNo = random.randint(1000, 10000)
        ui.memberIDTxt.setText('FOPAJ' + str(randNo))       

    
    def clear_page(self, tab, ui):
        id = ui.memberIDTxt.text()
        for widg in tab.findChildren(QLineEdit):
            widg.clear()
        ui.memberIDTxt.setText(id)
    
    def change_tabs(self, btn_text):
        if btn_text == "nextPageBtn":
            self.addMemberTab.setCurrentIndex(1)
        elif btn_text == "nokPrevPageBtn":
            self.addMemberTab.setCurrentIndex(0)
        elif btn_text == "nokNextPageBtn":
            self.addMemberTab.setCurrentIndex(2)
        elif btn_text == "acctPrevPageBtn":
            self.addMemberTab.setCurrentIndex(1)
        else:
            self.addMemberTab.setCurrentIndex(0)

    
    def submit_form(self, ui):
        memberID = self.ui.memberIDTxt.text().strip()
        ledgerNo = self.ui.ledgerNoTxt.text().strip()
        staffNo = self.ui.staffNoTxt.text().strip()
        title = self.ui.titleCombo.currentText().strip()
        surname = self.ui.surnameTxt.text().strip()
        firstname = self.ui.firstnameTxt.text().strip()
        othername = self.ui.othernameTxt.text().strip()
        gender = self.ui.genderCombo.currentText().strip()
        dob = self.ui.dobDateEdit.text().strip()
        phoneNo = self.ui.phoneNoTxt.text().strip()
        email = self.ui.emailTxt.text().strip()
        contact = self.ui.contactTxt.text().strip()
        department = self.ui.deptCombo.currentText().strip()
        designation = self.ui.designationTxt.text().strip()
        salaryGrade = self.ui.salaryGradeTxt.text().strip()
        bankName = self.ui.bankNameCombo.currentText().strip()
        accountNo = self.ui.accountNoTxt.text().strip()
        accountType = self.ui.accountTypeCombo.currentText().strip()
        doa = self.ui.doaDateEdit.text().strip()
        date_enrolled = datetime.datetime.now()
        date_last_modified = date_enrolled
        
        nokTitle = self.ui.nokTitleCombo.currentText().strip()
        nokSurname = self.ui.nokSurnameTxt.text().strip()
        nokFirstname = self.ui.nokFirstnameTxt.text().strip()
        nokOthername = self.ui.nokOthernameTxt.text().strip()
        nokGender = self.ui.nokGenderCombo.currentText().strip()
        nokPhoneNo = self.ui.nokPhoneNoTxt.text().strip()
        nokEmail = self.ui.nokEmailTxt.text().strip()
        nokJobStatus = self.ui.nokJobStatusTxt.text().strip()
        nokContact = self.ui.nokContactTxt.text().strip()
        nokWorkPlace = self.ui.nokWorkPlaceTxt.text().strip()

        g1Surname = self.ui.g1SurnameTxt.text().strip()
        g1Firstname = self.ui.g1FirstnameTxt.text().strip()
        g1Othername = self.ui.g1OthernameTxt.text().strip()
        g1PhoneNo = self.ui.g1PhoneNoTxt.text().strip()
        g1Email = self.ui.g1EmailTxt.text().strip()
        g1Contact = self.ui.g1ContactTxt.text().strip()

        g2Surname = self.ui.g2SurnameTxt.text().strip()
        g2Firstname = self.ui.g2FirstnameTxt.text().strip()
        g2Othername = self.ui.g2OthernameTxt.text().strip()
        g2PhoneNo = self.ui.g2PhoneNoTxt.text().strip()
        g2Email = self.ui.g2EmailTxt.text().strip()
        g2Contact = self.ui.g2ContactTxt.text().strip() 

        monthlySavings = float(self.ui.monthlyDoubleSpinBox.value())
        xmasSavings = float(self.ui.xmasDoubleSpinBox.value())
        eduSavings = float(self.ui.eduDoubleSpinBox.value())
        exitSavings = float(self.ui.exitDoubleSpinBox.value())

        fullname = surname + " " + firstname + " " + othername
        nokFullname = nokSurname + " " + nokFirstname + " " + nokOthername
        entranceFee = 5000
        shareCapital = 10000
        totalSavings = monthlySavings - entranceFee - shareCapital 
        totalAssets = shareCapital + totalSavings
        totalXmas = xmasSavings
        totalEdu = eduSavings
        totalExit = exitSavings
        loanBalance = 0.00
        commodityPayment = 0.00
        commodityBalance = 0.00

        member_data = (memberID, ledgerNo, staffNo, title, surname, firstname, \
                    othername, fullname, gender, dob, phoneNo, email, contact, \
                    department, designation, salaryGrade, bankName, accountNo, accountType, doa, date_enrolled, \
                    date_last_modified, nokTitle, nokSurname, nokFirstname, nokOthername, nokFullname, nokGender, \
                    nokPhoneNo, nokEmail, nokJobStatus, nokContact, nokWorkPlace, \
                    g1Surname, g1Firstname, g1Othername, g1PhoneNo, g1Email, g1Contact, \
                    g2Surname, g2Firstname, g2Othername, g2PhoneNo, g2Email, g2Contact,
                    monthlySavings, shareCapital, xmasSavings, eduSavings, exitSavings, totalSavings, \
                    totalAssets, totalEdu, totalExit, totalXmas, loanBalance, commodityPayment, \
                    commodityBalance, entranceFee)
        self.db.add_member(member_data)
        self.reset_form(ui)
        # ListMembers().get_members()
        ListMembers().loadMembersTable(ui)

        # print(date_enrolled)



        

       


