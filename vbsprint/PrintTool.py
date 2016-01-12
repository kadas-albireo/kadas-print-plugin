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
import os
import math

from CartoucheDialog import CartoucheDialog
from ui.ui_printdialog import Ui_PrintDialog


class PrintTool(QgsMapTool):

    def __init__(self, iface):
        QgsMapTool.__init__(self, iface.mapCanvas())
        self.setCursor(Qt.OpenHandCursor)

        self.iface = iface
        self.rubberband = None
        self.oldrubberband = None
        self.pressPos = None
        self.fixedSizeMode = True
        self.mapitem = None
        self.printing = False

        self.dialog = QDialog(self.iface.mainWindow())
        self.dialogui = Ui_PrintDialog()
        self.dialogui.setupUi(self.dialog)
        self.exportButton = self.dialogui.buttonBox.addButton(self.tr("Export"), QDialogButtonBox.ActionRole)
        self.printButton = self.dialogui.buttonBox.addButton(self.tr("Print"), QDialogButtonBox.ActionRole)
        self.advancedButton = self.dialogui.buttonBox.addButton(self.tr("Advanced"), QDialogButtonBox.HelpRole)
        self.dialogui.comboBox_fileformat.addItem("PDF", self.tr("PDF Document (*.pdf);;"))
        self.dialogui.comboBox_fileformat.addItem("JPG", self.tr("JPG Image (*.jpg);;"))
        self.dialogui.comboBox_fileformat.addItem("BMP", self.tr("BMP Image (*.bmp);;"))
        self.dialogui.comboBox_fileformat.addItem("PNG", self.tr("PNG Image (*.png);;"))

        self.dialogui.comboBox_crs.addItem("LV03", "EPSG:21781,0")
        self.dialogui.comboBox_crs.addItem("LV95", "EPSG:2056,0")
        self.dialogui.comboBox_crs.addItem("DD", "EPSG:4326,0")
        self.dialogui.comboBox_crs.addItem("DM", "EPSG:4326,minute")
        self.dialogui.comboBox_crs.addItem("DMS", "EPSG:4326,second")
        self.dialogui.comboBox_crs.addItem("MGRS", "EPSG:4326,MGRS")
        self.dialogui.comboBox_crs.addItem("UTM", "EPSG:4326,UTM")

        self.dialogui.lineedit_xmin.setValidator(QDoubleValidator())
        self.dialogui.lineedit_xmax.setValidator(QDoubleValidator())
        self.dialogui.lineedit_ymin.setValidator(QDoubleValidator())
        self.dialogui.lineedit_ymax.setValidator(QDoubleValidator())

        self.dialogui.previewGraphic.resizeEvent = self.__resizePreview

        self.iface.composerAdded.connect(lambda view: self.__reloadComposers(view, True))
        self.iface.composerWillBeRemoved.connect(lambda view: self.__reloadComposers(view, False))
        self.dialogui.comboBox_composers.currentIndexChanged.connect(self.__selectComposer)
        self.dialogui.lineEdit_title.textChanged.connect(self.__titleChanged)
        self.dialogui.spinBox_scale.valueChanged.connect(self.__changeScale)
        self.dialogui.spinBox_border.valueChanged.connect(self.__generateComposer)
        self.dialogui.lineedit_xmin.editingFinished.connect(self.__generateComposer)
        self.dialogui.lineedit_xmax.editingFinished.connect(self.__generateComposer)
        self.dialogui.lineedit_ymin.editingFinished.connect(self.__generateComposer)
        self.dialogui.lineedit_ymax.editingFinished.connect(self.__generateComposer)
        self.dialogui.button_mapCartouche.clicked.connect(self.__showCartoucheDialog)
        self.dialogui.comboBox_crs.currentIndexChanged.connect(self.__setupGrid)
        self.dialogui.checkBox_gridAnnotations.toggled.connect(self.__toggleGridAnnotations)
        self.dialogui.checkBox_legend.toggled.connect(self.__toggleLegend)
        self.dialogui.checkBox_scalebar.toggled.connect(self.__toggleScalebar)
        self.dialogui.checkBox_mapCartouche.toggled.connect(self.__toggleMapCartouche)
        self.dialogui.spinBox_intervalx.valueChanged.connect(self.__intervalXChanged)
        self.dialogui.spinBox_intervaly.valueChanged.connect(self.__intervalYChanged)
        self.exportButton.clicked.connect(self.__export)
        self.printButton.clicked.connect(self.__print)
        self.advancedButton.clicked.connect(self.__advanced)
        self.dialog.finished.connect(lambda: self.setToolEnabled(False))
        self.dialogui.groupBox_grid.collapsedStateChanged.connect(self.__setupGrid)
        self.iface.mapCanvas().mapCanvasRefreshed.connect(self.__updateMap)
        self.iface.mapCanvas().mapUnitsChanged.connect(self.__mapUnitsChanged)

        self.__setUiEnabled(False)

    def __resizePreview(self, ev=None):
        try:
            page = self.composerView.composition().pages()[0]
            self.dialogui.previewGraphic.fitInView(page, Qt.KeepAspectRatio)
        except:
            pass

    def __updateMap(self):
        if self.mapitem and not self.printing:
            self.mapitem.cache()
            self.mapitem.updateItem()

    def __mapUnitsChanged(self):
        if not self.fixedSizeMode and self.iface.mapCanvas().mapSettings().mapUnits() != QGis.Meters:
            self.__setUiEnabled(False)
            self.dialogui.label_unitWarning.setVisible(True)
        elif self.dialogui.label_unitWarning.isVisible():
            self.__setUiEnabled(True)
            self.__initComposer()

    def __initComposer(self):
        self.title = self.composerView.composition().getComposerItemById("title")
        self.legend = self.composerView.composition().getComposerItemById("legend")
        self.scalebar = self.composerView.composition().getComposerItemById("scalebar")
        self.mapcartouche = self.composerView.composition().getComposerItemById("mapcartouche")
        self.grid = self.mapitem.grid()
        self.cartouchedialog = CartoucheDialog(self.composerView.composition(), self.dialog)

        self.mapitem.setPreviewMode(1)
        if not self.fixedSizeMode:
            extent = self.iface.mapCanvas().extent()
            self.dialogui.spinBox_scale.blockSignals(True)
            self.dialogui.spinBox_scale.setValue(self.iface.mapCanvas().scale())
            self.dialogui.spinBox_scale.blockSignals(False)
            self.dialogui.lineedit_xmin.setText(str(round(extent.xMinimum())))
            self.dialogui.lineedit_xmax.setText(str(round(extent.xMaximum())))
            self.dialogui.lineedit_ymin.setText(str(round(extent.yMinimum())))
            self.dialogui.lineedit_ymax.setText(str(round(extent.yMaximum())))
            self.__generateComposer()
        else:
            extent = self.iface.mapCanvas().extent()
            extentheight = self.mapitem.rect().height() / self.mapitem.rect().width() * extent.width()
            center = extent.center().y()
            extent.setYMinimum(center - extentheight / 2.)
            extent.setYMaximum(center + extentheight / 2.)
            self.mapitem.setNewExtent(extent)
            self.dialogui.spinBox_scale.blockSignals(True)
            self.dialogui.spinBox_scale.setValue(self.mapitem.scale())
            self.dialogui.spinBox_scale.blockSignals(False)
        self.mapitem.cache()
        self.mapitem.updateItem()
        self.dialogui.previewGraphic.setScene(self.composerView.composition())
        self.__resizePreview()
        self.__updateView()
        self.__createRubberBand()

        if not self.title:
            self.dialogui.lineEdit_title.setEnabled(False)
        else:
            self.title.setText(self.dialogui.lineEdit_title.text())
        if not self.legend:
            self.dialogui.checkBox_legend.setEnabled(False)
        else:
            self.legend.setVisible(self.dialogui.checkBox_legend.isChecked())
        if not self.scalebar:
            self.dialogui.checkBox_scalebar.setEnabled(False)
        else:
            self.scalebar.setVisible(self.dialogui.checkBox_scalebar.isChecked())
        if not self.grid:
            self.dialogui.groupBox_grid.setEnabled(False)
        else:
            self.__setupGrid()
        if not self.mapcartouche:
            self.dialogui.checkBox_mapCartouche.setEnabled(False)
        else:
            self.mapcartouche.setVisibility(self.dialogui.checkBox_mapCartouche.isChecked())
        self.mapitem.setGridEnabled(not self.dialogui.groupBox_grid.isCollapsed())

    def setToolEnabled(self, enabled):
        if enabled:
            self.dialog.show()
            self.__reloadComposers()
            self.iface.mapCanvas().setMapTool(self)
        else:
            self.mapitem = None
            self.dialog.hide()
            self.__clearRubberBand()
            self.iface.mapCanvas().unsetMapTool(self)

    def canvasPressEvent(self, e):
        if not self.rubberband or not self.fixedSizeMode:
            return
        r = self.__canvasRect(self.rect)
        if e.button() == Qt.LeftButton and self.__canvasRect(self.rect).contains(e.pos()):
            self.oldrect = QRectF(self.rect)
            self.oldrubberband = QgsRubberBand(self.iface.mapCanvas(), QGis.Polygon)
            self.oldrubberband.setToCanvasRectangle(self.__canvasRect(self.oldrect))
            self.oldrubberband.setColor(QColor(127, 127, 255, 31))
            self.pressPos = (e.x(), e.y())
            self.iface.mapCanvas().setCursor(Qt.ClosedHandCursor)

    def canvasMoveEvent(self, e):
        if not self.pressPos:
            return
        mup = self.iface.mapCanvas().mapSettings().mapUnitsPerPixel()
        x = self.corner.x() + (e.x() - self.pressPos[0]) * mup
        y = self.corner.y() + (self.pressPos[1] - e.y()) * mup

        snaptol = 10 * mup
        # Left edge matches with old right
        if abs(x - (self.oldrect.x() + self.oldrect.width())) < snaptol:
            x = self.oldrect.x() + self.oldrect.width()
        # Right edge matches with old left
        elif abs(x + self.rect.width() - self.oldrect.x()) < snaptol:
            x = self.oldrect.x() - self.rect.width()
        # Left edge matches with old left
        elif abs(x - self.oldrect.x()) < snaptol:
            x = self.oldrect.x()
        # Bottom edge matches with old top
        if abs(y - (self.oldrect.y() + self.oldrect.height())) < snaptol:
            y = self.oldrect.y() + self.oldrect.height()
        # Top edge matches with old bottom
        elif abs(y + self.rect.height() - self.oldrect.y()) < snaptol:
            y = self.oldrect.y() - self.rect.height()
        # Bottom edge matches with old bottom
        elif abs(y - self.oldrect.y()) < snaptol:
            y = self.oldrect.y()

        self.rect = QRectF(
            x,
            y,
            self.rect.width(),
            self.rect.height()
        )
        self.rubberband.setToCanvasRectangle(self.__canvasRect(self.rect))

    def canvasReleaseEvent(self, e):
        if e.button() == Qt.LeftButton and self.pressPos:
            self.corner = QPointF(self.rect.x(), self.rect.y())
            self.pressPos = None
            self.iface.mapCanvas().setCursor(Qt.OpenHandCursor)
            self.iface.mapCanvas().scene().removeItem(self.oldrubberband)
            self.oldrect = None
            self.oldrubberband = None
            self.mapitem.setNewExtent(QgsRectangle(self.rect))

    def __setupGrid(self):
        if not self.mapitem:
            return
        if self.dialogui.groupBox_grid.isCollapsed():
            self.mapitem.setGridEnabled(False)
        else:
            crs, format = self.dialogui.comboBox_crs.itemData(self.dialogui.comboBox_crs.currentIndex()).split(",")
            self.mapitem.setGridEnabled(True)
            self.grid.setCrs(QgsCoordinateReferenceSystem(crs))
            if format == '0':
                self.mapitem.setGridAnnotationFormat(0)
                self.grid.setAnnotationPrecision(5)
            elif format == 'second':
                self.grid.setAnnotationPrecision(1)
                self.mapitem.setGridAnnotationFormat(QgsComposerMap.DegreeMinuteSecond)
            elif format == 'minute':
                self.grid.setAnnotationPrecision(3)
                self.mapitem.setGridAnnotationFormat(QgsComposerMap.DegreeMinute)
            elif format == 'MGRS':
                self.grid.setAnnotationFormat(QgsComposerMapGrid.MGRS)
                self.grid.setAnnotationPrecision(0)
            elif format == 'UTM':
                self.grid.setAnnotationFormat(QgsComposerMapGrid.UTM)
                self.grid.setAnnotationPrecision(0)

            if crs != "EPSG:4326":
                self.grid.setAnnotationDisplay(QgsComposerMapGrid.HideAll, QgsComposerMapGrid.Top)
                self.grid.setAnnotationDisplay(QgsComposerMapGrid.HideAll, QgsComposerMapGrid.Right)
                self.grid.setAnnotationDisplay(QgsComposerMapGrid.LongitudeOnly, QgsComposerMapGrid.Bottom)
                self.grid.setAnnotationDisplay(QgsComposerMapGrid.LatitudeOnly, QgsComposerMapGrid.Left)
                self.grid.setAnnotationPrecision(0)
            else:
                self.grid.setAnnotationDisplay(QgsComposerMapGrid.LongitudeOnly, QgsComposerMapGrid.Top)
                self.grid.setAnnotationDisplay(QgsComposerMapGrid.LatitudeOnly, QgsComposerMapGrid.Right)
                self.grid.setAnnotationDisplay(QgsComposerMapGrid.LongitudeOnly, QgsComposerMapGrid.Bottom)
                self.grid.setAnnotationDisplay(QgsComposerMapGrid.LatitudeOnly, QgsComposerMapGrid.Left)

            interval = round(self.rect.width() / 1000) * 100
            self.dialogui.spinBox_intervalx.blockSignals(True)
            self.dialogui.spinBox_intervalx.setValue(interval)
            self.dialogui.spinBox_intervalx.blockSignals(False)
            self.dialogui.spinBox_intervaly.blockSignals(True)
            self.dialogui.spinBox_intervaly.setValue(interval)
            self.dialogui.spinBox_intervaly.blockSignals(False)
            self.mapitem.setGridIntervalX(interval)
            self.mapitem.setGridIntervalY(interval)

        self.__updateView()

    def __showCartoucheDialog(self):
        self.cartouchedialog.exec_()

    def __intervalXChanged(self, value):
        self.mapitem.setGridIntervalX(value)
        self.__updateView()

    def __intervalYChanged(self, value):
        self.mapitem.setGridIntervalY(value)
        self.__updateView()

    def __titleChanged(self, arg):
        self.title.setText(unicode(self.dialogui.lineEdit_title.text()))
        self.__updateView()

    def __toggleGridAnnotations(self, active):
        self.mapitem.setShowGridAnnotation(active)
        self.__updateView()

    def __toggleLegend(self, active):
        self.legend.setVisible(active)
        self.__updateView()

    def __toggleScalebar(self, active):
        self.scalebar.setVisible(active)
        self.__updateView()

    def __toggleMapCartouche(self, active):
        self.dialogui.button_mapCartouche.setEnabled(active)
        self.mapcartouche.setVisibility(active)
        self.__updateView()

    def __changeScale(self):
        if self.fixedSizeMode:
            self.mapitem.setNewScale(self.dialogui.spinBox_scale.value())
            self.__createRubberBand()
        else:
            self.__generateComposer()

    def __updateView(self):
        self.composerView.composition().update()
        self.dialogui.previewGraphic.update()

    def __reloadComposers(self, changedView=None, added=False):
        self.cartouchedialog = None
        self.mapitem = 0
        self.dialogui.comboBox_composers.blockSignals(True)
        prev = self.dialogui.comboBox_composers.currentText()
        self.dialogui.comboBox_composers.clear()
        active = 0
        for composer in self.iface.activeComposers():
            if (not changedView or added) and composer.composerWindow():
                cur = composer.composerWindow().windowTitle()
                self.dialogui.comboBox_composers.addItem(cur, composer)
                if prev == cur:
                    active = self.dialogui.comboBox_composers.count() - 1
        # Ensure that changed signal is emitted
        self.dialogui.comboBox_composers.setCurrentIndex(-1)
        self.dialogui.comboBox_composers.blockSignals(False)
        if self.dialogui.comboBox_composers.count() > 0:
            self.__setUiEnabled(True)
            self.dialogui.comboBox_composers.setCurrentIndex(active)
        else:
            self.__setUiEnabled(False)

    def __selectComposer(self):
        if not self.dialog.isVisible():
            return

        self.__clearRubberBand()
        self.mapitem = None
        try:
            activeIndex = self.dialogui.comboBox_composers.currentIndex()
            composerView = self.dialogui.comboBox_composers.itemData(activeIndex)
            self.fixedSizeMode = composerView.composerWindow().windowTitle() != "custom_extent"
        except:
            self.__setUiEnabled(False)
            return

        if not self.fixedSizeMode and self.iface.mapCanvas().mapSettings().mapUnits() != QGis.Meters:
            self.__setUiEnabled(False)
            self.dialogui.label_unitWarning.setVisible(True)
            return

        try:
            maps = composerView.composition().composerMapItems()
        except:
            # composerMapItems is not available with PyQt4 < 4.8.4
            maps = []
            for item in composerView.composition().items():
                if isinstance(item, QgsComposerMap):
                    maps.append(item)
        if len(maps) != 1:
            QMessageBox.warning(self.iface.mainWindow(), self.tr("Invalid composer"), self.tr("The composer must have exactly one map item."))
            self.__setUiEnabled(False)
            return

        self.__setUiEnabled(True)

        self.composerView = composerView
        self.mapitem = maps[0]
        self.__initComposer()

    def __generateComposer(self):
        scale = self.dialogui.spinBox_scale.value()
        try:
            xmin = float(self.dialogui.lineedit_xmin.text())
            ymin = float(self.dialogui.lineedit_ymin.text())
            xmax = float(self.dialogui.lineedit_xmax.text())
            ymax = float(self.dialogui.lineedit_ymax.text())
        except:
            # One or more extent inputs empty
            return
        border = self.dialogui.spinBox_border.value()
        borderdelta = border - self.mapitem.x()

        if xmin > xmax:
            tmp = xmin
            xmin = xmax
            xmax = tmp

        if ymin > ymax:
            tmp = ymin
            ymin = ymax
            ymax = tmp

        mapwidth = ((xmax - xmin) / scale * 1000.0)
        mapheight = ((ymax - ymin) / scale * 1000.0)

        self.mapitem.setSceneRect( QRectF(border, border, mapwidth, mapheight ) )
        self.mapitem.setPos(border, border)
        self.mapitem.setNewExtent(QgsRectangle(xmin, ymin, xmax, ymax))
        self.mapitem.setNewScale(scale)
        self.mapitem.updateItem()

        newwidth = 2 * border + mapwidth
        newheight = 2 * border + mapheight

        for item in self.composerView.composition().items():
            if item is not self.mapitem:
                item.moveBy(borderdelta, borderdelta)

        self.composerView.composition().setPaperSize(newwidth, newheight)
        self.dialogui.label_paperSize.setText(self.tr("Paper size: %.2f cm x %.2f cm") % (newwidth / 10., newheight / 10.))

        self.rect = QRectF(xmin, ymin, xmax - xmin, ymax - ymin)
        self.__createRubberBand()
        self.__resizePreview()
        self.__updateView()

    def __createRubberBand(self):
        self.__clearRubberBand()
        extent = self.mapitem.extent()
        center = self.iface.mapCanvas().extent().center()
        self.corner = QPointF(center.x() - 0.5 * extent.width(), center.y() - 0.5 * extent.height())
        self.rect = QRectF(self.corner.x(), self.corner.y(), extent.width(), extent.height())

        self.rubberband = QgsRubberBand(self.iface.mapCanvas(), QGis.Polygon)
        self.rubberband.setToCanvasRectangle(self.__canvasRect(self.rect))
        self.rubberband.setColor(QColor(127, 127, 255, 127))

        self.pressPos = None

    def __clearRubberBand(self):
        if self.rubberband:
            self.iface.mapCanvas().scene().removeItem(self.rubberband)
        if self.oldrubberband:
            self.iface.mapCanvas().scene().removeItem(self.oldrubberband)
        self.rubberband = None
        self.oldrubberband = None
        self.pressPos = None

    def __canvasRect(self, rect):
        mtp = self.iface.mapCanvas().mapSettings().mapToPixel()
        p1 = mtp.transform(QgsPoint(rect.left(), rect.top()))
        p2 = mtp.transform(QgsPoint(rect.right(), rect.bottom()))
        try:
            return QRect(int(p1.x()), int(p1.y()), int(p2.x() - p1.x()), int(p2.y() - p1.y()))
        except:
            return QRect(0, 0, 0, 0)

    def __export(self):
        settings = QSettings()
        format = self.dialogui.comboBox_fileformat.itemData(self.dialogui.comboBox_fileformat.currentIndex())
        filename = QFileDialog.getSaveFileName(
            self.iface.mainWindow(),
            self.tr("Print Composition"),
            settings.value("/print/lastfile", ""),
            format
        )
        if not filename:
            return

        self.printing = True

        # Ensure output filename has correct extension
        filename = os.path.splitext(filename)[0] + "." + self.dialogui.comboBox_fileformat.currentText().lower()

        settings.setValue("/print/lastfile", filename)

        success = False
        if filename[-3:].lower() == u"pdf":
            success = self.composerView.composition().exportAsPDF(filename)
        else:
            image = self.composerView.composition().printPageAsRaster(self.composerView.composition().itemPageNumber(self.mapitem))
            if not image.isNull():
                success = image.save(filename)
        if not success:
            QMessageBox.warning(self.iface.mainWindow(), self.tr("Print Failed"), self.tr("Failed to print the composition."))

        self.printing = False

    def __print(self):
        composer = self.composerView.composerWindow()
        composer.on_mActionPrint_triggered()

    def __setUiEnabled(self, enabled):
        self.dialogui.lineEdit_title.setEnabled(enabled)
        self.dialogui.spinBox_scale.setEnabled(enabled)
        self.dialogui.button_mapCartouche.setEnabled(self.dialogui.checkBox_mapCartouche.isChecked())
        self.dialogui.checkBox_legend.setEnabled(enabled)
        self.dialogui.checkBox_scalebar.setEnabled(enabled)
        self.dialogui.groupBox_grid.setEnabled(enabled)
        self.dialogui.comboBox_fileformat.setEnabled(enabled)
        self.dialogui.checkBox_mapCartouche.setEnabled(enabled)
        self.printButton.setEnabled(enabled)
        self.advancedButton.setEnabled(enabled)
        self.exportButton.setEnabled(enabled)
        self.__setVariableExtentUiVisibile(enabled and not self.fixedSizeMode)
        self.dialogui.label_unitWarning.setVisible(False)

    def __setVariableExtentUiVisibile(self, visible):
        self.dialogui.label_extent.setVisible(visible)
        self.dialogui.widget_extent.setVisible(visible)
        self.dialogui.label_border.setVisible(visible)
        self.dialogui.spinBox_border.setVisible(visible)
        self.dialogui.label_paperSize.setVisible(visible)

    def __advanced(self):
        composer = self.composerView.composerWindow()
        composer.showNormal()
