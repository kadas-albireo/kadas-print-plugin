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
from PrintLayoutManager import PrintLayoutManager
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
        self.composerView = None

        self.dialog = QDialog(self.iface.mainWindow())
        self.dialogui = Ui_PrintDialog()
        self.dialogui.setupUi(self.dialog)
        self.exportButton = self.dialogui.buttonBox.addButton(self.tr("Export"), QDialogButtonBox.ActionRole)
        self.printButton = self.dialogui.buttonBox.addButton(self.tr("Print"), QDialogButtonBox.ActionRole)
        self.advancedButton = self.dialogui.buttonBox.addButton(self.tr("Advanced"), QDialogButtonBox.HelpRole)

        proxy = QSortFilterProxyModel(self.dialogui.comboBox_composers)
        proxy.setSourceModel(self.dialogui.comboBox_composers.model())
        self.dialogui.comboBox_composers.model().setParent(proxy)
        self.dialogui.comboBox_composers.setModel(proxy)


        self.dialogui.comboBox_fileformat.addItem("PDF", self.tr("PDF Document (*.pdf);;"))
        self.dialogui.comboBox_fileformat.addItem("JPG", self.tr("JPG Image (*.jpg);;"))
        self.dialogui.comboBox_fileformat.addItem("BMP", self.tr("BMP Image (*.bmp);;"))
        self.dialogui.comboBox_fileformat.addItem("PNG", self.tr("PNG Image (*.png);;"))

        self.dialogui.comboBox_crs.addItem("LV95", "EPSG:2056,0")
        self.dialogui.comboBox_crs.addItem("LV03", "EPSG:21781,0")
        self.dialogui.comboBox_crs.addItem("DD", "EPSG:4326,0")
        self.dialogui.comboBox_crs.addItem("DM", "EPSG:4326,minute")
        self.dialogui.comboBox_crs.addItem("DMS", "EPSG:4326,second")
        self.dialogui.comboBox_crs.addItem("MGRS", "EPSG:4326,MGRS")
        self.dialogui.comboBox_crs.addItem("UTM", "EPSG:4326,UTM")

        self.dialogui.lineedit_xmin.setValidator(QDoubleValidator())
        self.dialogui.lineedit_xmax.setValidator(QDoubleValidator())
        self.dialogui.lineedit_ymin.setValidator(QDoubleValidator())
        self.dialogui.lineedit_ymax.setValidator(QDoubleValidator())

        self.dialogui.checkBox_gridAnnotations.setChecked(True)

        self.dialogui.previewGraphic.resizeEvent = self.__resizePreview

        self.iface.composerAdded.connect(lambda view: self.__reloadComposers())
        self.iface.composerWillBeRemoved.connect(self.__reloadComposers)
        self.dialogui.comboBox_composers.currentIndexChanged.connect(self.__selectComposer)
        self.dialogui.toolButton_layoutManager.clicked.connect(self.__manageLayouts)
        self.dialogui.lineEdit_title.textChanged.connect(self.__titleChanged)
        self.dialogui.comboBox_scale.scaleChanged.connect(self.__changeScale)
        self.dialogui.spinBox_border.valueChanged.connect(self.__generateComposer)
        self.dialogui.lineedit_xmin.editingFinished.connect(self.__generateComposer)
        self.dialogui.lineedit_xmax.editingFinished.connect(self.__generateComposer)
        self.dialogui.lineedit_ymin.editingFinished.connect(self.__generateComposer)
        self.dialogui.lineedit_ymax.editingFinished.connect(self.__generateComposer)
        self.dialogui.button_mapCartouche.clicked.connect(self.__showCartoucheDialog)
        self.dialogui.comboBox_crs.currentIndexChanged.connect(self.__setupGrid)
        self.dialogui.checkBox_gridAnnotations.toggled.connect(self.__toggleGridAnnotations)
        self.dialogui.checkBox_legend.toggled.connect(self.__toggleLegend)
        self.dialogui.button_configureLegend.clicked.connect(lambda: self.__configureLegend())
        self.dialogui.checkBox_scalebar.toggled.connect(self.__toggleScalebar)
        self.dialogui.checkBox_mapCartouche.toggled.connect(self.__toggleMapCartouche)
        self.dialogui.spinBox_intervalx.valueChanged.connect(self.__intervalXChanged)
        self.dialogui.spinBox_intervaly.valueChanged.connect(self.__intervalYChanged)
        self.dialogui.groupBox_grid.setChecked(True)
        self.exportButton.clicked.connect(self.__export)
        self.printButton.clicked.connect(self.__print)
        self.advancedButton.clicked.connect(self.__advanced)
        self.dialog.finished.connect(lambda: self.setToolEnabled(False))
        self.dialogui.groupBox_grid.toggled.connect(self.__setupGrid)
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

    def __composerItem(self, id, classtype):
        try:
            item = self.composerView.composition().getComposerItemById(id) if self.composerView else None
            if item:
                item.__class__ = classtype
                dir(item)
            return item
        except:
            return None

    def __initComposer(self):
        self.grid = self.mapitem.grid()
        self.cartouchedialog = CartoucheDialog(self.composerView.composition(), self.dialog)

        self.mapitem.setPreviewMode(1)
        if not self.fixedSizeMode:
            # Only update extent if it does not intersect with full extent of map
            extent = self.__getCustomExtent()
            if not extent or not self.iface.mapCanvas().fullExtent().contains(extent):
                extent = self.iface.mapCanvas().extent()
                self.dialogui.lineedit_xmin.setText(str(round(extent.xMinimum() + 0.125 * extent.width())))
                self.dialogui.lineedit_xmax.setText(str(round(extent.xMaximum() - 0.125 * extent.width())))
                self.dialogui.lineedit_ymin.setText(str(round(extent.yMinimum() + 0.125 * extent.height())))
                self.dialogui.lineedit_ymax.setText(str(round(extent.yMaximum() - 0.125 * extent.height())))
            self.__generateComposer()
        else:
            extent = self.iface.mapCanvas().extent()
            extentheight = self.mapitem.rect().height() / self.mapitem.rect().width() * extent.width()
            center = extent.center().y()
            extent.setYMinimum(center - extentheight / 2.)
            extent.setYMaximum(center + extentheight / 2.)
            self.mapitem.setNewExtent(extent)
        wmtsScales = []
        refRes = 0.0254 / self.composerView.composition().printResolution()
        try:
            resolutions = self.iface.mapCanvas().wmtsResolutions()
        except:
            resolutions = []
        minDist = -1
        bestScale = 1. / self.mapitem.scale()
        if resolutions:
            minDist = abs(1. / self.mapitem.scale() - refRes / resolutions[0])
        for resolution in resolutions:
            scale = refRes / resolution
            dist = abs(1. / self.mapitem.scale() - scale)
            if dist < minDist:
                minDist = dist
                bestScale = scale
            wmtsScales.append(QgsScaleComboBox.toString(scale))
        self.dialogui.comboBox_scale.updateScales(wmtsScales)
        self.dialogui.comboBox_scale.blockSignals(True)
        self.dialogui.comboBox_scale.setScale(bestScale)
        self.dialogui.comboBox_scale.blockSignals(False)
        self.mapitem.cache()
        self.mapitem.updateItem()
        self.dialogui.previewGraphic.setScene(self.composerView.composition())
        self.__resizePreview()
        self.__updateView()
        self.__changeScale()


        titleItem = self.__composerItem("title", QgsComposerLabel)
        if not titleItem:
            self.dialogui.lineEdit_title.setEnabled(False)
        else:
            titleItem.setText(self.dialogui.lineEdit_title.text())
            titleItem.setVisible(not not titleItem.text())
        legendItem = self.__composerItem("legend", QgsComposerLegend)
        if not legendItem:
            self.dialogui.checkBox_legend.setEnabled(False)
        else:
            legendItem.setVisible(self.dialogui.checkBox_legend.isChecked())
        scaleBarItem = self.__composerItem("scalebar", QgsComposerScaleBar)
        if not scaleBarItem:
            self.dialogui.checkBox_scalebar.setEnabled(False)
        else:
            scaleBarItem.setVisible(self.dialogui.checkBox_scalebar.isChecked())
        if not self.grid:
            self.dialogui.groupBox_grid.setEnabled(False)
        else:
            self.__setupGrid()
        cartoucheItem = self.__composerItem("mapcartouche", QgsComposerItemGroup)
        if not cartoucheItem:
            self.dialogui.checkBox_mapCartouche.setEnabled(False)
        else:
            cartoucheItem.setVisibility(self.dialogui.checkBox_mapCartouche.isChecked())
        self.mapitem.setGridEnabled(self.dialogui.groupBox_grid.isChecked())

    def setToolEnabled(self, enabled):
        if enabled:
            self.dialog.show()
            self.__reloadComposers()
            self.__configureLegend(False)
            self.iface.mapCanvas().setMapTool(self)
        else:
            self.mapitem = None
            self.composerView = None
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
        if not self.dialogui.groupBox_grid.isChecked():
            self.mapitem.setGridEnabled(False)
        else:
            crs, format = self.dialogui.comboBox_crs.itemData(self.dialogui.comboBox_crs.currentIndex()).split(",")
            self.mapitem.setGridEnabled(True)
            self.grid.setCrs(QgsCoordinateReferenceSystem(crs))
            try:
                if format == '0':
                    self.grid.setGridCrsType(QgsComposerMapGrid.CrsUserSelected)
                    self.mapitem.setGridAnnotationFormat(0)
                    self.grid.setAnnotationPrecision(5)
                elif format == 'second':
                    self.grid.setGridCrsType(QgsComposerMapGrid.CrsUserSelected)
                    self.grid.setAnnotationPrecision(1)
                    self.mapitem.setGridAnnotationFormat(QgsComposerMap.DegreeMinuteSecond)
                elif format == 'minute':
                    self.grid.setGridCrsType(QgsComposerMapGrid.CrsUserSelected)
                    self.grid.setAnnotationPrecision(3)
                    self.mapitem.setGridAnnotationFormat(QgsComposerMap.DegreeMinute)
                elif format == 'MGRS':
                    self.grid.setGridCrsType(QgsComposerMapGrid.CrsMGRS)
                elif format == 'UTM':
                    self.grid.setGridCrsType(QgsComposerMapGrid.CrsUTM)
            except:
                # Ignore missing setGridCrsType method
                pass

            self.grid.setAnnotationDisplay(QgsComposerMapGrid.LongitudeOnly, QgsComposerMapGrid.Top)
            self.grid.setAnnotationDisplay(QgsComposerMapGrid.LatitudeOnly, QgsComposerMapGrid.Right)
            self.grid.setAnnotationDisplay(QgsComposerMapGrid.LongitudeOnly, QgsComposerMapGrid.Bottom)
            self.grid.setAnnotationDisplay(QgsComposerMapGrid.LatitudeOnly, QgsComposerMapGrid.Left)
            if crs != "EPSG:4326":
                # self.grid.setAnnotationDisplay(QgsComposerMapGrid.HideAll, QgsComposerMapGrid.Top)
                # self.grid.setAnnotationDisplay(QgsComposerMapGrid.HideAll, QgsComposerMapGrid.Right)
                self.grid.setAnnotationPrecision(0)

            showInterval = (format != 'MGRS' and format != 'UTM')
            self.dialogui.spinBox_intervalx.setEnabled(showInterval)
            self.dialogui.label_intervalx.setEnabled(showInterval)
            self.dialogui.spinBox_intervaly.setEnabled(showInterval)
            self.dialogui.label_intervaly.setEnabled(showInterval)
            if showInterval:
                # Get interval from composer
                self.dialogui.spinBox_intervalx.blockSignals(True)
                self.dialogui.spinBox_intervalx.setValue(self.mapitem.gridIntervalX())
                self.dialogui.spinBox_intervalx.blockSignals(False)
                self.dialogui.spinBox_intervaly.blockSignals(True)
                self.dialogui.spinBox_intervaly.setValue(self.mapitem.gridIntervalY())
                self.dialogui.spinBox_intervaly.blockSignals(False)

        self.__updateView()

    def __showCartoucheDialog(self):
        self.cartouchedialog.exec_()
        self.cartouchedialog.storeInProject()

    def __intervalXChanged(self, value):
        self.mapitem.setGridIntervalX(value)
        self.__updateView()

    def __intervalYChanged(self, value):
        self.mapitem.setGridIntervalY(value)
        self.__updateView()

    def __titleChanged(self, arg):
        titleItem = self.__composerItem("title", QgsComposerLabel)
        if titleItem:
            titleItem.setText(unicode(self.dialogui.lineEdit_title.text()))
            titleItem.setVisible(not not titleItem.text())
            self.__updateView()

    def __toggleGridAnnotations(self, active):
        self.mapitem.setShowGridAnnotation(active)
        self.__updateView()

    def __toggleLegend(self, active):
        legendItem = self.__composerItem("legend", QgsComposerLegend)
        self.dialogui.button_configureLegend.setEnabled(active)
        if legendItem:
            legendItem.setVisible(active)
            self.__updateView()

    def __configureLegend(self, execDialog = True):
        legendItem = self.__composerItem("legend", QgsComposerLegend)
        if not legendItem:
            return
        model = legendItem.modelV2()

        # Get previously displayed layers
        prevLayers = {}
        for layerNode in model.rootGroup().findLayers():
            index = model.node2index(layerNode)
            prevLayers[layerNode.layerId()] = model.rowCount(index) > 0

        # Build list-widget of layers
        layersList = QTableWidget(0, 2)
        layersList.horizontalHeader().hide()
        layersList.horizontalHeader().setStretchLastSection(True)
        layersList.verticalHeader().hide()
        layerReg = QgsMapLayerRegistry.instance()
        for layerNode in QgsProject.instance().layerTreeRoot().findLayers():
            row = layersList.rowCount()
            layersList.insertRow(row)
            layer = layerReg.mapLayer(layerNode.layerId())
            item = QTableWidgetItem(layer.name())
            item.setData(Qt.UserRole, layerNode.layerId())
            layersList.setItem(row, 0, item)
            combo = QComboBox()
            combo.addItems([self.tr("Hidden"), self.tr("Visible without layer legend"), self.tr("Visible with layer legend")])
            if layerNode.layerId() in prevLayers:
                combo.setCurrentIndex(2 if prevLayers[layerNode.layerId()] == True else 1)
            else:
                combo.setCurrentIndex(0)
            layersList.setCellWidget(row, 1, combo)
        legendDialog = QDialog(self.dialog)
        if execDialog:
            legendDialog.resize(320, 240)
            bbox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
            legendDialog.setWindowTitle(self.tr("Configure legend"))
            legendDialog.setLayout(QVBoxLayout())
            legendDialog.layout().addWidget(QLabel(self.tr("Select layers to display in legend:")))
            legendDialog.layout().addWidget(layersList)
            legendDialog.layout().addWidget(bbox)
            bbox.accepted.connect(legendDialog.accept)
            bbox.rejected.connect(legendDialog.reject)
        if not execDialog or legendDialog.exec_() == QDialog.Accepted:
            # Reset model
            legendItem.setAutoUpdateModel(True)
            legendItem.setAutoUpdateModel(False)
            removeLayers = []
            removeLegends = []
            for i in range(0, layersList.rowCount()):
                layerId = layersList.item(i, 0).data(Qt.UserRole)
                comboIdx = layersList.cellWidget(i, 1).currentIndex()
                if comboIdx == 0:
                    removeLayers.append(layerId)
                elif comboIdx == 1:
                    removeLegends.append(layerId)
            for layerNode in model.rootGroup().findLayers():
                if layerNode.layerId() in removeLayers:
                    index = model.node2index(layerNode)
                    model.removeRow(index.row(), index.parent())
                elif layerNode.layerId() in removeLegends:
                    index = model.node2index(layerNode)
                    if model.rowCount(index) > 0:
                        layerNode.setCustomProperty("legend/node-order", "empty")
                        model.refreshLayerLegend(layerNode)
            legendItem.adjustBoxSize()
            legendItem.update()

    def __toggleScalebar(self, active):
        scaleBarItem = self.__composerItem("scalebar", QgsComposerScaleBar)
        if scaleBarItem:
            scaleBarItem.setVisible(active)
            self.__updateView()

    def __toggleMapCartouche(self, active):
        self.dialogui.button_mapCartouche.setEnabled(active)
        cartoucheItem = self.__composerItem("mapcartouche", QgsComposerItemGroup)
        if cartoucheItem:
            cartoucheItem.setVisibility(active)
        self.__updateView()

    def __changeScale(self):
        if self.fixedSizeMode:
            self.mapitem.setNewScale(1. / self.dialogui.comboBox_scale.scale())
            self.__createRubberBand()
        else:
            self.__generateComposer()

    def __updateView(self):
        self.composerView.composition().update()
        self.dialogui.previewGraphic.update()

    def __reloadComposers(self, removedView=None):
        self.cartouchedialog = None
        self.mapitem = 0
        self.dialogui.comboBox_composers.blockSignals(True)
        prev = self.dialogui.comboBox_composers.currentText()
        self.dialogui.comboBox_composers.clear()
        items = []
        for composer in self.iface.activeComposers():
            if composer != removedView and composer.composerWindow():
                cur = composer.composerWindow().windowTitle()
                items.append((cur, composer))
        items.sort(key=lambda x: x[0])
        for item in items:
            self.dialogui.comboBox_composers.addItem(item[0], item[1])
        # Ensure that changed signal is emitted
        self.dialogui.comboBox_composers.setCurrentIndex(-1)
        self.dialogui.comboBox_composers.blockSignals(False)
        if self.dialogui.comboBox_composers.count() > 0:
            self.__setUiEnabled(True)
            active = self.dialogui.comboBox_composers.findText(prev)
            if active == -1:
              active = 0
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
            self.fixedSizeMode = composerView.composerWindow().windowTitle() != "Custom"
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

        if self.composerView:
            self.composerView.composerViewHide.disconnect(self.__initComposer)
        self.composerView = composerView
        self.composerView.composerViewHide.connect(self.__initComposer)
        # Default to twice the screen resolution
        self.composerView.composition().setPrintResolution(2 * QApplication.desktop().logicalDpiX())
        self.mapitem = maps[0]
        self.__initComposer()

    def __manageLayouts(self):
        PrintLayoutManager(self.iface, self.dialog).exec_()

    def __getCustomExtent(self):
        try:
            xmin = float(self.dialogui.lineedit_xmin.text())
            ymin = float(self.dialogui.lineedit_ymin.text())
            xmax = float(self.dialogui.lineedit_xmax.text())
            ymax = float(self.dialogui.lineedit_ymax.text())
        except:
            # One or more extent inputs empty
            return None

        if xmin > xmax:
            tmp = xmin
            xmin = xmax
            xmax = tmp

        if ymin > ymax:
            tmp = ymin
            ymin = ymax
            ymax = tmp

        return QgsRectangle(xmin, ymin, xmax, ymax)

    def __generateComposer(self):
        scale = 1. / self.dialogui.comboBox_scale.scale()
        extent = self.__getCustomExtent()
        if not extent:
            return
        border = self.dialogui.spinBox_border.value()
        borderdelta = border - self.mapitem.x()

        mapwidth = ((extent.xMaximum() - extent.xMinimum()) / scale * 1000.0)
        mapheight = ((extent.yMaximum() - extent.yMinimum()) / scale * 1000.0)

        self.mapitem.setSceneRect( QRectF(border, border, mapwidth, mapheight ) )
        self.mapitem.setPos(border, border)
        self.mapitem.setNewExtent(extent)
        self.mapitem.setNewScale(scale)
        self.mapitem.updateItem()

        newwidth = 2 * border + mapwidth
        newheight = 2 * border + mapheight

        for item in self.composerView.composition().items():
            if item is not self.mapitem:
                item.moveBy(borderdelta, borderdelta)

        self.composerView.composition().setPaperSize(newwidth, newheight)
        self.dialogui.label_paperSize.setText(self.tr("Paper size: %.2f cm x %.2f cm") % (newwidth / 10., newheight / 10.))

        self.rect = extent.toRectF()
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

        # Ensure output filename has correct extension
        filename = settings.value("/print/lastfile", "")
        if filename:
            filename = os.path.splitext(filename)[0] + "." + self.dialogui.comboBox_fileformat.currentText().lower()
        else:
            filename = QDir.homePath()

        filename = QFileDialog.getSaveFileName(
            self.iface.mainWindow(),
            self.tr("Print Composition"),
            filename,
            format
        )
        if type(filename) == tuple: filename = filename[0]
        if not filename:
            return

        self.printing = True
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.dialogui.previewGraphic.setUpdatesEnabled(False)
        self.dialog.setEnabled(False)

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

        self.dialog.setEnabled(True)
        self.dialogui.previewGraphic.setUpdatesEnabled(True)
        QApplication.restoreOverrideCursor()
        self.printing = False

    def __print(self):
        composer = self.composerView.composerWindow()
        composer.on_mActionPrint_triggered()

    def __setUiEnabled(self, enabled):
        self.dialogui.lineEdit_title.setEnabled(enabled)
        self.dialogui.comboBox_scale.setEnabled(enabled)
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
        composer.setWindowModality(Qt.ApplicationModal)
        composer.showNormal()
        composer.raise_()
