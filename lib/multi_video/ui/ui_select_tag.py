# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/select_tag.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SelectTagDialog(object):
    def setupUi(self, SelectTagDialog):
        SelectTagDialog.setObjectName("SelectTagDialog")
        SelectTagDialog.resize(565, 334)
        self.verticalLayout = QtWidgets.QVBoxLayout(SelectTagDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(SelectTagDialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.tagDirLineEdit = QtWidgets.QLineEdit(SelectTagDialog)
        self.tagDirLineEdit.setEnabled(False)
        self.tagDirLineEdit.setReadOnly(True)
        self.tagDirLineEdit.setObjectName("tagDirLineEdit")
        self.horizontalLayout_2.addWidget(self.tagDirLineEdit)
        self.changeTagDirButton = QtWidgets.QPushButton(SelectTagDialog)
        self.changeTagDirButton.setObjectName("changeTagDirButton")
        self.horizontalLayout_2.addWidget(self.changeTagDirButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listWidget = QtWidgets.QListWidget(SelectTagDialog)
        self.listWidget.setObjectName("listWidget")
        self.horizontalLayout.addWidget(self.listWidget)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(SelectTagDialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.tagComboBox = QtWidgets.QComboBox(SelectTagDialog)
        self.tagComboBox.setEnabled(False)
        self.tagComboBox.setObjectName("tagComboBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.tagComboBox)
        self.buttonAdd = QtWidgets.QPushButton(SelectTagDialog)
        self.buttonAdd.setEnabled(False)
        self.buttonAdd.setObjectName("buttonAdd")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.buttonAdd)
        self.buttonRemove = QtWidgets.QPushButton(SelectTagDialog)
        self.buttonRemove.setEnabled(False)
        self.buttonRemove.setObjectName("buttonRemove")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.buttonRemove)
        self.horizontalLayout.addLayout(self.formLayout)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(SelectTagDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.actionAdd = QtWidgets.QAction(SelectTagDialog)
        icon = QtGui.QIcon.fromTheme("list-add")
        self.actionAdd.setIcon(icon)
        self.actionAdd.setObjectName("actionAdd")
        self.actionRemove = QtWidgets.QAction(SelectTagDialog)
        icon = QtGui.QIcon.fromTheme("list-remove")
        self.actionRemove.setIcon(icon)
        self.actionRemove.setObjectName("actionRemove")

        self.retranslateUi(SelectTagDialog)
        self.buttonBox.accepted.connect(SelectTagDialog.accept)
        self.buttonBox.rejected.connect(SelectTagDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SelectTagDialog)
        SelectTagDialog.setTabOrder(self.buttonAdd, self.buttonRemove)
        SelectTagDialog.setTabOrder(self.buttonRemove, self.listWidget)

    def retranslateUi(self, SelectTagDialog):
        _translate = QtCore.QCoreApplication.translate
        SelectTagDialog.setWindowTitle(_translate("SelectTagDialog", "Select tags"))
        self.label_2.setText(_translate("SelectTagDialog", "Tag dir:"))
        self.changeTagDirButton.setText(_translate("SelectTagDialog", "Change tag directory"))
        self.label.setText(_translate("SelectTagDialog", "Avaliable tags:"))
        self.buttonAdd.setText(_translate("SelectTagDialog", "Add"))
        self.buttonRemove.setText(_translate("SelectTagDialog", "Remove"))
        self.actionAdd.setText(_translate("SelectTagDialog", "Add"))
        self.actionRemove.setText(_translate("SelectTagDialog", "Remove"))
