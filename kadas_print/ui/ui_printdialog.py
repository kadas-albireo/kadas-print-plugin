# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'printdialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PrintDialog(object):
    def setupUi(self, PrintDialog):
        PrintDialog.setObjectName("PrintDialog")
        PrintDialog.resize(501, 670)
        icon = QtGui.QIcon.fromTheme("printer")
        PrintDialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(PrintDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label_border = QtWidgets.QLabel(PrintDialog)
        self.label_border.setObjectName("label_border")
        self.gridLayout.addWidget(self.label_border, 5, 0, 1, 1)
        self.label_extent = QtWidgets.QLabel(PrintDialog)
        self.label_extent.setObjectName("label_extent")
        self.gridLayout.addWidget(self.label_extent, 4, 0, 1, 1)
        self.label_printlayouts = QtWidgets.QLabel(PrintDialog)
        self.label_printlayouts.setObjectName("label_printlayouts")
        self.gridLayout.addWidget(self.label_printlayouts, 1, 0, 1, 1)
        self.label_title = QtWidgets.QLabel(PrintDialog)
        self.label_title.setObjectName("label_title")
        self.gridLayout.addWidget(self.label_title, 2, 0, 1, 1)
        self.comboBox_printlayouts = QtWidgets.QComboBox(PrintDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_printlayouts.sizePolicy().hasHeightForWidth())
        self.comboBox_printlayouts.setSizePolicy(sizePolicy)
        self.comboBox_printlayouts.setObjectName("comboBox_printlayouts")
        self.gridLayout.addWidget(self.comboBox_printlayouts, 1, 1, 1, 1)
        self.checkBox_scalebar = QtWidgets.QCheckBox(PrintDialog)
        self.checkBox_scalebar.setObjectName("checkBox_scalebar")
        self.gridLayout.addWidget(self.checkBox_scalebar, 9, 0, 1, 1)
        self.checkBox_legend = QtWidgets.QCheckBox(PrintDialog)
        self.checkBox_legend.setObjectName("checkBox_legend")
        self.gridLayout.addWidget(self.checkBox_legend, 10, 0, 1, 1)
        self.label_fileformat = QtWidgets.QLabel(PrintDialog)
        self.label_fileformat.setObjectName("label_fileformat")
        self.gridLayout.addWidget(self.label_fileformat, 14, 0, 1, 1)
        self.checkBox_mapCartouche = QtWidgets.QCheckBox(PrintDialog)
        self.checkBox_mapCartouche.setObjectName("checkBox_mapCartouche")
        self.gridLayout.addWidget(self.checkBox_mapCartouche, 8, 0, 1, 1)
        self.label_scale = QtWidgets.QLabel(PrintDialog)
        self.label_scale.setObjectName("label_scale")
        self.gridLayout.addWidget(self.label_scale, 3, 0, 1, 1)
        self.toolButton_layoutManager = QtWidgets.QToolButton(PrintDialog)
        self.toolButton_layoutManager.setObjectName("toolButton_layoutManager")
        self.gridLayout.addWidget(self.toolButton_layoutManager, 1, 2, 1, 1)
        self.label_unitWarning = QtWidgets.QLabel(PrintDialog)
        self.label_unitWarning.setStyleSheet("QLabel { background: orange; font-weight:bold; border-radius: 5px; padding: 5px; }")
        self.label_unitWarning.setWordWrap(True)
        self.label_unitWarning.setObjectName("label_unitWarning")
        self.gridLayout.addWidget(self.label_unitWarning, 0, 0, 1, 3)
        self.lineEdit_title = QtWidgets.QLineEdit(PrintDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_title.sizePolicy().hasHeightForWidth())
        self.lineEdit_title.setSizePolicy(sizePolicy)
        self.lineEdit_title.setObjectName("lineEdit_title")
        self.gridLayout.addWidget(self.lineEdit_title, 2, 1, 1, 2)
        self.comboBox_scale = gui.QgsScaleComboBox(PrintDialog)
        self.comboBox_scale.setEditable(True)
        self.comboBox_scale.setObjectName("comboBox_scale")
        self.gridLayout.addWidget(self.comboBox_scale, 3, 1, 1, 2)
        self.widget_extent = QtWidgets.QWidget(PrintDialog)
        self.widget_extent.setObjectName("widget_extent")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget_extent)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lineedit_ymin = QtWidgets.QLineEdit(self.widget_extent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineedit_ymin.sizePolicy().hasHeightForWidth())
        self.lineedit_ymin.setSizePolicy(sizePolicy)
        self.lineedit_ymin.setObjectName("lineedit_ymin")
        self.gridLayout_2.addWidget(self.lineedit_ymin, 1, 2, 1, 1)
        self.label_xmax = QtWidgets.QLabel(self.widget_extent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_xmax.sizePolicy().hasHeightForWidth())
        self.label_xmax.setSizePolicy(sizePolicy)
        self.label_xmax.setObjectName("label_xmax")
        self.gridLayout_2.addWidget(self.label_xmax, 0, 3, 1, 1)
        self.label_xmin = QtWidgets.QLabel(self.widget_extent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_xmin.sizePolicy().hasHeightForWidth())
        self.label_xmin.setSizePolicy(sizePolicy)
        self.label_xmin.setObjectName("label_xmin")
        self.gridLayout_2.addWidget(self.label_xmin, 0, 0, 1, 1)
        self.lineedit_xmin = QtWidgets.QLineEdit(self.widget_extent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineedit_xmin.sizePolicy().hasHeightForWidth())
        self.lineedit_xmin.setSizePolicy(sizePolicy)
        self.lineedit_xmin.setObjectName("lineedit_xmin")
        self.gridLayout_2.addWidget(self.lineedit_xmin, 0, 2, 1, 1)
        self.label_ymax = QtWidgets.QLabel(self.widget_extent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ymax.sizePolicy().hasHeightForWidth())
        self.label_ymax.setSizePolicy(sizePolicy)
        self.label_ymax.setObjectName("label_ymax")
        self.gridLayout_2.addWidget(self.label_ymax, 1, 3, 1, 1)
        self.label_ymin = QtWidgets.QLabel(self.widget_extent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ymin.sizePolicy().hasHeightForWidth())
        self.label_ymin.setSizePolicy(sizePolicy)
        self.label_ymin.setObjectName("label_ymin")
        self.gridLayout_2.addWidget(self.label_ymin, 1, 0, 1, 1)
        self.lineedit_ymax = QtWidgets.QLineEdit(self.widget_extent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineedit_ymax.sizePolicy().hasHeightForWidth())
        self.lineedit_ymax.setSizePolicy(sizePolicy)
        self.lineedit_ymax.setObjectName("lineedit_ymax")
        self.gridLayout_2.addWidget(self.lineedit_ymax, 1, 4, 1, 1)
        self.lineedit_xmax = QtWidgets.QLineEdit(self.widget_extent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineedit_xmax.sizePolicy().hasHeightForWidth())
        self.lineedit_xmax.setSizePolicy(sizePolicy)
        self.lineedit_xmax.setObjectName("lineedit_xmax")
        self.gridLayout_2.addWidget(self.lineedit_xmax, 0, 4, 1, 1)
        self.label_paperSize = QtWidgets.QLabel(self.widget_extent)
        self.label_paperSize.setText("")
        self.label_paperSize.setObjectName("label_paperSize")
        self.gridLayout_2.addWidget(self.label_paperSize, 2, 0, 1, 5)
        self.gridLayout.addWidget(self.widget_extent, 4, 1, 1, 2)
        self.spinBox_border = QtWidgets.QDoubleSpinBox(PrintDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_border.sizePolicy().hasHeightForWidth())
        self.spinBox_border.setSizePolicy(sizePolicy)
        self.spinBox_border.setKeyboardTracking(False)
        self.spinBox_border.setDecimals(0)
        self.spinBox_border.setMaximum(1000.0)
        self.spinBox_border.setProperty("value", 15.0)
        self.spinBox_border.setObjectName("spinBox_border")
        self.gridLayout.addWidget(self.spinBox_border, 5, 1, 1, 2)
        self.groupBox_grid = QtWidgets.QGroupBox(PrintDialog)
        self.groupBox_grid.setCheckable(True)
        self.groupBox_grid.setChecked(False)
        self.groupBox_grid.setObjectName("groupBox_grid")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_grid)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.comboBox_crs = QtWidgets.QComboBox(self.groupBox_grid)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_crs.sizePolicy().hasHeightForWidth())
        self.comboBox_crs.setSizePolicy(sizePolicy)
        self.comboBox_crs.setObjectName("comboBox_crs")
        self.gridLayout_3.addWidget(self.comboBox_crs, 0, 2, 1, 1)
        self.label_crs = QtWidgets.QLabel(self.groupBox_grid)
        self.label_crs.setObjectName("label_crs")
        self.gridLayout_3.addWidget(self.label_crs, 0, 0, 1, 1)
        self.spinBox_intervaly = QtWidgets.QDoubleSpinBox(self.groupBox_grid)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_intervaly.sizePolicy().hasHeightForWidth())
        self.spinBox_intervaly.setSizePolicy(sizePolicy)
        self.spinBox_intervaly.setKeyboardTracking(False)
        self.spinBox_intervaly.setDecimals(10)
        self.spinBox_intervaly.setMaximum(9999999.99)
        self.spinBox_intervaly.setObjectName("spinBox_intervaly")
        self.gridLayout_3.addWidget(self.spinBox_intervaly, 2, 2, 1, 1)
        self.label_intervalx = QtWidgets.QLabel(self.groupBox_grid)
        self.label_intervalx.setObjectName("label_intervalx")
        self.gridLayout_3.addWidget(self.label_intervalx, 1, 0, 1, 1)
        self.checkBox_gridAnnotations = QtWidgets.QCheckBox(self.groupBox_grid)
        self.checkBox_gridAnnotations.setObjectName("checkBox_gridAnnotations")
        self.gridLayout_3.addWidget(self.checkBox_gridAnnotations, 3, 0, 1, 3)
        self.spinBox_intervalx = QtWidgets.QDoubleSpinBox(self.groupBox_grid)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_intervalx.sizePolicy().hasHeightForWidth())
        self.spinBox_intervalx.setSizePolicy(sizePolicy)
        self.spinBox_intervalx.setKeyboardTracking(False)
        self.spinBox_intervalx.setDecimals(10)
        self.spinBox_intervalx.setMaximum(9999999.99)
        self.spinBox_intervalx.setObjectName("spinBox_intervalx")
        self.gridLayout_3.addWidget(self.spinBox_intervalx, 1, 2, 1, 1)
        self.label_intervaly = QtWidgets.QLabel(self.groupBox_grid)
        self.label_intervaly.setObjectName("label_intervaly")
        self.gridLayout_3.addWidget(self.label_intervaly, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_grid, 7, 0, 1, 3)
        self.button_mapCartouche = QtWidgets.QPushButton(PrintDialog)
        self.button_mapCartouche.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_mapCartouche.sizePolicy().hasHeightForWidth())
        self.button_mapCartouche.setSizePolicy(sizePolicy)
        self.button_mapCartouche.setObjectName("button_mapCartouche")
        self.gridLayout.addWidget(self.button_mapCartouche, 8, 1, 1, 2)
        self.button_configureLegend = QtWidgets.QPushButton(PrintDialog)
        self.button_configureLegend.setEnabled(False)
        self.button_configureLegend.setObjectName("button_configureLegend")
        self.gridLayout.addWidget(self.button_configureLegend, 10, 1, 1, 2)
        self.previewGraphic = QtWidgets.QGraphicsView(PrintDialog)
        self.previewGraphic.setEnabled(False)
        self.previewGraphic.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.previewGraphic.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.previewGraphic.setInteractive(False)
        self.previewGraphic.setObjectName("previewGraphic")
        self.gridLayout.addWidget(self.previewGraphic, 13, 0, 1, 3)
        self.comboBox_fileformat = QtWidgets.QComboBox(PrintDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_fileformat.sizePolicy().hasHeightForWidth())
        self.comboBox_fileformat.setSizePolicy(sizePolicy)
        self.comboBox_fileformat.setObjectName("comboBox_fileformat")
        self.gridLayout.addWidget(self.comboBox_fileformat, 14, 1, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(PrintDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 15, 0, 1, 3)

        self.retranslateUi(PrintDialog)
        self.buttonBox.accepted.connect(PrintDialog.accept)
        self.buttonBox.rejected.connect(PrintDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PrintDialog)
        PrintDialog.setTabOrder(self.comboBox_printlayouts, self.lineEdit_title)
        PrintDialog.setTabOrder(self.lineEdit_title, self.comboBox_scale)
        PrintDialog.setTabOrder(self.comboBox_scale, self.lineedit_xmin)
        PrintDialog.setTabOrder(self.lineedit_xmin, self.lineedit_xmax)
        PrintDialog.setTabOrder(self.lineedit_xmax, self.lineedit_ymin)
        PrintDialog.setTabOrder(self.lineedit_ymin, self.lineedit_ymax)
        PrintDialog.setTabOrder(self.lineedit_ymax, self.spinBox_border)
        PrintDialog.setTabOrder(self.spinBox_border, self.groupBox_grid)
        PrintDialog.setTabOrder(self.groupBox_grid, self.comboBox_crs)
        PrintDialog.setTabOrder(self.comboBox_crs, self.spinBox_intervalx)
        PrintDialog.setTabOrder(self.spinBox_intervalx, self.spinBox_intervaly)
        PrintDialog.setTabOrder(self.spinBox_intervaly, self.checkBox_gridAnnotations)
        PrintDialog.setTabOrder(self.checkBox_gridAnnotations, self.checkBox_mapCartouche)
        PrintDialog.setTabOrder(self.checkBox_mapCartouche, self.button_mapCartouche)
        PrintDialog.setTabOrder(self.button_mapCartouche, self.checkBox_scalebar)
        PrintDialog.setTabOrder(self.checkBox_scalebar, self.checkBox_legend)
        PrintDialog.setTabOrder(self.checkBox_legend, self.button_configureLegend)
        PrintDialog.setTabOrder(self.button_configureLegend, self.previewGraphic)
        PrintDialog.setTabOrder(self.previewGraphic, self.comboBox_fileformat)
        PrintDialog.setTabOrder(self.comboBox_fileformat, self.buttonBox)

    def retranslateUi(self, PrintDialog):
        _translate = QtCore.QCoreApplication.translate
        PrintDialog.setWindowTitle(_translate("PrintDialog", "Print"))
        self.label_border.setText(_translate("PrintDialog", "Border:"))
        self.label_extent.setText(_translate("PrintDialog", "Extent:"))
        self.label_printlayouts.setText(_translate("PrintDialog", "Layout:"))
        self.label_title.setText(_translate("PrintDialog", "Title:"))
        self.checkBox_scalebar.setText(_translate("PrintDialog", "Scalebar"))
        self.checkBox_legend.setText(_translate("PrintDialog", "Legend"))
        self.label_fileformat.setText(_translate("PrintDialog", "File format:"))
        self.checkBox_mapCartouche.setText(_translate("PrintDialog", "Map cartouche"))
        self.label_scale.setText(_translate("PrintDialog", "Scale:"))
        self.toolButton_layoutManager.setText(_translate("PrintDialog", "..."))
        self.label_unitWarning.setText(_translate("PrintDialog", "Only meter based coordinate systems are supported in variable extent mode."))
        self.label_xmax.setText(_translate("PrintDialog", "X Max.:"))
        self.label_xmin.setText(_translate("PrintDialog", "X Min.:"))
        self.label_ymax.setText(_translate("PrintDialog", "Y Max.:"))
        self.label_ymin.setText(_translate("PrintDialog", "Y Min.:"))
        self.spinBox_border.setSuffix(_translate("PrintDialog", " mm"))
        self.groupBox_grid.setTitle(_translate("PrintDialog", "Grid"))
        self.label_crs.setText(_translate("PrintDialog", "Coordinate system:"))
        self.label_intervalx.setText(_translate("PrintDialog", "Interval X:"))
        self.checkBox_gridAnnotations.setText(_translate("PrintDialog", "Coordinate labels"))
        self.label_intervaly.setText(_translate("PrintDialog", "Interval Y:"))
        self.button_mapCartouche.setText(_translate("PrintDialog", "Edit map cartouche"))
        self.button_configureLegend.setText(_translate("PrintDialog", "Configure"))
from qgis import gui
