from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

from ui.ui_casedialog import Ui_CaseDialog

class Case(QDialog, Ui_CaseDialog):
    def __init__(self, scene, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.scene = scene
        self.mapcartridgeView.setInteractive(False)
        self.cartridge = self.scene.getComposerItemById("mapcartridge")

        self.exercisedateLE.textEdited.connect(self.valueChanged)
        self.classificationLE.textEdited.connect(self.valueChanged)
        self.exerciseorganisationLE.textEdited.connect(self.valueChanged)
        self.coursetitleLE.textEdited.connect(self.valueChanged)
        self.troopstitleLE.textEdited.connect(self.valueChanged)
        self.codenameLE.textEdited.connect(self.valueChanged)
        self.mapcircumscriptionLE.textEdited.connect(self.valueChanged)
        self.supplementtitleLE.textEdited.connect(self.valueChanged)
        self.scaletitleLE.textEdited.connect(self.valueChanged)
        self.exercisetitleLE.textEdited.connect(self.valueChanged)
        self.documenttitleLE.textEdited.connect(self.valueChanged)
        self.placedateLE.textEdited.connect(self.valueChanged)
        self.exerciseGroupBox.toggled.connect(self.boxChanged)

        self.mapcartridgeView.setScene(self.scene)
        # self.mapcartridgeView.fitInView(self.cartridge, Qt.KeepAspectRatio)
        self.mapcartridgeView.setSceneRect(self.cartridge.mapRectToScene(self.cartridge.boundingRect()))

    def insertLE(self):

        self.codenameLE.setText(unicode(self.scene.getComposerItemById("codename").text()))
        self.troopstitleLE.setText(unicode(self.scene.getComposerItemById("troopstitle").text()))
        self.supplementtitleLE.setText(unicode(self.scene.getComposerItemById("supplementtitle").text()))
        self.mapcircumscriptionLE.setText(unicode(self.scene.getComposerItemById("mapcircumscription").text()))
        self.scaletitleLE.setText(unicode(self.scene.getComposerItemById("scaletitle").text()))
        self.placedateLE.setText(unicode(self.scene.getComposerItemById("placedate").text()))
        self.exercisedateLE.setText(unicode(self.scene.getComposerItemById("exercisedate").text()))
        self.classificationLE.setText(unicode(self.scene.getComposerItemById("classification1").text()))
        self.exerciseorganisationLE.setText(unicode(self.scene.getComposerItemById("exerciseorganisation").text()))
        self.coursetitleLE.setText(unicode(self.scene.getComposerItemById("coursetitle").text()))
        self.exercisetitleLE.setText(unicode(self.scene.getComposerItemById("exercisetitle").text()))
        self.documenttitleLE.setText(unicode(self.scene.getComposerItemById("documenttitle").text()))

        if not self.exerciseGroupBox.isChecked():
            self.scene.getComposerItemById("exercisedate").setText("")
            self.scene.getComposerItemById("classification2").setText("")
            self.scene.getComposerItemById("exerciseorganisation").setText("")
            self.scene.getComposerItemById("coursetitle").setText("")
            self.scene.getComposerItemById("exercisetitle").setText("")
            self.scene.getComposerItemById("documenttitle").setText("")

    def valueChanged(self,value):
        self.scene.getComposerItemById("classification1").setText(unicode(self.classificationLE.text()))
        self.scene.getComposerItemById("troopstitle").setText(unicode(self.troopstitleLE.text()))
        self.scene.getComposerItemById("codename").setText(unicode(self.codenameLE.text()))
        self.scene.getComposerItemById("mapcircumscription").setText(unicode(self.mapcircumscriptionLE.text()))
        self.scene.getComposerItemById("supplementtitle").setText(unicode(self.supplementtitleLE.text()))
        self.scene.getComposerItemById("scaletitle").setText(unicode(self.scaletitleLE.text()))
        self.scene.getComposerItemById("placedate").setText(unicode(self.placedateLE.text()))

        if self.exerciseGroupBox.isChecked():
            self.scene.getComposerItemById("exercisedate").setText(unicode(self.exercisedateLE.text()))
            self.scene.getComposerItemById("classification2").setText(unicode(self.classificationLE.text()))
            self.scene.getComposerItemById("exerciseorganisation").setText(unicode(self.exerciseorganisationLE.text()))
            self.scene.getComposerItemById("coursetitle").setText(unicode(self.coursetitleLE.text()))
            self.scene.getComposerItemById("exercisetitle").setText(unicode(self.exercisetitleLE.text()))
            self.scene.getComposerItemById("documenttitle").setText(unicode(self.documenttitleLE.text()))

        self.scene.update()
        self.mapcartridgeView.update()

    def boxChanged(self, active):
        if not active:
            self.scene.getComposerItemById("exercisedate").setText("")
            self.scene.getComposerItemById("classification2").setText("")
            self.scene.getComposerItemById("exerciseorganisation").setText("")
            self.scene.getComposerItemById("coursetitle").setText("")
            self.scene.getComposerItemById("exercisetitle").setText("")
            self.scene.getComposerItemById("documenttitle").setText("")
        else:
            self.scene.getComposerItemById("exercisedate").setText(unicode(self.exercisedateLE.text()))
            self.scene.getComposerItemById("classification2").setText(unicode(self.classificationLE.text()))
            self.scene.getComposerItemById("exerciseorganisation").setText(unicode(self.exerciseorganisationLE.text()))
            self.scene.getComposerItemById("coursetitle").setText(unicode(self.coursetitleLE.text()))
            self.scene.getComposerItemById("exercisetitle").setText(unicode(self.exercisetitleLE.text()))
            self.scene.getComposerItemById("documenttitle").setText(unicode(self.documenttitleLE.text()))
        self.scene.update()
        self.mapcartridgeView.update()
