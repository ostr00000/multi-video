# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lib/multi_video/ui/select_tag.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SelectTagDialog(object):
    def setupUi(self, SelectTagDialog):
        SelectTagDialog.setObjectName("SelectTagDialog")
        SelectTagDialog.resize(1171, 573)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(SelectTagDialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.splitter = QtWidgets.QSplitter(SelectTagDialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.tagDirLineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.tagDirLineEdit.setEnabled(False)
        self.tagDirLineEdit.setReadOnly(True)
        self.tagDirLineEdit.setObjectName("tagDirLineEdit")
        self.horizontalLayout_2.addWidget(self.tagDirLineEdit)
        self.changeTagDirButton = QtWidgets.QToolButton(self.layoutWidget)
        icon = QtGui.QIcon.fromTheme("folder")
        self.changeTagDirButton.setIcon(icon)
        self.changeTagDirButton.setObjectName("changeTagDirButton")
        self.horizontalLayout_2.addWidget(self.changeTagDirButton)
        self.refreshButton = QtWidgets.QToolButton(self.layoutWidget)
        icon = QtGui.QIcon.fromTheme("view-refresh")
        self.refreshButton.setIcon(icon)
        self.refreshButton.setObjectName("refreshButton")
        self.horizontalLayout_2.addWidget(self.refreshButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.listWidget = QtWidgets.QListWidget(self.layoutWidget)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.selectedTagLabel = QtWidgets.QLabel(self.layoutWidget)
        self.selectedTagLabel.setObjectName("selectedTagLabel")
        self.horizontalLayout.addWidget(self.selectedTagLabel)
        self.removeButton = QtWidgets.QToolButton(self.layoutWidget)
        self.removeButton.setEnabled(False)
        self.removeButton.setObjectName("removeButton")
        self.horizontalLayout.addWidget(self.removeButton)
        self.addButton = QtWidgets.QToolButton(self.layoutWidget)
        self.addButton.setObjectName("addButton")
        self.horizontalLayout.addWidget(self.addButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tagWidgetPlaceholder = QtWidgets.QWidget(self.widget)
        self.tagWidgetPlaceholder.setObjectName("tagWidgetPlaceholder")
        self.verticalLayout_2.addWidget(self.tagWidgetPlaceholder)
        self.verticalLayout_3.addWidget(self.splitter)
        self.buttonBox = QtWidgets.QDialogButtonBox(SelectTagDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)
        self.actionAdd = QtWidgets.QAction(SelectTagDialog)
        icon = QtGui.QIcon.fromTheme("list-add")
        self.actionAdd.setIcon(icon)
        self.actionAdd.setObjectName("actionAdd")
        self.actionRemove = QtWidgets.QAction(SelectTagDialog)
        icon = QtGui.QIcon.fromTheme("list-remove")
        self.actionRemove.setIcon(icon)
        self.actionRemove.setObjectName("actionRemove")

        self.retranslateUi(SelectTagDialog)
        self.buttonBox.accepted.connect(SelectTagDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(SelectTagDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(SelectTagDialog)

    def retranslateUi(self, SelectTagDialog):
        _translate = QtCore.QCoreApplication.translate
        SelectTagDialog.setWindowTitle(_translate("SelectTagDialog", "Select tags"))
        self.label_2.setText(_translate("SelectTagDialog", "Tag dir:"))
        self.changeTagDirButton.setToolTip(_translate("SelectTagDialog", "Change tag directory"))
        self.changeTagDirButton.setText(_translate("SelectTagDialog", "..."))
        self.refreshButton.setToolTip(_translate("SelectTagDialog", "Refresh possible tags"))
        self.refreshButton.setText(_translate("SelectTagDialog", "..."))
        self.label_3.setText(_translate("SelectTagDialog", "Total tags:"))
        self.selectedTagLabel.setText(_translate("SelectTagDialog", "0"))
        self.removeButton.setText(_translate("SelectTagDialog", "Remove"))
        self.addButton.setText(_translate("SelectTagDialog", "Add"))
        self.actionAdd.setText(_translate("SelectTagDialog", "Add"))
        self.actionRemove.setText(_translate("SelectTagDialog", "Remove"))
