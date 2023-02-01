# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\search_members.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(514, 236)
        Dialog.setStyleSheet("QDialog {\n"
"    background-color: #ffffff;\n"
"}\n"
"\n"
"#searchMemberTxt{\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #c4c4c4;\n"
"    border-radius: 5px;\n"
"    text-align: left;\n"
"    width: 200px;\n"
"    height: 30px\n"
"}\n"
"\n"
"#membersList {\n"
"    border: none;\n"
"    background-color: #ffffff;\n"
"}\n"
"\n"
"#membersList:item:hover {\n"
"    background-color: #385723;\n"
"    color: #ffffff;\n"
"    border-radius: 5px;\n"
"    font-weight: bold;\n"
"}")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(170, 20, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.searchMemberTxt = QtWidgets.QLineEdit(Dialog)
        self.searchMemberTxt.setGeometry(QtCore.QRect(80, 70, 361, 30))
        self.searchMemberTxt.setMinimumSize(QtCore.QSize(0, 30))
        self.searchMemberTxt.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.searchMemberTxt.setFont(font)
        self.searchMemberTxt.setObjectName("searchMemberTxt")
        self.membersList = QtWidgets.QListWidget(Dialog)
        self.membersList.setGeometry(QtCore.QRect(80, 110, 361, 111))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.membersList.setFont(font)
        self.membersList.setObjectName("membersList")
        item = QtWidgets.QListWidgetItem()
        self.membersList.addItem(item)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Search Members"))
        self.searchMemberTxt.setPlaceholderText(_translate("Dialog", "Type name, id, or ledger no and press enter"))
        __sortingEnabled = self.membersList.isSortingEnabled()
        self.membersList.setSortingEnabled(False)
        item = self.membersList.item(0)
        item.setText(_translate("Dialog", "Ajewole Peter Oluwole"))
        self.membersList.setSortingEnabled(__sortingEnabled)