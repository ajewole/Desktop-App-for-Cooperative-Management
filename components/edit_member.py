from PyQt5.QtWidgets import QMainWindow, QLineEdit, QFileDialog
from PyQt5.QtGui import QPixmap
import sys
sys.path.insert(0, 'C:/Python Apps/FOPAJ/data')
from dummyData import transactions
from members import Member_DB
import random
import datetime
import components

class EditMember(QMainWindow):
    def __init__(self):
        super().__init__() 
        self.db = Member_DB()
    
    def get_data(self, ui, id):
        self.ui = ui
        self.id = id
        self.member = self.db.get_member((self.id,))
        self.ui.stackedWidget.setCurrentIndex(4)
        self.ui.editMemberTab.setCurrentIndex(0)
        
        # Edit Member Page Signals
        self.ui.nextPageBtn_2.clicked.connect(lambda: self.change_tabs("nextPageBtn"))
        self.ui.nokPrevPageBtn_2.clicked.connect(lambda: self.change_tabs("nokPrevPageBtn"))
        self.ui.nokNextPageBtn_2.clicked.connect(lambda: self.change_tabs("nokNextPageBtn"))
        self.ui.acctPrevPageBtn_2.clicked.connect(lambda: self.change_tabs("acctPrevPageBtn"))

        
        self.ui.uploadPicBtn_2.clicked.connect(lambda: self.upload_picture(self.picLabel, self.picNameLabel))
        self.ui.resetFormBtn_2.clicked.connect(lambda: self.reset_form(self.ui))
        self.ui.personalClearBtn_2.clicked.connect(lambda: self.clear_page(self.ui.editMemberTab.widget(0), self.ui))
        self.ui.nokClearBtn_2.clicked.connect(lambda: self.clear_page(self.ui.editMemberTab.widget(1), self.ui))
        self.ui.accountClearBtn_2.clicked.connect(lambda: self.clear_page(self.ui.editMemberTab.widget(2), self.ui))
        self.ui.submitFormBtn_2.clicked.connect(lambda: self.submit_form(self.ui)) 
        self.ui.backToMemberListBtn_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))

        self.ui.editMemberTitle.setText('Edit Member Details - ' + self.member['fullname'])
        self.ui.memberIDTxt_2.setText(self.member['memberID'])
        self.ui.ledgerNoTxt_2.setText(self.member['ledger_no'])
        self.ui.staffNoTxt_2.setText(self.member['staff_no'])
        self.ui.titleCombo_2.setCurrentText(self.member['title'])
        self.ui.surnameTxt_2.setText(self.member['surname'])
        self.ui.firstnameTxt_2.setText(self.member['firstname'])
        self.ui.othernameTxt_2.setText(self.member['othername'])
        self.ui.genderCombo_2.setCurrentText(self.member['gender'])
        # dob = self.ui.dobDateEdit.setDate(self.member[0])
        self.ui.phoneNoTxt_2.setText(self.member['phone_no'])
        self.ui.emailTxt_2.setText(self.member['email'])
        self.ui.contactTxt_2.setText(self.member['contact'])
        self.ui.deptCombo_2.setCurrentText(self.member['dept'])
        self.ui.designationTxt_2.setText(self.member['designation'])
        self.ui.salaryGradeTxt_2.setText(self.member['salary'])
        self.ui.bankNameCombo_2.setCurrentText(self.member['bank_name'])
        self.ui.accountNoTxt_2.setText(self.member['account_no'])
        self.ui.accountTypeCombo_2.setCurrentText(self.member['account_type'])
        # doa = self.ui.doaDateEdit.setDate(self.member[0])
    
        
        self.ui.nokTitleCombo_2.setCurrentText(self.member['nok_title'])
        self.ui.nokSurnameTxt_2.setText(self.member['nok_surname'])
        self.ui.nokFirstnameTxt_2.setText(self.member['nok_firstname'])
        self.ui.nokOthernameTxt_2.setText(self.member['nok_othername'])
        self.ui.nokGenderCombo_2.setCurrentText(self.member['nok_gender'])
        self.ui.nokPhoneNoTxt_2.setText(self.member['nok_phone_no'])
        self.ui.nokEmailTxt_2.setText(self.member['nok_email'])
        self.ui.nokJobStatusTxt_2.setText(self.member['nok_job_status'])
        self.ui.nokContactTxt_2.setText(self.member['nok_contact'])
        self.ui.nokWorkPlaceTxt_2.setText(self.member['nok_work_place'])

        self.ui.g1SurnameTxt_2.setText(self.member['g1_surname'])
        self.ui.g1FirstnameTxt_2.setText(self.member['g1_firstname'])
        self.ui.g1OthernameTxt_2.setText(self.member['g1_othername'])
        self.ui.g1PhoneNoTxt_2.setText(self.member['g1_phone_no'])
        self.ui.g1EmailTxt_2.setText(self.member['g1_email'])
        self.ui.g1ContactTxt_2.setText(self.member['g1_contact'])

        self.ui.g2SurnameTxt_2.setText(self.member['g2_surname'])
        self.ui.g2FirstnameTxt_2.setText(self.member['g2_firstname'])
        self.ui.g2OthernameTxt_2.setText(self.member['g2_othername'])
        self.ui.g2PhoneNoTxt_2.setText(self.member['g2_phone_no'])
        self.ui.g2EmailTxt_2.setText(self.member['g2_email'])
        self.ui.g2ContactTxt_2.setText(self.member['g2_contact'])


        self.ui.monthlyDoubleSpinBox.setValue(float(self.member['monthly_savings']))
        self.ui.xmasDoubleSpinBox.setValue(float(self.member['xmas_savings']))
        self.ui.eduDoubleSpinBox.setValue(float(self.member['edu_savings']))
        self.ui.exitDoubleSpinBox.setValue(float(self.member['exit_savings'])) 

    def change_pages(self, btn):
        btn_text = btn.text().strip()
        if btn_text == self.dashboardBtn.text().strip():
            self.ui.stackedWidget.setCurrentIndex(0)
        elif btn_text == self.membersBtn.text().strip():
            self.ui.stackedWidget.setCurrentIndex(1)
        else:
            self.ui.stackedWidget.setCurrentIndex(0)

    def change_tabs(self, btn_text):
        if btn_text == "nextPageBtn":
            self.ui.editMemberTab.setCurrentIndex(1)
        elif btn_text == "nokPrevPageBtn":
            self.ui.editMemberTab.setCurrentIndex(0)
        elif btn_text == "nokNextPageBtn":
            self.ui.editMemberTab.setCurrentIndex(2)
        elif btn_text == "acctPrevPageBtn":
            self.ui.editMemberTab.setCurrentIndex(1)
        else:
            self.ui.editMemberTab.setCurrentIndex(0)

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
        for widg in ui.editMemberPage.findChildren(QLineEdit):
            widg.clear()
        ui.editMemberTab.setCurrentIndex(0)
        randNo = random.randint(1000, 10000)
        ui.memberIDTxt_2.setText('FOPAJ' + str(randNo))       

    
    def clear_page(self, tab, ui):
        id = ui.memberIDTxt_2.text()
        for widg in tab.findChildren(QLineEdit):
            widg.clear()
        ui.memberIDTxt_2.setText(id)
    
    def submit_form(self, ui):
        id = self.id
        memberID = ui.memberIDTxt_2.text().strip()
        ledgerNo = ui.ledgerNoTxt_2.text().strip()
        staffNo = ui.staffNoTxt_2.text().strip()
        title = ui.titleCombo_2.currentText().strip()
        surname = ui.surnameTxt_2.text().strip()
        firstname = ui.firstnameTxt_2.text().strip()
        othername = ui.othernameTxt_2.text().strip()
        gender = ui.genderCombo_2.currentText().strip()
        dob = ui.dobDateEdit.text().strip()
        phoneNo = ui.phoneNoTxt_2.text().strip()
        email = ui.emailTxt_2.text().strip()
        contact = ui.contactTxt_2.text().strip()
        department = ui.deptCombo_2.currentText().strip()
        designation = ui.designationTxt_2.text().strip()
        salaryGrade = ui.salaryGradeTxt_2.text().strip()
        bankName = ui.bankNameCombo_2.currentText().strip()
        accountNo = ui.accountNoTxt_2.text().strip()
        accountType = ui.accountTypeCombo_2.currentText().strip()
        doa = ui.doaDateEdit.text().strip()
        date_last_modified = datetime.date.now()
        
        nokTitle = ui.nokTitleCombo_2.currentText().strip()
        nokSurname = ui.nokSurnameTxt_2.text().strip()
        nokFirstname = ui.nokFirstnameTxt_2.text().strip()
        nokOthername = ui.nokOthernameTxt_2.text().strip()
        nokGender = ui.nokGenderCombo_2.currentText().strip()
        nokPhoneNo = ui.nokPhoneNoTxt_2.text().strip()
        nokEmail = ui.nokEmailTxt_2.text().strip()
        nokJobStatus = ui.nokJobStatusTxt_2.text().strip()
        nokContact = ui.nokContactTxt_2.text().strip()
        nokWorkPlace = ui.nokWorkPlaceTxt_2.text().strip()

        g1Surname = ui.g1SurnameTxt_2.text().strip()
        g1Firstname = ui.g1FirstnameTxt_2.text().strip()
        g1Othername = ui.g1OthernameTxt_2.text().strip()
        g1PhoneNo = ui.g1PhoneNoTxt_2.text().strip()
        g1Email = ui.g1EmailTxt_2.text().strip()
        g1Contact = ui.g1ContactTxt_2.text().strip()

        g2Surname = ui.g2SurnameTxt_2.text().strip()
        g2Firstname = ui.g2FirstnameTxt_2.text().strip()
        g2Othername = ui.g2OthernameTxt_2.text().strip()
        g2PhoneNo = ui.g2PhoneNoTxt_2.text().strip()
        g2Email = ui.g2EmailTxt_2.text().strip()
        g2Contact = ui.g2ContactTxt_2.text().strip() 

        monthlySavings = float(ui.monthlyDoubleSpinBox.value())
        xmasSavings = float(ui.xmasDoubleSpinBox.value())
        eduSavings = float(ui.eduDoubleSpinBox.value())
        exitSavings = float(ui.exitDoubleSpinBox.value())

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

        member_data = (ledgerNo, staffNo, title, surname, firstname, \
                    othername, fullname, gender, dob, phoneNo, email, contact, \
                    department, designation, salaryGrade, bankName, accountNo, accountType, doa, \
                    date_last_modified, nokTitle, nokSurname, nokFirstname, nokOthername, nokFullname, nokGender, \
                    nokPhoneNo, nokEmail, nokJobStatus, nokContact, nokWorkPlace, \
                    g1Surname, g1Firstname, g1Othername, g1PhoneNo, g1Email, g1Contact, \
                    g2Surname, g2Firstname, g2Othername, g2PhoneNo, g2Email, g2Contact,
                    monthlySavings, xmasSavings, eduSavings, exitSavings, totalSavings, \
                    totalAssets, totalEdu, totalExit, totalXmas, loanBalance, commodityPayment, \
                    commodityBalance, id)
        self.db.update_member(member_data)
        # self.ui.stackedWidget.setCurrentIndex(1)
        from components.list_members import ListMembers
        ListMembers().loadMembersTable(ui)


        

       


