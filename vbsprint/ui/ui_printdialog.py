# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'printdialog.ui'
#
# Created: Thu Nov  5 16:57:59 2015
#      by: PyQt4 UI code generator 4.10.4
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
        self.verticalLayout = QtGui.QVBoxLayout(PrintDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(PrintDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_composers = QtGui.QLabel(self.tab)
        self.label_composers.setObjectName(_fromUtf8("label_composers"))
        self.horizontalLayout_2.addWidget(self.label_composers)
        self.comboBox_composers = QtGui.QComboBox(self.tab)
        self.comboBox_composers.setObjectName(_fromUtf8("comboBox_composers"))
        self.horizontalLayout_2.addWidget(self.comboBox_composers)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label = QtGui.QLabel(self.tab)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        self.spinBoxScale = QtGui.QSpinBox(self.tab)
        self.spinBoxScale.setPrefix(_fromUtf8("1:"))
        self.spinBoxScale.setMinimum(1)
        self.spinBoxScale.setMaximum(1000000000)
        self.spinBoxScale.setSingleStep(1)
        self.spinBoxScale.setObjectName(_fromUtf8("spinBoxScale"))
        self.horizontalLayout_3.addWidget(self.spinBoxScale)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.label_4 = QtGui.QLabel(self.tab_2)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_9.addWidget(self.label_4)
        self.topleftLE = QtGui.QLineEdit(self.tab_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.topleftLE.sizePolicy().hasHeightForWidth())
        self.topleftLE.setSizePolicy(sizePolicy)
        self.topleftLE.setObjectName(_fromUtf8("topleftLE"))
        self.horizontalLayout_9.addWidget(self.topleftLE)
        self.verticalLayout_5.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.label_5 = QtGui.QLabel(self.tab_2)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_10.addWidget(self.label_5)
        self.bottomrightLE = QtGui.QLineEdit(self.tab_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bottomrightLE.sizePolicy().hasHeightForWidth())
        self.bottomrightLE.setSizePolicy(sizePolicy)
        self.bottomrightLE.setObjectName(_fromUtf8("bottomrightLE"))
        self.horizontalLayout_10.addWidget(self.bottomrightLE)
        self.verticalLayout_5.addLayout(self.horizontalLayout_10)
        self.coordinateButton = QtGui.QPushButton(self.tab_2)
        self.coordinateButton.setObjectName(_fromUtf8("coordinateButton"))
        self.verticalLayout_5.addWidget(self.coordinateButton)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_fileformat = QtGui.QLabel(PrintDialog)
        self.label_fileformat.setObjectName(_fromUtf8("label_fileformat"))
        self.horizontalLayout_4.addWidget(self.label_fileformat)
        self.comboBox_fileformat = QtGui.QComboBox(PrintDialog)
        self.comboBox_fileformat.setObjectName(_fromUtf8("comboBox_fileformat"))
        self.horizontalLayout_4.addWidget(self.comboBox_fileformat)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_14 = QtGui.QLabel(PrintDialog)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.horizontalLayout_7.addWidget(self.label_14)
        self.titleLE = QtGui.QLineEdit(PrintDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLE.sizePolicy().hasHeightForWidth())
        self.titleLE.setSizePolicy(sizePolicy)
        self.titleLE.setObjectName(_fromUtf8("titleLE"))
        self.horizontalLayout_7.addWidget(self.titleLE)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.checkBox_scalebar = QtGui.QCheckBox(PrintDialog)
        self.checkBox_scalebar.setObjectName(_fromUtf8("checkBox_scalebar"))
        self.horizontalLayout.addWidget(self.checkBox_scalebar)
        self.checkBox_legend = QtGui.QCheckBox(PrintDialog)
        self.checkBox_legend.setObjectName(_fromUtf8("checkBox_legend"))
        self.horizontalLayout.addWidget(self.checkBox_legend)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.frame = QtGui.QFrame(PrintDialog)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_15 = QtGui.QLabel(self.frame)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.horizontalLayout_6.addWidget(self.label_15)
        self.comboBox_crs = QtGui.QComboBox(self.frame)
        self.comboBox_crs.setObjectName(_fromUtf8("comboBox_crs"))
        self.horizontalLayout_6.addWidget(self.comboBox_crs)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_5.addWidget(self.label_2)
        self.spinBox_intervalx = QtGui.QDoubleSpinBox(self.frame)
        self.spinBox_intervalx.setDecimals(10)
        self.spinBox_intervalx.setMaximum(9999999.99)
        self.spinBox_intervalx.setObjectName(_fromUtf8("spinBox_intervalx"))
        self.horizontalLayout_5.addWidget(self.spinBox_intervalx)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_8.addWidget(self.label_3)
        self.spinBox_intervaly = QtGui.QDoubleSpinBox(self.frame)
        self.spinBox_intervaly.setDecimals(10)
        self.spinBox_intervaly.setMaximum(9999999.99)
        self.spinBox_intervaly.setObjectName(_fromUtf8("spinBox_intervaly"))
        self.horizontalLayout_8.addWidget(self.spinBox_intervaly)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.checkBox_caption = QtGui.QCheckBox(self.frame)
        self.checkBox_caption.setObjectName(_fromUtf8("checkBox_caption"))
        self.verticalLayout_2.addWidget(self.checkBox_caption)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout.addWidget(self.frame)
        self.caseButton = QtGui.QPushButton(PrintDialog)
        self.caseButton.setObjectName(_fromUtf8("caseButton"))
        self.verticalLayout.addWidget(self.caseButton)
        self.previewGraphic = QtGui.QGraphicsView(PrintDialog)
        self.previewGraphic.setObjectName(_fromUtf8("previewGraphic"))
        self.verticalLayout.addWidget(self.previewGraphic)
        self.buttonBox = QtGui.QDialogButtonBox(PrintDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(PrintDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PrintDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PrintDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PrintDialog)

    def retranslateUi(self, PrintDialog):
        PrintDialog.setWindowTitle(_translate("PrintDialog", "Print", None))
        self.label_composers.setText(_translate("PrintDialog", "Composer:", None))
        self.label.setText(_translate("PrintDialog", "Scale:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("PrintDialog", "Model", None))
        self.label_4.setText(_translate("PrintDialog", "Top Left:", None))
        self.label_5.setText(_translate("PrintDialog", "Bottom Right:", None))
        self.coordinateButton.setText(_translate("PrintDialog", "Generate", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("PrintDialog", "Coordinates", None))
        self.label_fileformat.setText(_translate("PrintDialog", "File format:", None))
        self.label_14.setText(_translate("PrintDialog", "Title:", None))
        self.checkBox_scalebar.setText(_translate("PrintDialog", "Scalebar", None))
        self.checkBox_legend.setText(_translate("PrintDialog", "Legend", None))
        self.label_15.setText(_translate("PrintDialog", "Grid:", None))
        self.label_2.setText(_translate("PrintDialog", "Interval X:", None))
        self.label_3.setText(_translate("PrintDialog", "Interval Y:", None))
        self.checkBox_caption.setText(_translate("PrintDialog", "Caption", None))
        self.caseButton.setText(_translate("PrintDialog", "Map Cartouche", None))

