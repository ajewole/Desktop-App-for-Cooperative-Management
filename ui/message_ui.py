# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\message.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(477, 228)
        Dialog.setStyleSheet("#messageFrame {\n"
"    background-color: #ffffff;\n"
"}\n"
"\n"
"#messageFrame QPushButton:pressed{\n"
"    padding-left: 15px;\n"
"}\n"
"\n"
"#messageYesBtn, #messageNoBtn {\n"
"    border: none;\n"
"    border-radius: 3px;\n"
"    padding: 5px 10px;\n"
"    font-size: 14px;\n"
"    padding: 5px 10px;\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"#messageYesBtn {\n"
"    background-color: #0d6efd;\n"
"}\n"
"\n"
"#messageNoBtn {\n"
"    background-color: #dc3545 ;\n"
"}\n"
"\n"
"#messageYesBtn:hover, #messageYesBtn:pressed {\n"
"    background-color: #001f4d;\n"
"}\n"
"\n"
"#messageNoBtn:hover, #messageNoBtn:pressed {\n"
"    background-color: #b30000;\n"
"}\n"
"\n"
"#messageIconBtn {\n"
"    background-color: #ffffff;\n"
"    border: none;\n"
"}\n"
"\n"
"")
        self.messageFrame = QtWidgets.QFrame(Dialog)
        self.messageFrame.setGeometry(QtCore.QRect(0, 0, 481, 241))
        self.messageFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.messageFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.messageFrame.setObjectName("messageFrame")
        self.messageTitle = QtWidgets.QLabel(self.messageFrame)
        self.messageTitle.setGeometry(QtCore.QRect(70, 10, 341, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.messageTitle.setFont(font)
        self.messageTitle.setObjectName("messageTitle")
        self.layoutWidget = QtWidgets.QWidget(self.messageFrame)
        self.layoutWidget.setGeometry(QtCore.QRect(130, 160, 261, 32))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.messageYesBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.messageYesBtn.setMinimumSize(QtCore.QSize(0, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icon/white/check-circle.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.messageYesBtn.setIcon(icon)
        self.messageYesBtn.setObjectName("messageYesBtn")
        self.horizontalLayout_11.addWidget(self.messageYesBtn)
        spacerItem = QtWidgets.QSpacerItem(140, 27, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem)
        self.messageNoBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.messageNoBtn.setMinimumSize(QtCore.QSize(0, 30))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icon/white/power.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.messageNoBtn.setIcon(icon1)
        self.messageNoBtn.setObjectName("messageNoBtn")
        self.horizontalLayout_11.addWidget(self.messageNoBtn)
        self.label = QtWidgets.QLabel(self.messageFrame)
        self.label.setGeometry(QtCore.QRect(130, 60, 311, 61))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.messageIconBtn = QtWidgets.QPushButton(self.messageFrame)
        self.messageIconBtn.setGeometry(QtCore.QRect(40, 60, 75, 61))
        self.messageIconBtn.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icon/black/alert-triangle.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.messageIconBtn.setIcon(icon2)
        self.messageIconBtn.setIconSize(QtCore.QSize(48, 48))
        self.messageIconBtn.setObjectName("messageIconBtn")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.messageTitle.setText(_translate("Dialog", "Add Savings for Ajewole Peter Oluwole"))
        self.messageYesBtn.setText(_translate("Dialog", "Yes"))
        self.messageNoBtn.setText(_translate("Dialog", "Cancel"))
        self.label.setText(_translate("Dialog", "Are you sure you want to remove this member? All their records and transactions will also be deleted!"))
from static import resource_rc
