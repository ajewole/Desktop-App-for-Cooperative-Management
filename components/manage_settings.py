from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer
import sys, datetime
sys.path.insert(0, 'C:/Python Apps/FOPAJ/data')
from settings import Settings_DB
from message import MsgBox
from alert import Alert


class ManageSettings(QMainWindow):
    def __init__(self):
        super().__init__() 

    def get_ui(self, ui):
        self.db = Settings_DB()
        self.ui = ui
        self.settings = self.db.get_settings()
        self.ui.stackedWidget.setCurrentIndex(7)
        self.btn_text = self.ui.editSettingsBtn.text()

        # Set the current page to Member's detail page
        self.initialise_widgets()

    def initialise_widgets(self):
        # Initialise Widgets
        self.ui.appNamePlainTxt.setPlainText(self.settings['app_name'])
        self.ui.interestRateDblSpin.setValue(float(self.settings['interest_rate']))
        self.ui.entranceFeeDblSpin.setValue(float(self.settings['entrance_fee']))
        self.ui.minShareCapitalDblSpin.setValue(float(self.settings['share_capital']))
        self.ui.minMonthlySavingsDblSpin.setValue(float(self.settings['monthly_savings']))
        self.ui.minXmasSavingsDblSpin.setValue(float(self.settings['xmas_savings']))
        self.ui.minEduSavingsDblSpin.setValue(float(self.settings['edu_savings']))
        self.ui.minExitSavingsDblSpin.setValue(float(self.settings['exit_savings']))
        self.ui.updateSettingsBtn.setVisible(False)

        # Connect Signals and Slots
        self.ui.editSettingsBtn.clicked.connect(self.edit_settings)
        self.ui.cancelEditSettingsBtn.clicked.connect(self.cancel_edit)
        self.ui.updateSettingsBtn.clicked.connect(self.start_update)
        # self.ui.getTransBtn.clicked.connect(lambda: self.member_trans.loadTransTable(self.ui, (self.id,)))
        # self.ui.profDateEnrolledLbl.setText(self.member[7])

    def disable_widgets(self):
        self.ui.appNamePlainTxt.setDisabled(True)
        self.ui.interestRateDblSpin.setDisabled(True)
        self.ui.entranceFeeDblSpin.setDisabled(True)
        self.ui.minShareCapitalDblSpin.setDisabled(True)
        self.ui.minMonthlySavingsDblSpin.setDisabled(True)
        self.ui.minXmasSavingsDblSpin.setDisabled(True)
        self.ui.minEduSavingsDblSpin.setDisabled(True)
        self.ui.minExitSavingsDblSpin.setDisabled(True)
        self.ui.editSettingsBtn.setVisible(True)
        self.ui.updateSettingsBtn.setVisible(False)
        
    def edit_settings(self):
        self.ui.appNamePlainTxt.setDisabled(False)
        self.ui.interestRateDblSpin.setDisabled(False)
        self.ui.entranceFeeDblSpin.setDisabled(False)
        self.ui.minShareCapitalDblSpin.setDisabled(False)
        self.ui.minMonthlySavingsDblSpin.setDisabled(False)
        self.ui.minXmasSavingsDblSpin.setDisabled(False)
        self.ui.minEduSavingsDblSpin.setDisabled(False)
        self.ui.minExitSavingsDblSpin.setDisabled(False)
        self.ui.editSettingsBtn.setVisible(False)
        self.ui.updateSettingsBtn.setVisible(True)

    def start_update(self):
        self.msgbox = MsgBox()
        self.msgbox.ui.label.setText("Are you sure you want to make changes to the app settings? The changes will be effected across the whole application!")
        self.msgbox.ui.messageTitle.setText("Edit Settings?")
        
        self.msgbox.ui.messageYesBtn.clicked.connect(self.update_settings)
        self.msgbox.ui.messageNoBtn.clicked.connect(self.msgbox.close)
        self.msgbox.show()
        # self.msgbox.exec_()
        self.ui.editSettingsBtn.setText('Edit Settings')
    
    def update_settings(self):
        app_name = self.ui.appNamePlainTxt.toPlainText().strip()
        app_logo = self.settings['app_logo']
        interest_rate = float(self.ui.interestRateDblSpin.value())
        entrance_fee = float(self.ui.entranceFeeDblSpin.value())
        share_capital = float(self.ui.minShareCapitalDblSpin.value())
        monthly_savings = float(self.ui.minMonthlySavingsDblSpin.value())
        xmas_savings = float(self.ui.minXmasSavingsDblSpin.value())
        edu_savings = float(self.ui.minEduSavingsDblSpin.value())
        exit_savings = float(self.ui.minExitSavingsDblSpin.value())
        date_last_modified = datetime.datetime.now()

        settings_data = (app_name, app_logo, interest_rate, entrance_fee, share_capital, monthly_savings, xmas_savings, \
                edu_savings, exit_savings, date_last_modified)
        self.db.update_setting(settings_data)
        self.alert = Alert()
        self.alert.ui.messageLbl.setStyleSheet("color: #00331F")
        self.alert.ui.messageLbl.setText("The application settings have been updated successfully")
        self.alert.ui.OKBtn.clicked.connect(self.alert.close)
        QTimer.singleShot(1500, self.close_alert)
        self.alert.exec_()
        self.disable_widgets()
        self.msgbox.close()   
        self.ui.stackedWidget.setCurrentIndex(0)
    
    def close_alert(self):
        self.alert.close()
    
    def cancel_edit(self):
        pass


    