# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'printdialog.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_PrintDialog(object):
    def setupUi(self, PrintDialog):
        PrintDialog.setObjectName(_fromUtf8("PrintDialog"))
        PrintDialog.resize(394, 670)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("printer"))
        PrintDialog.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(PrintDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.scalebarLegendWidget = QtGui.QHBoxLayout()
        self.scalebarLegendWidget.setObjectName(_fromUtf8("scalebarLegendWidget"))
        self.checkBox_scalebar = QtGui.QCheckBox(PrintDialog)
        self.checkBox_scalebar.setObjectName(_fromUtf8("checkBox_scalebar"))
        self.scalebarLegendWidget.addWidget(self.checkBox_scalebar)
        self.checkBox_legend = QtGui.QCheckBox(PrintDialog)
        self.checkBox_legend.setObjectName(_fromUtf8("checkBox_legend"))
        self.scalebarLegendWidget.addWidget(self.checkBox_legend)
        self.gridLayout.addLayout(self.scalebarLegendWidget, 6, 0, 1, 2)
        self.caseButton = QtGui.QPushButton(PrintDialog)
        self.caseButton.setObjectName(_fromUtf8("caseButton"))
        self.gridLayout.addWidget(self.caseButton, 5, 0, 1, 2)
        self.comboBox_composers = QtGui.QComboBox(PrintDialog)
        self.comboBox_composers.setObjectName(_fromUtf8("comboBox_composers"))
        self.gridLayout.addWidget(self.comboBox_composers, 0, 1, 1, 1)
        self.gridGB = QgsCollapsibleGroupBox(PrintDialog)
        self.gridGB.setObjectName(_fromUtf8("gridGB"))
        self.gridLayout_3 = QtGui.QGridLayout(self.gridGB)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.comboBox_crs = QtGui.QComboBox(self.gridGB)
        self.comboBox_crs.setObjectName(_fromUtf8("comboBox_crs"))
        self.gridLayout_3.addWidget(self.comboBox_crs, 0, 2, 1, 1)
        self.label_15 = QtGui.QLabel(self.gridGB)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.gridLayout_3.addWidget(self.label_15, 0, 0, 1, 1)
        self.spinBox_intervaly = QtGui.QDoubleSpinBox(self.gridGB)
        self.spinBox_intervaly.setDecimals(10)
        self.spinBox_intervaly.setMaximum(9999999.99)
        self.spinBox_intervaly.setObjectName(_fromUtf8("spinBox_intervaly"))
        self.gridLayout_3.addWidget(self.spinBox_intervaly, 2, 2, 1, 1)
        self.label_2 = QtGui.QLabel(self.gridGB)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)
        self.checkBox_caption = QtGui.QCheckBox(self.gridGB)
        self.checkBox_caption.setObjectName(_fromUtf8("checkBox_caption"))
        self.gridLayout_3.addWidget(self.checkBox_caption, 3, 0, 1, 3)
        self.spinBox_intervalx = QtGui.QDoubleSpinBox(self.gridGB)
        self.spinBox_intervalx.setDecimals(10)
        self.spinBox_intervalx.setMaximum(9999999.99)
        self.spinBox_intervalx.setObjectName(_fromUtf8("spinBox_intervalx"))
        self.gridLayout_3.addWidget(self.spinBox_intervalx, 1, 2, 1, 1)
        self.label_3 = QtGui.QLabel(self.gridGB)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_3.addWidget(self.label_3, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.gridGB, 7, 0, 1, 2)
        self.label = QtGui.QLabel(PrintDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.coordinateGB = QgsCollapsibleGroupBox(PrintDialog)
        self.coordinateGB.setFlat(False)
        self.coordinateGB.setCheckable(False)
        self.coordinateGB.setChecked(False)
        self.coordinateGB.setObjectName(_fromUtf8("coordinateGB"))
        self.gridLayout_2 = QtGui.QGridLayout(self.coordinateGB)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_4 = QtGui.QLabel(self.coordinateGB)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.label_7 = QtGui.QLabel(self.coordinateGB)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 0, 3, 1, 1)
        self.xleftLE = QtGui.QLineEdit(self.coordinateGB)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xleftLE.sizePolicy().hasHeightForWidth())
        self.xleftLE.setSizePolicy(sizePolicy)
        self.xleftLE.setObjectName(_fromUtf8("xleftLE"))
        self.gridLayout_2.addWidget(self.xleftLE, 0, 2, 1, 1)
        self.label_9 = QtGui.QLabel(self.coordinateGB)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_2.addWidget(self.label_9, 1, 1, 1, 1)
        self.ybottomLE = QtGui.QLineEdit(self.coordinateGB)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ybottomLE.sizePolicy().hasHeightForWidth())
        self.ybottomLE.setSizePolicy(sizePolicy)
        self.ybottomLE.setObjectName(_fromUtf8("ybottomLE"))
        self.gridLayout_2.addWidget(self.ybottomLE, 1, 4, 1, 1)
        self.ytopLE = QtGui.QLineEdit(self.coordinateGB)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ytopLE.sizePolicy().hasHeightForWidth())
        self.ytopLE.setSizePolicy(sizePolicy)
        self.ytopLE.setObjectName(_fromUtf8("ytopLE"))
        self.gridLayout_2.addWidget(self.ytopLE, 0, 4, 1, 1)
        self.label_5 = QtGui.QLabel(self.coordinateGB)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)
        self.label_8 = QtGui.QLabel(self.coordinateGB)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_2.addWidget(self.label_8, 1, 3, 1, 1)
        self.label_10 = QtGui.QLabel(self.coordinateGB)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_2.addWidget(self.label_10, 2, 0, 1, 1)
        self.label_6 = QtGui.QLabel(self.coordinateGB)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 0, 1, 1, 1)
        self.xrightLE = QtGui.QLineEdit(self.coordinateGB)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xrightLE.sizePolicy().hasHeightForWidth())
        self.xrightLE.setSizePolicy(sizePolicy)
        self.xrightLE.setObjectName(_fromUtf8("xrightLE"))
        self.gridLayout_2.addWidget(self.xrightLE, 1, 2, 1, 1)
        self.coordinateButton = QtGui.QPushButton(self.coordinateGB)
        self.coordinateButton.setObjectName(_fromUtf8("coordinateButton"))
        self.gridLayout_2.addWidget(self.coordinateButton, 3, 0, 1, 5)
        self.borderSB = QtGui.QDoubleSpinBox(self.coordinateGB)
        self.borderSB.setDecimals(0)
        self.borderSB.setMinimum(15.0)
        self.borderSB.setMaximum(1000.0)
        self.borderSB.setObjectName(_fromUtf8("borderSB"))
        self.gridLayout_2.addWidget(self.borderSB, 2, 2, 1, 3)
        self.gridLayout.addWidget(self.coordinateGB, 2, 0, 1, 2)
        self.label_composers = QtGui.QLabel(PrintDialog)
        self.label_composers.setObjectName(_fromUtf8("label_composers"))
        self.gridLayout.addWidget(self.label_composers, 0, 0, 1, 1)
        self.spinBoxScale = QtGui.QSpinBox(PrintDialog)
        self.spinBoxScale.setPrefix(_fromUtf8("1:"))
        self.spinBoxScale.setMinimum(1)
        self.spinBoxScale.setMaximum(1000000000)
        self.spinBoxScale.setSingleStep(1)
        self.spinBoxScale.setObjectName(_fromUtf8("spinBoxScale"))
        self.gridLayout.addWidget(self.spinBoxScale, 3, 1, 1, 1)
        self.comboBox_fileformat = QtGui.QComboBox(PrintDialog)
        self.comboBox_fileformat.setObjectName(_fromUtf8("comboBox_fileformat"))
        self.gridLayout.addWidget(self.comboBox_fileformat, 9, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(PrintDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 10, 0, 1, 2)
        self.label_fileformat = QtGui.QLabel(PrintDialog)
        self.label_fileformat.setObjectName(_fromUtf8("label_fileformat"))
        self.gridLayout.addWidget(self.label_fileformat, 9, 0, 1, 1)
        self.previewGraphic = QtGui.QGraphicsView(PrintDialog)
        self.previewGraphic.setObjectName(_fromUtf8("previewGraphic"))
        self.gridLayout.addWidget(self.previewGraphic, 8, 0, 1, 2)
        self.label_14 = QtGui.QLabel(PrintDialog)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout.addWidget(self.label_14, 1, 0, 1, 1)
        self.titleLE = QtGui.QLineEdit(PrintDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLE.sizePolicy().hasHeightForWidth())
        self.titleLE.setSizePolicy(sizePolicy)
        self.titleLE.setObjectName(_fromUtf8("titleLE"))
        self.gridLayout.addWidget(self.titleLE, 1, 1, 1, 1)

        self.retranslateUi(PrintDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PrintDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PrintDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PrintDialog)

    def retranslateUi(self, PrintDialog):
        PrintDialog.setWindowTitle(_translate("PrintDialog", "Print", None))
        self.checkBox_scalebar.setText(_translate("PrintDialog", "Scalebar", None))
        self.checkBox_legend.setText(_translate("PrintDialog", "Legend", None))
        self.caseButton.setText(_translate("PrintDialog", "Map Cartouche", None))
        self.gridGB.setTitle(_translate("PrintDialog", "Grid", None))
        self.label_15.setText(_translate("PrintDialog", "Grid:", None))
        self.label_2.setText(_translate("PrintDialog", "Interval X:", None))
        self.checkBox_caption.setText(_translate("PrintDialog", "Caption", None))
        self.label_3.setText(_translate("PrintDialog", "Interval Y:", None))
        self.label.setText(_translate("PrintDialog", "Scale:", None))
        self.coordinateGB.setTitle(_translate("PrintDialog", "Variable size", None))
        self.label_4.setText(_translate("PrintDialog", "Top Left:", None))
        self.label_7.setText(_translate("PrintDialog", "Y:", None))
        self.label_9.setText(_translate("PrintDialog", "X:", None))
        self.label_5.setText(_translate("PrintDialog", "Bottom Right:", None))
        self.label_8.setText(_translate("PrintDialog", "Y:", None))
        self.label_10.setText(_translate("PrintDialog", "Border:", None))
        self.label_6.setText(_translate("PrintDialog", "X:", None))
        self.coordinateButton.setText(_translate("PrintDialog", "Update Layout", None))
        self.borderSB.setSuffix(_translate("PrintDialog", " mm", None))
        self.label_composers.setText(_translate("PrintDialog", "Layout:", None))
        self.label_fileformat.setText(_translate("PrintDialog", "File format:", None))
        self.label_14.setText(_translate("PrintDialog", "Title:", None))

from qgis.gui import QgsCollapsibleGroupBox
