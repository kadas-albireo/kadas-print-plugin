# -*- coding: utf-8 -*-
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    copyright            : (C) 2015 by Sourcepole AG

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

from ui.ui_cartouchedialog import Ui_CartoucheDialog

class CartoucheDialog(QDialog, Ui_CartoucheDialog):
    def __init__(self, scene, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.scene = scene
        self.mapcartoucheView.setInteractive(False)

        self.exercisedateLE.dateChanged.connect(self.updateComposition)
        self.classification1.currentIndexChanged.connect(self.updateComposition)
        self.classification2.currentIndexChanged.connect(self.updateComposition)
        self.classification1.lineEdit().textEdited.connect(self.updateComposition)
        self.classification2.lineEdit().textEdited.connect(self.updateComposition)
        self.exerciseorganisationLE.textEdited.connect(self.updateComposition)
        self.coursetitleLE.textEdited.connect(self.updateComposition)
        self.troopstitleLE.textEdited.connect(self.updateComposition)
        self.codenameLE.textEdited.connect(self.updateComposition)
        self.cartouchecircumscriptionLE.textEdited.connect(self.updateComposition)
        self.supplementtitleLE.textEdited.connect(self.updateComposition)
        self.scaletitleLE.textEdited.connect(self.updateComposition)
        self.exercisetitleLE.textEdited.connect(self.updateComposition)
        self.documenttitleLE.textEdited.connect(self.updateComposition)
        self.placedateLE.textEdited.connect(self.updateComposition)
        self.bz1LE.textEdited.connect(self.updateComposition)
        self.bz2LE.textEdited.connect(self.updateComposition)
        self.bz3LE.textEdited.connect(self.updateComposition)
        self.exerciseGroupBox.toggled.connect(self.updateComposition)

        self.mapcartoucheView.setScene(self.scene)
        self.mapcartoucheView.resizeEvent = self.__resizeEvent

        self.updateUi()

    def __resizeEvent(self, ev):
        cartouche = self.scene.getComposerItemById("mapcartouche")
        if cartouche:
            self.mapcartoucheView.fitInView(cartouche, Qt.KeepAspectRatio)

    def updateUi(self):
        self.codenameLE.setText(unicode(self.__getComposerItemText("codename")))
        self.troopstitleLE.setText(unicode(self.__getComposerItemText("troopstitle")))
        self.supplementtitleLE.setText(unicode(self.__getComposerItemText("supplementtitle")))
        self.cartouchecircumscriptionLE.setText(unicode(self.__getComposerItemText("cartouchecircumscription")))
        self.scaletitleLE.setText(unicode(self.__getComposerItemText("scaletitle")))
        self.placedateLE.setText(unicode(self.__getComposerItemText("placedate")))
        self.exerciseorganisationLE.setText(unicode(self.__getComposerItemText("exerciseorganisation")))
        self.coursetitleLE.setText(unicode(self.__getComposerItemText("coursetitle")))
        self.exercisetitleLE.setText(unicode(self.__getComposerItemText("exercisetitle")))
        self.documenttitleLE.setText(unicode(self.__getComposerItemText("documenttitle")))
        self.exercisedateLE.setDate(QDate.currentDate())


    def updateComposition(self, x=None):
        self.__setComposerItemText("classification1", unicode(self.classification2.currentText()))
        self.__setComposerItemText("troopstitle", unicode(self.troopstitleLE.text()))
        self.__setComposerItemText("codename", unicode(self.codenameLE.text()))
        self.__setComposerItemText("cartouchecircumscription", unicode(self.cartouchecircumscriptionLE.text()))
        self.__setComposerItemText("supplementtitle", unicode(self.supplementtitleLE.text()))
        self.__setComposerItemText("scaletitle", unicode(self.scaletitleLE.text()))
        self.__setComposerItemText("placedate", unicode(self.placedateLE.text()))
        self.__setComposerItemText("bz1", unicode(self.bz1LE.text()))
        self.__setComposerItemText("bz2", unicode(self.bz2LE.text()))
        self.__setComposerItemText("bz3", unicode(self.bz3LE.text()))

        if self.exerciseGroupBox.isChecked():
            self.__setComposerItemText("exercisedate", unicode(self.exercisedateLE.text()))
            self.__setComposerItemText("classification2", unicode(self.classification1.currentText()))
            self.__setComposerItemText("exerciseorganisation", unicode(self.exerciseorganisationLE.text()))
            self.__setComposerItemText("coursetitle", unicode(self.coursetitleLE.text()))
            self.__setComposerItemText("exercisetitle", unicode(self.exercisetitleLE.text()))
            self.__setComposerItemText("documenttitle", unicode(self.documenttitleLE.text()))
        else:
            self.__setComposerItemText("exercisedate", "")
            self.__setComposerItemText("classification2", "")
            self.__setComposerItemText("exerciseorganisation", "")
            self.__setComposerItemText("coursetitle", "")
            self.__setComposerItemText("exercisetitle", "")
            self.__setComposerItemText("documenttitle", "")

        self.scene.update()
        self.mapcartoucheView.update()

    def __setComposerItemText(self, itemid, text):
        item = self.scene.getComposerItemById(itemid)
        if item:
            item.setText(text)

    def __getComposerItemText(self, itemid):
        try:
            return self.scene.getComposerItemById(itemid).text()
        except:
            return ""
