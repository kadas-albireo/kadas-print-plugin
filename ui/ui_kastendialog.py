# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'kastendialog.ui'
#
# Created: Fri Sep 18 10:59:49 2015
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

class Ui_KastenDialog(object):
    def setupUi(self, KastenDialog):
        KastenDialog.setObjectName(_fromUtf8("KastenDialog"))
        KastenDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        KastenDialog.resize(560, 566)
        self.gridLayout = QtGui.QGridLayout(KastenDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.kartenkartuscheView = QtGui.QGraphicsView(KastenDialog)
        self.kartenkartuscheView.setObjectName(_fromUtf8("kartenkartuscheView"))
        self.gridLayout.addWidget(self.kartenkartuscheView, 18, 0, 1, 1)
        self.uebungGroupBox = QtGui.QGroupBox(KastenDialog)
        self.uebungGroupBox.setCheckable(True)
        self.uebungGroupBox.setChecked(False)
        self.uebungGroupBox.setObjectName(_fromUtf8("uebungGroupBox"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.uebungGroupBox)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.frame = QtGui.QFrame(self.uebungGroupBox)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frame)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)
        self.kursbezeichnungLE = QtGui.QLineEdit(self.frame)
        self.kursbezeichnungLE.setObjectName(_fromUtf8("kursbezeichnungLE"))
        self.gridLayout_3.addWidget(self.kursbezeichnungLE, 3, 1, 1, 1)
        self.uebungsbezeichnungLE = QtGui.QLineEdit(self.frame)
        self.uebungsbezeichnungLE.setObjectName(_fromUtf8("uebungsbezeichnungLE"))
        self.gridLayout_3.addWidget(self.uebungsbezeichnungLE, 2, 3, 1, 1)
        self.label_12 = QtGui.QLabel(self.frame)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_3.addWidget(self.label_12, 3, 2, 1, 1)
        self.label_5 = QtGui.QLabel(self.frame)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_3.addWidget(self.label_5, 3, 0, 1, 1)
        self.uebungsorganisationLE = QtGui.QLineEdit(self.frame)
        self.uebungsorganisationLE.setObjectName(_fromUtf8("uebungsorganisationLE"))
        self.gridLayout_3.addWidget(self.uebungsorganisationLE, 2, 1, 1, 1)
        self.label_11 = QtGui.QLabel(self.frame)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_3.addWidget(self.label_11, 2, 2, 1, 1)
        self.label_4 = QtGui.QLabel(self.frame)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_3.addWidget(self.label_4, 2, 0, 1, 1)
        self.dokumentbezeichnungLE = QtGui.QLineEdit(self.frame)
        self.dokumentbezeichnungLE.setObjectName(_fromUtf8("dokumentbezeichnungLE"))
        self.gridLayout_3.addWidget(self.dokumentbezeichnungLE, 3, 3, 1, 1)
        self.uebungsdatumLE = QtGui.QLineEdit(self.frame)
        self.uebungsdatumLE.setObjectName(_fromUtf8("uebungsdatumLE"))
        self.gridLayout_3.addWidget(self.uebungsdatumLE, 1, 1, 1, 1)
        self.horizontalLayout_2.addWidget(self.frame)
        self.gridLayout.addWidget(self.uebungGroupBox, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(KastenDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 19, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_3 = QtGui.QLabel(KastenDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.klassifizierungLE = QtGui.QLineEdit(KastenDialog)
        self.klassifizierungLE.setObjectName(_fromUtf8("klassifizierungLE"))
        self.horizontalLayout.addWidget(self.klassifizierungLE)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.frame_2 = QtGui.QFrame(KastenDialog)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout_4 = QtGui.QGridLayout(self.frame_2)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_6 = QtGui.QLabel(self.frame_2)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_4.addWidget(self.label_6, 0, 0, 1, 1)
        self.ortdatumLE = QtGui.QLineEdit(self.frame_2)
        self.ortdatumLE.setObjectName(_fromUtf8("ortdatumLE"))
        self.gridLayout_4.addWidget(self.ortdatumLE, 0, 3, 1, 1)
        self.label_13 = QtGui.QLabel(self.frame_2)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout_4.addWidget(self.label_13, 0, 2, 1, 1)
        self.label_7 = QtGui.QLabel(self.frame_2)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_4.addWidget(self.label_7, 1, 0, 1, 1)
        self.label_8 = QtGui.QLabel(self.frame_2)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_4.addWidget(self.label_8, 2, 0, 1, 1)
        self.label_9 = QtGui.QLabel(self.frame_2)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_4.addWidget(self.label_9, 3, 0, 1, 1)
        self.truppenbezeichnungLE = QtGui.QLineEdit(self.frame_2)
        self.truppenbezeichnungLE.setObjectName(_fromUtf8("truppenbezeichnungLE"))
        self.gridLayout_4.addWidget(self.truppenbezeichnungLE, 0, 1, 1, 1)
        self.label_10 = QtGui.QLabel(self.frame_2)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_4.addWidget(self.label_10, 4, 0, 1, 1)
        self.decknameLE = QtGui.QLineEdit(self.frame_2)
        self.decknameLE.setObjectName(_fromUtf8("decknameLE"))
        self.gridLayout_4.addWidget(self.decknameLE, 1, 1, 1, 1)
        self.kartenumschreibungLE = QtGui.QLineEdit(self.frame_2)
        self.kartenumschreibungLE.setObjectName(_fromUtf8("kartenumschreibungLE"))
        self.gridLayout_4.addWidget(self.kartenumschreibungLE, 2, 1, 1, 1)
        self.beilagebezeichnungLE = QtGui.QLineEdit(self.frame_2)
        self.beilagebezeichnungLE.setObjectName(_fromUtf8("beilagebezeichnungLE"))
        self.gridLayout_4.addWidget(self.beilagebezeichnungLE, 3, 1, 1, 1)
        self.massstabbezeichnungLE = QtGui.QLineEdit(self.frame_2)
        self.massstabbezeichnungLE.setObjectName(_fromUtf8("massstabbezeichnungLE"))
        self.gridLayout_4.addWidget(self.massstabbezeichnungLE, 4, 1, 1, 1)
        self.gridLayout.addWidget(self.frame_2, 2, 0, 1, 1)

        self.retranslateUi(KastenDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), KastenDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), KastenDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(KastenDialog)

    def retranslateUi(self, KastenDialog):
        KastenDialog.setWindowTitle(_translate("KastenDialog", "Kartenkartusche", None))
        self.uebungGroupBox.setTitle(_translate("KastenDialog", "Uebung", None))
        self.label_2.setText(_translate("KastenDialog", "Übungsdatum:", None))
        self.label_12.setText(_translate("KastenDialog", "Dokumentbezeichnung:", None))
        self.label_5.setText(_translate("KastenDialog", "Kursbezeichnung:", None))
        self.label_11.setText(_translate("KastenDialog", "Übungsbezeichnung:", None))
        self.label_4.setText(_translate("KastenDialog", "Übungsorganisation:", None))
        self.label_3.setText(_translate("KastenDialog", "Klassifizierung:", None))
        self.label_6.setText(_translate("KastenDialog", "Truppenbezeichnung:", None))
        self.label_13.setText(_translate("KastenDialog", "Ort, Datum:", None))
        self.label_7.setText(_translate("KastenDialog", "Deckname:", None))
        self.label_8.setText(_translate("KastenDialog", "Kartenumschreibung:", None))
        self.label_9.setText(_translate("KastenDialog", "Beilagebezeichnung:", None))
        self.label_10.setText(_translate("KastenDialog", "Massstabbezeichnung:", None))

