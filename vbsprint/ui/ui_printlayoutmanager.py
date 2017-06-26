# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'printlayoutmanager.ui'
#
# Created by: PyQt4 UI code generator 4.12
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_PrintLayoutManager(object):
    def setupUi(self, PrintLayoutManager):
        PrintLayoutManager.setObjectName(_fromUtf8("PrintLayoutManager"))
        PrintLayoutManager.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(PrintLayoutManager)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButtonImport = QtGui.QPushButton(PrintLayoutManager)
        self.pushButtonImport.setObjectName(_fromUtf8("pushButtonImport"))
        self.gridLayout.addWidget(self.pushButtonImport, 1, 0, 1, 1)
        self.pushButtonExport = QtGui.QPushButton(PrintLayoutManager)
        self.pushButtonExport.setEnabled(False)
        self.pushButtonExport.setObjectName(_fromUtf8("pushButtonExport"))
        self.gridLayout.addWidget(self.pushButtonExport, 1, 1, 1, 1)
        self.pushButtonRemove = QtGui.QPushButton(PrintLayoutManager)
        self.pushButtonRemove.setEnabled(False)
        self.pushButtonRemove.setObjectName(_fromUtf8("pushButtonRemove"))
        self.gridLayout.addWidget(self.pushButtonRemove, 1, 2, 1, 1)
        self.listWidgetLayouts = QtGui.QListWidget(PrintLayoutManager)
        self.listWidgetLayouts.setObjectName(_fromUtf8("listWidgetLayouts"))
        self.gridLayout.addWidget(self.listWidgetLayouts, 0, 0, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(PrintLayoutManager)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 3)

        self.retranslateUi(PrintLayoutManager)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PrintLayoutManager.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PrintLayoutManager.reject)
        QtCore.QMetaObject.connectSlotsByName(PrintLayoutManager)

    def retranslateUi(self, PrintLayoutManager):
        PrintLayoutManager.setWindowTitle(_translate("PrintLayoutManager", "Print Layout Manager", None))
        self.pushButtonImport.setText(_translate("PrintLayoutManager", "Import", None))
        self.pushButtonExport.setText(_translate("PrintLayoutManager", "Export", None))
        self.pushButtonRemove.setText(_translate("PrintLayoutManager", "Remove", None))

