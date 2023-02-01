from PyQt5.QtWidgets import QMainWindow
import sys
sys.path.insert(0, 'C:/Python Apps/FOPAJ/data')
from dummyData import transactions
from data.members import Member_DB
from member_transactions import MemberTransactions
from edit_member import EditMember


class ViewMember(QMainWindow):
    def __init__(self):
        super().__init__() 
        self.edit_member = EditMember()
        self.member_trans = MemberTransactions()

    def get_ui(self, ui, id):
        self.db = Member_DB()
        self.ui = ui
        self.id = id
        print(self.id)
        self.member = self.db.get_member((self.id,))
        self.ui.stackedWidget.setCurrentIndex(3)

        # Set the current page to Member's detail page
        self.initialise_widgets()

    def initialise_widgets(self):
        # Initialise Widgets
        self.ui.profNameTitle.setText(self.member['fullname'] + ' - ' + self.member['memberID'])
        self.ui.profFullNameLbl.setText(self.member['fullname'])
        self.ui.profMemberIDLbl.setText(self.member['memberID'])
        self.ui.profLedgerNoLbl.setText(self.member['ledger_no'])
        self.ui.profStaffNoLbl.setText(self.member['staff_no'])
        self.ui.profDateEnrolledLbl.setText(self.member['date_enrolled'])
        self.ui.profGenderLbl.setText(self.member['gender'])
        self.ui.profDobLbl.setText(self.member['dob'])
        self.ui.profPhoneNoLbl.setText(self.member['phone_no'])
        self.ui.profEmailLbl.setText(self.member['email'])
        self.ui.profContactLbl.setText(self.member['contact'])

        # Connect Signals and Slots
        self.ui.memberListBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.editMemberBtn.clicked.connect(lambda: self.edit_member.get_data(self.ui, self.id))
        self.ui.getTransBtn.clicked.connect(lambda: self.member_trans.loadTransTable(self.ui, (self.id,)))
        # self.ui.profDateEnrolledLbl.setText(self.member[7])

    