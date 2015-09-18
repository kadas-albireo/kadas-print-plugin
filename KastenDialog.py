from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

from ui.ui_kastendialog import Ui_KastenDialog

class Kasten(QDialog, Ui_KastenDialog):
    def __init__(self, scene, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.scene = scene
        self.kartenkartuscheView.setInteractive(False)
        self.kartusche = self.scene.getComposerItemById("kartenkartusche")

        self.uebungsdatumLE.textChanged.connect(self.valueChanged)
        self.klassifizierungLE.textChanged.connect(self.valueChanged)
        self.uebungsorganisationLE.textChanged.connect(self.valueChanged)
        self.kursbezeichnungLE.textChanged.connect(self.valueChanged)
        self.truppenbezeichnungLE.textChanged.connect(self.valueChanged)
        self.decknameLE.textChanged.connect(self.valueChanged)
        self.kartenumschreibungLE.textChanged.connect(self.valueChanged)
        self.beilagebezeichnungLE.textChanged.connect(self.valueChanged)
        self.massstabbezeichnungLE.textChanged.connect(self.valueChanged)
        self.uebungsbezeichnungLE.textChanged.connect(self.valueChanged)
        self.dokumentbezeichnungLE.textChanged.connect(self.valueChanged)
        self.ortdatumLE.textChanged.connect(self.valueChanged)
        self.uebungGroupBox.toggled.connect(self.boxChanged)

        self.kartenkartuscheView.setScene(self.scene)
        # self.kartenkartuscheView.fitInView(self.kartusche, Qt.KeepAspectRatio)
        self.kartenkartuscheView.setSceneRect(self.kartusche.mapRectToScene(self.kartusche.boundingRect()))

    def insertLE(self):
        self.truppenbezeichnungLE.setText(self.scene.getComposerItemById("truppenbezeichnung").text())
        self.decknameLE.setText(self.scene.getComposerItemById("deckname").text())
        self.kartenumschreibungLE.setText(self.scene.getComposerItemById("kartenumschreibung").text())
        self.beilagebezeichnungLE.setText(self.scene.getComposerItemById("beilagebezeichnung").text())
        self.massstabbezeichnungLE.setText(self.scene.getComposerItemById("massstabbezeichnung").text())
        self.ortdatumLE.setText(self.scene.getComposerItemById("ortdatum").text())

        if self.uebungGroupBox.isChecked():
            self.uebungsdatumLE.setText(self.scene.getComposerItemById("uebungsdatum").text())
            self.klassifizierungLE.setText(self.scene.getComposerItemById("klassifizierung1").text())
            self.uebungsorganisationLE.setText(self.scene.getComposerItemById("uebungsorganisation").text())
            self.kursbezeichnungLE.setText(self.scene.getComposerItemById("kursbezeichnung").text())
            self.uebungsbezeichnungLE.setText(self.scene.getComposerItemById("uebungsbezeichnung").text())
            self.dokumentbezeichnungLE.setText(self.scene.getComposerItemById("dokumentbezeichnung").text())

    def valueChanged(self,value):
        self.scene.getComposerItemById("klassifizierung1").setText(unicode(self.klassifizierungLE.text()))
        self.scene.getComposerItemById("truppenbezeichnung").setText(unicode(self.truppenbezeichnungLE.text()))
        self.scene.getComposerItemById("deckname").setText(unicode(self.decknameLE.text()))
        self.scene.getComposerItemById("kartenumschreibung").setText(unicode(self.kartenumschreibungLE.text()))
        self.scene.getComposerItemById("beilagebezeichnung").setText(unicode(self.beilagebezeichnungLE.text()))
        self.scene.getComposerItemById("massstabbezeichnung").setText(unicode(self.massstabbezeichnungLE.text()))
        self.scene.getComposerItemById("ortdatum").setText(unicode(self.ortdatumLE.text()))

        if self.uebungGroupBox.isChecked():
            self.scene.getComposerItemById("uebungsdatum").setText(unicode(self.uebungsdatumLE.text()))
            self.scene.getComposerItemById("klassifizierung2").setText(unicode(self.klassifizierungLE.text()))
            self.scene.getComposerItemById("uebungsorganisation").setText(unicode(self.uebungsorganisationLE.text()))
            self.scene.getComposerItemById("kursbezeichnung").setText(unicode(self.kursbezeichnungLE.text()))
            self.scene.getComposerItemById("uebungsbezeichnung").setText(unicode(self.uebungsbezeichnungLE.text()))
            self.scene.getComposerItemById("dokumentbezeichnung").setText(unicode(self.dokumentbezeichnungLE.text()))

        self.scene.update()
        self.kartenkartuscheView.update()

    def boxChanged(self, active):
        if not active:
            self.scene.getComposerItemById("uebungsdatum").setText("")
            self.scene.getComposerItemById("klassifizierung2").setText("")
            self.scene.getComposerItemById("uebungsorganisation").setText("")
            self.scene.getComposerItemById("kursbezeichnung").setText("")
            self.scene.getComposerItemById("uebungsbezeichnung").setText("")
            self.scene.getComposerItemById("dokumentbezeichnung").setText("")
        else:
            self.scene.getComposerItemById("uebungsdatum").setText(unicode(self.uebungsdatumLE.text()))
            self.scene.getComposerItemById("klassifizierung2").setText(unicode(self.klassifizierungLE.text()))
            self.scene.getComposerItemById("uebungsorganisation").setText(unicode(self.uebungsorganisationLE.text()))
            self.scene.getComposerItemById("kursbezeichnung").setText(unicode(self.kursbezeichnungLE.text()))
            self.scene.getComposerItemById("uebungsbezeichnung").setText(unicode(self.uebungsbezeichnungLE.text()))
            self.scene.getComposerItemById("dokumentbezeichnung").setText(unicode(self.dokumentbezeichnungLE.text()))
        self.scene.update()
        self.kartenkartuscheView.update()
