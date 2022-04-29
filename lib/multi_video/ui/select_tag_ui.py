# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lib/multi_video/ui/select_tag.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


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
        self.refreshButton = QtWidgets.QToolButton(SelectTagDialog)
        icon = QtGui.QIcon.fromTheme("view-refresh")
        self.refreshButton.setIcon(icon)
        self.refreshButton.setObjectName("refreshButton")
        self.horizontalLayout_2.addWidget(self.refreshButton)
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
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(4, QtWidgets.QFormLayout.SpanningRole, spacerItem)
        self.label_3 = QtWidgets.QLabel(SelectTagDialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.selectedTagLabel = QtWidgets.QLabel(SelectTagDialog)
        self.selectedTagLabel.setObjectName("selectedTagLabel")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.selectedTagLabel)
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
        self.refreshButton.setText(_translate("SelectTagDialog", "..."))
        self.label.setText(_translate("SelectTagDialog", "Avaliable tags:"))
        self.buttonAdd.setText(_translate("SelectTagDialog", "Add"))
        self.buttonRemove.setText(_translate("SelectTagDialog", "Remove"))
        self.label_3.setText(_translate("SelectTagDialog", "Selected tags:"))
        self.selectedTagLabel.setText(_translate("SelectTagDialog", "0"))
        self.actionAdd.setText(_translate("SelectTagDialog", "Add"))
        self.actionRemove.setText(_translate("SelectTagDialog", "Remove"))