# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Designer/chatWizard.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WizardPage(object):
    def setupUi(self, WizardPage):
        WizardPage.setObjectName("WizardPage")
        WizardPage.resize(661, 232)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(WizardPage)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.Instructions = QtWidgets.QLabel(WizardPage)
        self.Instructions.setWordWrap(True)
        self.Instructions.setObjectName("Instructions")
        self.verticalLayout_2.addWidget(self.Instructions)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.promptEdit = QtWidgets.QTextEdit(WizardPage)
        self.promptEdit.setObjectName("promptEdit")
        self.verticalLayout.addWidget(self.promptEdit)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(WizardPage)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.tempEdit = QtWidgets.QLineEdit(WizardPage)
        self.tempEdit.setObjectName("tempEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.tempEdit)
        self.label_2 = QtWidgets.QLabel(WizardPage)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.tokenEdit = QtWidgets.QLineEdit(WizardPage)
        self.tokenEdit.setObjectName("tokenEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.tokenEdit)
        self.horizontalLayout_2.addLayout(self.formLayout)
        spacerItem = QtWidgets.QSpacerItem(148, 75, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.saveButton = QtWidgets.QPushButton(WizardPage)
        self.saveButton.setObjectName("saveButton")
        self.verticalLayout_2.addWidget(self.saveButton)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        _translate = QtCore.QCoreApplication.translate
        WizardPage.setWindowTitle(_translate("WizardPage", "Chat Wizard"))
        self.Instructions.setText(_translate("WizardPage", "Write down a description of how you want the AI to act when responding to user prompts"))
        self.label.setText(_translate("WizardPage", "Temperature (0-2)"))
        self.label_2.setText(_translate("WizardPage", "Max Tokens"))
        self.saveButton.setText(_translate("WizardPage", "SAVE"))
