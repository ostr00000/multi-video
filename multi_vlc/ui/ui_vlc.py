# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/vlc.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_VlcMainWindow(object):
    def setupUi(self, VlcMainWindow):
        VlcMainWindow.setObjectName("VlcMainWindow")
        VlcMainWindow.resize(651, 474)
        VlcMainWindow.setAcceptDrops(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/icon.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        VlcMainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(VlcMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 0, 0, 1, 1)
        VlcMainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(VlcMainWindow)
        self.toolBar.setObjectName("toolBar")
        VlcMainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionAdd = QtWidgets.QAction(VlcMainWindow)
        self.actionAdd.setObjectName("actionAdd")
        self.actionDelete = QtWidgets.QAction(VlcMainWindow)
        self.actionDelete.setObjectName("actionDelete")
        self.actionReset = QtWidgets.QAction(VlcMainWindow)
        self.actionReset.setObjectName("actionReset")
        self.actionLoad = QtWidgets.QAction(VlcMainWindow)
        self.actionLoad.setObjectName("actionLoad")
        self.actionSave = QtWidgets.QAction(VlcMainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionFind_Opened = QtWidgets.QAction(VlcMainWindow)
        self.actionFind_Opened.setObjectName("actionFind_Opened")
        self.actionSet_Position = QtWidgets.QAction(VlcMainWindow)
        self.actionSet_Position.setCheckable(True)
        self.actionSet_Position.setObjectName("actionSet_Position")
        self.actionStart = QtWidgets.QAction(VlcMainWindow)
        self.actionStart.setObjectName("actionStart")
        self.actionClose = QtWidgets.QAction(VlcMainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionPause = QtWidgets.QAction(VlcMainWindow)
        self.actionPause.setCheckable(True)
        self.actionPause.setObjectName("actionPause")
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionLoad)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionAdd)
        self.toolBar.addAction(self.actionDelete)
        self.toolBar.addAction(self.actionReset)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionFind_Opened)
        self.toolBar.addAction(self.actionSet_Position)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionStart)
        self.toolBar.addAction(self.actionPause)
        self.toolBar.addAction(self.actionClose)

        self.retranslateUi(VlcMainWindow)
        QtCore.QMetaObject.connectSlotsByName(VlcMainWindow)

    def retranslateUi(self, VlcMainWindow):
        _translate = QtCore.QCoreApplication.translate
        VlcMainWindow.setWindowTitle(_translate("VlcMainWindow", "MainWindow"))
        self.toolBar.setWindowTitle(_translate("VlcMainWindow", "toolBar"))
        self.actionAdd.setText(_translate("VlcMainWindow", "Add"))
        self.actionDelete.setText(_translate("VlcMainWindow", "Delete"))
        self.actionDelete.setShortcut(_translate("VlcMainWindow", "Del"))
        self.actionReset.setText(_translate("VlcMainWindow", "Reset"))
        self.actionLoad.setText(_translate("VlcMainWindow", "Load"))
        self.actionLoad.setShortcut(_translate("VlcMainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("VlcMainWindow", "Save"))
        self.actionSave.setShortcut(_translate("VlcMainWindow", "Ctrl+S"))
        self.actionFind_Opened.setText(_translate("VlcMainWindow", "Find Opened"))
        self.actionFind_Opened.setToolTip(_translate("VlcMainWindow", "Find Opened"))
        self.actionSet_Position.setText(_translate("VlcMainWindow", "Set Position"))
        self.actionSet_Position.setShortcut(_translate("VlcMainWindow", "S"))
        self.actionStart.setText(_translate("VlcMainWindow", "Start"))
        self.actionClose.setText(_translate("VlcMainWindow", "Close"))
        self.actionClose.setShortcut(_translate("VlcMainWindow", "Ctrl+Esc"))
        self.actionPause.setText(_translate("VlcMainWindow", "Pause"))
        self.actionPause.setShortcut(_translate("VlcMainWindow", "Space"))

from . import resources_rc
