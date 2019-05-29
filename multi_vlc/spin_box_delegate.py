from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QItemDelegate, QSpinBox


class SpinBoxDelegate(QItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QSpinBox(parent)
        editor.setRange(1, 10)
        return editor

    def setEditorData(self, spinBox, index):
        spinBox.setValue(index.model().data(index, Qt.DisplayRole))

    def setModelData(self, spinBox, model, index):
        spinBox.interpretText()
        value = spinBox.value()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
