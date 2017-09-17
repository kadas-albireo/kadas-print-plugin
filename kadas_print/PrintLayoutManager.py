# -*- coding: utf-8 -*-
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    copyright            : (C) 2015 by Sourcepole AG

from ui.ui_printlayoutmanager import Ui_PrintLayoutManager

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtXml import *

from qgis.core import *


class PrintLayoutManager(QDialog, Ui_PrintLayoutManager):

    def __init__(self, iface, parent=None):
        QDialog.__init__(self, parent)
        self.iface = iface
        self.setupUi(self)

        self.__reloadComposers()

        self.iface.compositionAdded.connect(lambda view: self.__reloadComposers())
        self.iface.compositionWillBeRemoved.connect(self.__reloadComposers)
        self.listWidgetLayouts.selectionModel().selectionChanged.connect(self.__listSelectionChanged)
        self.pushButtonImport.clicked.connect(self.__import)
        self.pushButtonExport.clicked.connect(self.__export)
        self.pushButtonRemove.clicked.connect(self.__remove)

    def __reloadComposers(self, removedComposition=None):
        self.listWidgetLayouts.clear()
        for composition in self.iface.printCompositions():
            if composition != removedComposition:
                title = composition.title()
                item = QListWidgetItem(title)
                item.setData(Qt.UserRole, composition)
                self.listWidgetLayouts.addItem(item)
        self.listWidgetLayouts.sortItems()

    def __listSelectionChanged(self):
        selected = len(self.listWidgetLayouts.selectedItems()) > 0
        fixedMode = False
        if selected:
            composition = self.listWidgetLayouts.selectedItems()[0].data(Qt.UserRole)
            composition.__class__ = QgsComposition
            fixedMode = composition.title() == "Custom"
        self.pushButtonExport.setEnabled(selected)
        self.pushButtonRemove.setEnabled(selected and not fixedMode)

    def __import(self):
        lastDir = QSettings().value( "/UI/lastImportExportDir", "." )
        filename = QFileDialog.getOpenFileName(self, self.tr("Import Layout"), lastDir, self.tr("QPT Files (*.qpt);;"))
        if type(filename) == tuple: filename = filename[0]
        if not filename:
            return
        QSettings().setValue("/UI/lastImportExportDir", QFileInfo(filename).absolutePath())
        file = QFile(filename)
        if not file.open(QIODevice.ReadOnly):
            QMessageBox.critical(self, self.tr("Import Failed"), self.tr("Failed to open the input file for reading."), QMessageBox.Ok)
        else:
            doc = QDomDocument()
            doc.setContent(file)
            composerEls = doc.elementsByTagName("Composer")
            if len(composerEls) == 0:
                QMessageBox.critical(self, self.tr("Import Failed"), self.tr("The file does not appear to be a valid print layout."), QMessageBox.Ok)
                return
            composerEl = composerEls.at(0).toElement()
            composition = self.iface.createNewComposition(composerEl.attribute("title"))
            if not composition.loadFromTemplate(doc):
                QMessageBox.critical(self, self.tr("Import Failed"), self.tr("The file does not appear to be a valid print layout."), QMessageBox.Ok)
                self.iface.deleteComposition(composition)

    def __export(self):
        item = self.listWidgetLayouts.selectedItems()[0]
        composition = item.data(Qt.UserRole)
        composition.__class__ = QgsComposition
        doc = QDomDocument()
        composition.writeXML(doc, doc)

        lastDir = QSettings().value( "/UI/lastImportExportDir", "." )
        filename = QFileDialog.getSaveFileName(self, self.tr("Export Layout"), lastDir, self.tr("QPT Files (*.qpt);;"))
        if type(filename) == tuple: filename = filename[0]
        if not filename:
            return
        QSettings().setValue("/UI/lastImportExportDir", QFileInfo(filename).absolutePath())
        file = QFile(filename)
        if not file.open(QIODevice.WriteOnly):
            QMessageBox.critical(self, self.tr("Export Failed"), self.tr("Failed to open the output file for writing."), QMessageBox.Ok)
        else:
            file.write(bytes(doc.toString()))

    def __remove(self):
        item = self.listWidgetLayouts.selectedItems()[0]
        composition = item.data(Qt.UserRole)
        composition.__class__ = QgsComposition
        self.iface.deleteComposition(composition)
