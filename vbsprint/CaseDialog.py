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
        self.mapcartoucheView.setInteractive(False)
        self.cartouche = self.scene.getComposerItemById("mapcartouche")

        self.exercisedateLE.dateChanged.connect(self.valueChanged)
        self.classification1.currentIndexChanged.connect(self.valueChanged)
        self.classification2.currentIndexChanged.connect(self.valueChanged)
        self.classification1.lineEdit().textEdited.connect(self.valueChanged)
        self.classification2.lineEdit().textEdited.connect(self.valueChanged)
        self.exerciseorganisationLE.textEdited.connect(self.valueChanged)
        self.coursetitleLE.textEdited.connect(self.valueChanged)
        self.troopstitleLE.textEdited.connect(self.valueChanged)
        self.codenameLE.textEdited.connect(self.valueChanged)
        self.cartouchecircumscriptionLE.textEdited.connect(self.valueChanged)
        self.supplementtitleLE.textEdited.connect(self.valueChanged)
        self.scaletitleLE.textEdited.connect(self.valueChanged)
        self.exercisetitleLE.textEdited.connect(self.valueChanged)
        self.documenttitleLE.textEdited.connect(self.valueChanged)
        self.placedateLE.textEdited.connect(self.valueChanged)
        self.exerciseGroupBox.toggled.connect(self.boxChanged)

        self.mapcartoucheView.setScene(self.scene)
        # self.mapcartoucheView.fitInView(self.cartouche, Qt.KeepAspectRatio)
        self.mapcartoucheView.setSceneRect(self.cartouche.mapRectToScene(self.cartouche.boundingRect()))

    def insertLE(self):

        self.codenameLE.setText(unicode(self.scene.getComposerItemById("codename").text()))
        self.troopstitleLE.setText(unicode(self.scene.getComposerItemById("troopstitle").text()))
        self.supplementtitleLE.setText(unicode(self.scene.getComposerItemById("supplementtitle").text()))
        self.cartouchecircumscriptionLE.setText(unicode(self.scene.getComposerItemById("cartouchecircumscription").text()))
        self.scaletitleLE.setText(unicode(self.scene.getComposerItemById("scaletitle").text()))
        self.placedateLE.setText(unicode(self.scene.getComposerItemById("placedate").text()))
        self.classification2.setItemText(self.classification2.currentIndex(), unicode(self.scene.getComposerItemById("classification1").text()))
        self.classification1.setItemText(self.classification1.currentIndex(), unicode(self.scene.getComposerItemById("classification2").text()))
        self.exerciseorganisationLE.setText(unicode(self.scene.getComposerItemById("exerciseorganisation").text()))
        self.coursetitleLE.setText(unicode(self.scene.getComposerItemById("coursetitle").text()))
        self.exercisetitleLE.setText(unicode(self.scene.getComposerItemById("exercisetitle").text()))
        self.documenttitleLE.setText(unicode(self.scene.getComposerItemById("documenttitle").text()))

        date = self.scene.getComposerItemById("exercisedate").text()
        if not date:
            date = QDate(0,0,0)
        else:
            y,m,d = date.split('.')
            date = QDate(int(y),int(m),int(d))
        self.exercisedateLE.setDate(date)

        if not self.exerciseGroupBox.isChecked():
            self.scene.getComposerItemById("exercisedate").setText("")
            self.scene.getComposerItemById("classification2").setText("")
            self.scene.getComposerItemById("exerciseorganisation").setText("")
            self.scene.getComposerItemById("coursetitle").setText("")
            self.scene.getComposerItemById("exercisetitle").setText("")
            self.scene.getComposerItemById("documenttitle").setText("")

    def valueChanged(self,value):
        self.scene.getComposerItemById("classification1").setText(unicode(self.classification2.currentText()))
        self.scene.getComposerItemById("troopstitle").setText(unicode(self.troopstitleLE.text()))
        self.scene.getComposerItemById("codename").setText(unicode(self.codenameLE.text()))
        self.scene.getComposerItemById("cartouchecircumscription").setText(unicode(self.cartouchecircumscriptionLE.text()))
        self.scene.getComposerItemById("supplementtitle").setText(unicode(self.supplementtitleLE.text()))
        self.scene.getComposerItemById("scaletitle").setText(unicode(self.scaletitleLE.text()))
        self.scene.getComposerItemById("placedate").setText(unicode(self.placedateLE.text()))

        if self.exerciseGroupBox.isChecked():
            self.scene.getComposerItemById("exercisedate").setText(unicode(self.exercisedateLE.text()))
            self.scene.getComposerItemById("classification2").setText(unicode(self.classification1.currentText()))
            self.scene.getComposerItemById("exerciseorganisation").setText(unicode(self.exerciseorganisationLE.text()))
            self.scene.getComposerItemById("coursetitle").setText(unicode(self.coursetitleLE.text()))
            self.scene.getComposerItemById("exercisetitle").setText(unicode(self.exercisetitleLE.text()))
            self.scene.getComposerItemById("documenttitle").setText(unicode(self.documenttitleLE.text()))

        self.scene.update()
        self.mapcartoucheView.update()

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
            self.scene.getComposerItemById("classification2").setText(unicode(self.classification1.currentText()))
            self.scene.getComposerItemById("exerciseorganisation").setText(unicode(self.exerciseorganisationLE.text()))
            self.scene.getComposerItemById("coursetitle").setText(unicode(self.coursetitleLE.text()))
            self.scene.getComposerItemById("exercisetitle").setText(unicode(self.exercisetitleLE.text()))
            self.scene.getComposerItemById("documenttitle").setText(unicode(self.documenttitleLE.text()))
        self.scene.update()
        self.mapcartoucheView.update()
