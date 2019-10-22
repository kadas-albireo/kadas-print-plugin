# -*- coding: utf-8 -*-
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    copyright            : (C) 2015 by Sourcepole AG

from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtPrintSupport import *
from qgis.core import *
from qgis.gui import *
import os
import math

from .CartoucheDialog import CartoucheDialog
from .PrintLayoutManager import PrintLayoutManager
from .ui.ui_printdialog import Ui_PrintDialog


class PrintTool(QgsMapTool):

    def __init__(self, iface):
        QgsMapTool.__init__(self, iface.mapCanvas())

        self.iface = iface
        self.layoutManager = QgsProject.instance().layoutManager()
        self.printer = QPrinter()
        self.rubberband = None
        self.oldrubberband = None
        self.resizeTol = 10
        self.resizePoints = []
        self.resizeHandlers = []
        self.resizeMoveOffset = None
        self.fixedSizeMode = True
        self.mapitem = None
        self.printing = False
        self.printLayout = None
        self.rect = None

        self.dialog = QDialog(self.iface.mainWindow())
        self.dialogui = Ui_PrintDialog()
        self.dialogui.setupUi(self.dialog)
        self.exportButton = self.dialogui.buttonBox.addButton(
            self.tr("Export"), QDialogButtonBox.ActionRole)
        self.printButton = self.dialogui.buttonBox.addButton(
            self.tr("Print"), QDialogButtonBox.ActionRole)
        self.advancedButton = self.dialogui.buttonBox.addButton(
            self.tr("Advanced"), QDialogButtonBox.HelpRole)

        proxy = QSortFilterProxyModel(self.dialogui.comboBox_printlayouts)
        proxy.setSourceModel(self.dialogui.comboBox_printlayouts.model())
        self.dialogui.comboBox_printlayouts.model().setParent(proxy)
        self.dialogui.comboBox_printlayouts.setModel(proxy)

        self.dialogui.comboBox_fileformat.addItem(
            "PDF", self.tr("PDF Document (*.pdf);;"))
        self.dialogui.comboBox_fileformat.addItem(
            "JPG", self.tr("JPG Image (*.jpg);;"))
        self.dialogui.comboBox_fileformat.addItem(
            "BMP", self.tr("BMP Image (*.bmp);;"))
        self.dialogui.comboBox_fileformat.addItem(
            "PNG", self.tr("PNG Image (*.png);;"))

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

        QgsProject.instance().layoutManager().layoutAdded.connect(
            lambda view: self.__reloadPrintLayouts())
        QgsProject.instance().layoutManager().layoutRemoved.connect(
            self.__reloadPrintLayouts)
        self.dialogui.comboBox_printlayouts.currentIndexChanged.connect(
            self.__selectPrintLayout)
        self.dialogui.toolButton_layoutManager.clicked.connect(
            self.__manageLayouts)
        self.dialogui.lineEdit_title.textChanged.connect(
            self.__titleChanged)
        self.dialogui.comboBox_scale.scaleChanged.connect(
            self.__changeScale)
        self.dialogui.spinBox_border.valueChanged.connect(
            self.__generatePrintLayout)
        self.dialogui.lineedit_xmin.editingFinished.connect(
            self.__generatePrintLayout)
        self.dialogui.lineedit_xmax.editingFinished.connect(
            self.__generatePrintLayout)
        self.dialogui.lineedit_ymin.editingFinished.connect(
            self.__generatePrintLayout)
        self.dialogui.lineedit_ymax.editingFinished.connect(
            self.__generatePrintLayout)
        self.dialogui.button_mapCartouche.clicked.connect(
            self.__showCartoucheDialog)
        self.dialogui.comboBox_crs.currentIndexChanged.connect(
            self.__setupGrid)
        self.dialogui.checkBox_gridAnnotations.toggled.connect(
            self.__toggleGridAnnotations)
        self.dialogui.checkBox_legend.toggled.connect(self.__toggleLegend)
        self.dialogui.button_configureLegend.clicked.connect(
            lambda: self.__configureLegend())
        self.dialogui.checkBox_scalebar.toggled.connect(self.__toggleScalebar)
        self.dialogui.checkBox_mapCartouche.toggled.connect(
            self.__toggleMapCartouche)
        self.dialogui.spinBox_intervalx.valueChanged.connect(
            self.__intervalXChanged)
        self.dialogui.spinBox_intervaly.valueChanged.connect(
            self.__intervalYChanged)
        self.dialogui.groupBox_grid.setChecked(False)
        self.exportButton.clicked.connect(self.__export)
        self.printButton.clicked.connect(self.__print)
        # self.advancedButton.clicked.connect(self.__advanced)
        self.dialog.finished.connect(lambda: self.setToolEnabled(False))
        self.dialogui.groupBox_grid.toggled.connect(self.__setupGrid)
        self.iface.mapCanvas().mapCanvasRefreshed.connect(self.__updateMap)
        self.iface.mapCanvas().destinationCrsChanged.connect(
            self.__mapUnitsChanged)

        self.__setUiEnabled(False)

    def __resizePreview(self, ev=None):
        try:
            page = self.printLayout.pageCollection()[0]
            self.dialogui.previewGraphic.fitInView(page, Qt.KeepAspectRatio)
        except:
            pass

    def __updateMap(self):
        if self.mapitem and not self.printing:
            self.mapitem.recreateCachedImageInBackground()
            self.mapitem.update()

    def __mapUnitsChanged(self):
        if not self.fixedSizeMode and \
                self.iface.mapCanvas().mapSettings().mapUnits() \
                != QgsUnitTypes.DistanceMeters:
            self.__setUiEnabled(False)
            self.dialogui.label_unitWarning.setVisible(True)
        elif self.dialogui.label_unitWarning.isVisible():
            self.__setUiEnabled(True)
            self.__initPrintLayout()

    def __layoutItem(self, id, classtype):
        try:
            item = self.printLayout.itemById(id) if self.printLayout else None
            if item:
                item.__class__ = classtype
                # This is not a debug leftover, but ensures that the object
                # gets the attributes...
                dir(item)
            return item
        except:
            return None

    def __initPrintLayout(self):
        self.grid = self.mapitem.grid()
        self.cartouchedialog = CartoucheDialog(self.printLayout, self.dialog)
        if not self.fixedSizeMode:
            # Only update extent if it does not intersect
            # with full extent of map
            extent = self.__getCustomExtent()
            if not extent or not self.iface.mapCanvas().fullExtent().contains(
                    extent):
                extent = self.iface.mapCanvas().extent()
                self.dialogui.lineedit_xmin.setText(
                    str(round(extent.xMinimum() + 0.125 * extent.width())))
                self.dialogui.lineedit_xmax.setText(
                    str(round(extent.xMaximum() - 0.125 * extent.width())))
                self.dialogui.lineedit_ymin.setText(
                    str(round(extent.yMinimum() + 0.125 * extent.height())))
                self.dialogui.lineedit_ymax.setText(
                    str(round(extent.yMaximum() - 0.125 * extent.height())))
            self.__generatePrintLayout()
        else:
            extent = self.iface.mapCanvas().extent()
            extentheight = self.mapitem.extent().height() / self.mapitem.extent().width() * extent.width()
            center = extent.center().y()
            extent.setYMinimum(center - extentheight / 2.)
            extent.setYMaximum(center + extentheight / 2.)
            self.mapitem.setExtent(extent)
        wmtsScales = []
        bestScale = self.mapitem.scale()
        # TODO: METHOD wmtsResolutions DOES NOT EXIST ASK SANDRO
        # refRes = 0.0254 / self.printLayout.renderContext().dpi()
        # try:
        #     resolutions = self.iface.mapCanvas().wmtsResolutions()
        # except:
        #     resolutions = []
        # minDist = -1
        # bestScale = 1. / self.mapitem.scale()
        # if resolutions:
        #     minDist = abs(1. / self.mapitem.scale() - refRes / resolutions[0])
        # for resolution in resolutions:
        #     scale = refRes / resolution
        #     if 1. / self.mapitem.scale() < scale:
        #         bestScale = scale
        #     wmtsScales.append(QgsScaleComboBox.toString(scale))
        self.dialogui.comboBox_scale.updateScales(wmtsScales)
        self.dialogui.comboBox_scale.blockSignals(True)
        self.dialogui.comboBox_scale.setScale(bestScale)
        self.dialogui.comboBox_scale.blockSignals(False)
        self.mapitem.recreateCachedImageInBackground()
        self.mapitem.update()
        self.dialogui.previewGraphic.setScene(self.printLayout)
        self.__resizePreview()
        self.__updateView()
        self.__changeScale()

        titleItem = self.__layoutItem("title", QgsLayoutItemLabel)
        if not titleItem:
            self.dialogui.lineEdit_title.setEnabled(False)
        else:
            self.dialogui.lineEdit_title.setText(titleItem.text())
            titleItem.setVisible(not not titleItem.text())
        legendItem = self.__layoutItem("legend", QgsLayoutItemLegend)
        if not legendItem:
            self.dialogui.checkBox_legend.setEnabled(False)
        else:
            self.dialogui.checkBox_legend.setChecked(legendItem.isVisible())
        scaleBarItem = self.__layoutItem("scalebar", QgsLayoutItemScaleBar)
        if not scaleBarItem:
            self.dialogui.checkBox_scalebar.setEnabled(False)
        else:
            self.dialogui.checkBox_scalebar.setChecked(scaleBarItem.isVisible())
        if not self.grid:
            self.dialogui.groupBox_grid.setEnabled(False)
        else:
            self.__setupGrid()
        cartoucheItem = self.__layoutItem(
            "mapcartouche", QgsLayoutItemGroup)
        if not cartoucheItem:
            self.dialogui.checkBox_mapCartouche.setEnabled(False)
        else:
            self.dialogui.checkBox_mapCartouche.setChecked(
                cartoucheItem.isVisible())
        self.dialogui.groupBox_grid.setChecked(
            self.mapitem.grid().enabled())

    def setToolEnabled(self, enabled):
        if enabled:
            self.dialog.show()
            self.__reloadPrintLayouts()
            self.__configureLegend(False)
            self.iface.mapCanvas().setMapTool(self)
        else:
            self.mapitem = None
            self.printLayout = None
            self.dialog.hide()
            self.__clearRubberBand()
            self.iface.mapCanvas().unsetMapTool(self)

    def canvasPressEvent(self, e):
        if not self.rubberband or not self.rect:
            return
        r = self.__canvasRect(self.rect)
        if e.button() == Qt.LeftButton:

            # Check whether to resize
            if not self.fixedSizeMode:
                p1 = r.topLeft()
                p2 = r.bottomRight()
                mup = self.iface.mapCanvas().mapSettings().mapUnitsPerPixel()
                self.resizePoints = [self.rect.topLeft(),
                                     self.rect.bottomRight()]
                self.resizeHandlers = []
                self.resizeMoveOffset = QPointF(0, 0)

                if abs(p1.x() - e.x()) < self.resizeTol:
                    self.resizeHandlers.append(
                        lambda p: self.resizePoints[0].setX(p.x()))
                    self.resizeMoveOffset.setX((e.x() - p1.x()) * mup)
                elif abs(p2.x() - e.x()) < self.resizeTol:
                    self.resizeHandlers.append(
                        lambda p: self.resizePoints[1].setX(p.x()))
                    self.resizeMoveOffset.setX((e.x() - p2.x()) * mup)
                if abs(p1.y() - e.y()) < self.resizeTol:
                    self.resizeHandlers.append(
                        lambda p: self.resizePoints[0].setY(p.y()))
                    self.resizeMoveOffset.setY(-(e.y() - p1.y()) * mup)
                elif abs(p2.y() - e.y()) < self.resizeTol:
                    self.resizeHandlers.append(
                        lambda p: self.resizePoints[1].setY(p.y()))
                    self.resizeMoveOffset.setY(-(e.y() - p2.y()) * mup)

            # Check whether to move
            if not self.resizeHandlers and r.contains(e.pos()):
                self.oldrect = QRectF(self.rect)
                self.oldrubberband = QgsRubberBand(
                    self.iface.mapCanvas(), QgsWkbTypes.PolygonGeometry)
                self.oldrubberband.setToCanvasRectangle(
                    self.__canvasRect(self.oldrect))
                self.oldrubberband.setColor(QColor(127, 127, 255, 31))
                mtp = self.iface.mapCanvas().mapSettings().mapToPixel()
                p = mtp.toMapCoordinates(e.pos())
                self.resizeMoveOffset = QPointF(
                    p.x() - self.rect.x(), p.y() - self.rect.y())

    def canvasMoveEvent(self, e):
        if not self.rect:
            return
        if not self.resizeMoveOffset:
            # Determine cursor
            r = self.__canvasRect(self.rect)
            left = abs(r.left() - e.x()) < self.resizeTol
            right = abs(r.right() - e.x()) < self.resizeTol
            top = abs(r.top() - e.y()) < self.resizeTol
            bottom = abs(r.bottom() - e.y()) < self.resizeTol
            if not self.fixedSizeMode:
                if (bottom and left) or (top and right):
                    self.iface.mapCanvas().setCursor(Qt.SizeFDiagCursor)
                elif (bottom and right) or (top and left):
                    self.iface.mapCanvas().setCursor(Qt.SizeBDiagCursor)
                elif top or bottom:
                    self.iface.mapCanvas().setCursor(Qt.SizeVerCursor)
                elif left or right:
                    self.iface.mapCanvas().setCursor(Qt.SizeHorCursor)
                elif r.contains(e.pos()):
                    self.iface.mapCanvas().setCursor(Qt.OpenHandCursor)
                else:
                    self.iface.mapCanvas().unsetCursor()
            elif r.contains(e.pos()):
                self.iface.mapCanvas().setCursor(Qt.OpenHandCursor)
            else:
                self.iface.mapCanvas().unsetCursor()
        else:
            mtp = self.iface.mapCanvas().mapSettings().mapToPixel()
            p = mtp.toMapCoordinates(e.pos())
            p.setX(p.x() - self.resizeMoveOffset.x())
            p.setY(p.y() - self.resizeMoveOffset.y())

            if not self.resizeHandlers:
                # Move entire rect
                corner = QPointF(self.rect.x(), self.rect.y())
                x = p.x()
                y = p.y()
                snaptol = 10 * self.iface.mapCanvas().mapSettings().mapUnitsPerPixel()
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

                self.rect = QRectF(x, y, self.rect.width(), self.rect.height())
            else:
                # Resize rect
                for handler in self.resizeHandlers:
                    handler(p)
                p1 = self.resizePoints[0]
                p2 = self.resizePoints[1]
                self.rect = QRectF(
                    min(p1.x(), p2.x()),
                    min(p1.y(), p2.y()),
                    abs(p1.x() - p2.x()),
                    abs(p1.y() - p2.y())
                )
            self.dialogui.lineedit_xmin.setText(str(round(self.rect.left())))
            self.dialogui.lineedit_xmax.setText(str(round(self.rect.right())))
            self.dialogui.lineedit_ymin.setText(str(round(self.rect.top())))
            self.dialogui.lineedit_ymax.setText(str(round(self.rect.bottom())))
            self.rubberband.setToCanvasRectangle(self.__canvasRect(self.rect))

    def canvasReleaseEvent(self, e):
        if e.button() == Qt.LeftButton and self.resizeMoveOffset:
            if self.oldrubberband:
                self.iface.mapCanvas().scene().removeItem(self.oldrubberband)
                self.oldrubberband = None
            self.oldrect = None
            self.resizeHandlers = []
            self.resizePoints = []
            self.resizeMoveOffset = None
            self.mapitem.setExtent(QgsRectangle(self.rect))
            if not self.fixedSizeMode:
                self.__generatePrintLayout()

    def __setupGrid(self):
        if not self.mapitem:
            return
        if not self.dialogui.groupBox_grid.isChecked():
            self.mapitem.grid().setEnabled(False)
        else:
            crs, format = self.dialogui.comboBox_crs.itemData(
                self.dialogui.comboBox_crs.currentIndex()).split(",")
            self.mapitem.grid().setEnabled(True)
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

            self.grid.setAnnotationDisplay(
                QgsLayoutItemMapGrid.LongitudeOnly, QgsLayoutItemMapGrid.Top)
            self.grid.setAnnotationDisplay(
                QgsLayoutItemMapGrid.LatitudeOnly, QgsLayoutItemMapGrid.Right)
            self.grid.setAnnotationDisplay(
                QgsLayoutItemMapGrid.LongitudeOnly,
                QgsLayoutItemMapGrid.Bottom)
            self.grid.setAnnotationDisplay(
                QgsLayoutItemMapGrid.LatitudeOnly, QgsLayoutItemMapGrid.Left)
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
                self.dialogui.spinBox_intervalx.setValue(
                    self.mapitem.grid().intervalX())
                self.dialogui.spinBox_intervalx.blockSignals(False)
                self.dialogui.spinBox_intervaly.blockSignals(True)
                self.dialogui.spinBox_intervaly.setValue(
                    self.mapitem.grid().intervalY())
                self.dialogui.spinBox_intervaly.blockSignals(False)

        self.__updateView()

    def __showCartoucheDialog(self):
        self.cartouchedialog.exec_()
        self.cartouchedialog.storeInProject()

    def __intervalXChanged(self, value):
        self.mapitem.grid().setIntervalX(value)
        self.__updateView()

    def __intervalYChanged(self, value):
        self.mapitem.grid().setIntervalY(value)
        self.__updateView()

    def __titleChanged(self, arg):
        titleItem = self.__layoutItem("title", QgsLayoutItemLabel)
        if titleItem:
            titleItem.setText(unicode(self.dialogui.lineEdit_title.text()))
            titleItem.setVisible(not not titleItem.text())
            self.__updateView()

    def __toggleGridAnnotations(self, active):
        self.mapitem.grid().setAnnotationEnabled(active)
        self.__updateView()

    def __toggleLegend(self, active):
        legendItem = self.__layoutItem("legend", QgsLayoutItemLegend)
        self.dialogui.button_configureLegend.setEnabled(active)
        if legendItem:
            legendItem.setVisible(active)
            self.__updateView()

    def __configureLegend(self, execDialog=True):
        legendItem = self.__layoutItem("legend", QgsLayoutItemLegend)
        if not legendItem:
            return
        model = legendItem.model()

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
        qgsProject = QgsProject.instance()
        for layerNode in QgsProject.instance().layerTreeRoot().findLayers():
            row = layersList.rowCount()
            layersList.insertRow(row)
            layer = qgsProject.mapLayer(layerNode.layerId())
            item = QTableWidgetItem(layer.name())
            item.setData(Qt.UserRole, layerNode.layerId())
            layersList.setItem(row, 0, item)
            combo = QComboBox()
            combo.addItems([
                self.tr("Hidden"),
                self.tr("Visible without layer legend"),
                self.tr("Visible with layer legend")])
            if layerNode.layerId() in prevLayers:
                combo.setCurrentIndex(
                    2 if prevLayers[layerNode.layerId()] is True else 1)
            else:
                combo.setCurrentIndex(0)
            layersList.setCellWidget(row, 1, combo)
        legendDialog = QDialog(self.dialog)
        if execDialog:
            legendDialog.resize(320, 240)
            bbox = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            legendDialog.setWindowTitle(self.tr("Configure legend"))
            legendDialog.setLayout(QVBoxLayout())
            legendDialog.layout().addWidget(QLabel(
                self.tr("Select layers to display in legend:")))
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
                        layerNode.setCustomProperty(
                            "legend/node-order", "empty")
                        model.refreshLayerLegend(layerNode)
            legendItem.adjustBoxSize()
            legendItem.updateLegend()

    def __toggleScalebar(self, active):
        scaleBarItem = self.__layoutItem("scalebar", QgsLayoutItemScaleBar)
        if scaleBarItem:
            scaleBarItem.setVisible(active)
            self.__updateView()

    def __toggleMapCartouche(self, active):
        self.dialogui.button_mapCartouche.setEnabled(active)
        cartoucheItem = self.__layoutItem("mapcartouche", QgsLayoutItemGroup)
        if cartoucheItem:
            cartoucheItem.setVisibility(active)
        self.__updateView()

    def __changeScale(self):
        if self.fixedSizeMode:
            self.mapitem.setScale(self.dialogui.comboBox_scale.scale())
            self.__createRubberBand()
        else:
            self.__generatePrintLayout()

    def __updateView(self):
        self.printLayout.update()
        self.dialogui.previewGraphic.update()

    def __reloadPrintLayouts(self, removedLayout=None):
        # Only reload if dialog is visible
        if not self.dialog.isVisible():
            return

        self.cartouchedialog = None
        self.mapitem = None
        self.dialogui.comboBox_printlayouts.blockSignals(True)
        prev = self.dialogui.comboBox_printlayouts.currentText()
        if not prev and self.layoutManager.printLayouts():
            prev = self.layoutManager.printLayouts()[0].name()
        self.dialogui.comboBox_printlayouts.clear()
        items = []
        for layout in self.layoutManager.printLayouts():
            if layout != removedLayout:
                cur = layout.name()
                items.append((cur, layout))
        items.sort(key=lambda x: x[0])
        for item in items:
            self.dialogui.comboBox_printlayouts.addItem(item[0], item[1])
        # Ensure that changed signal is emitted
        self.dialogui.comboBox_printlayouts.setCurrentIndex(-1)
        self.dialogui.comboBox_printlayouts.blockSignals(False)
        if self.dialogui.comboBox_printlayouts.count() > 0:
            self.__setUiEnabled(True)
            active = self.dialogui.comboBox_printlayouts.findText(prev)
            if active == -1:
                active = 0
            self.dialogui.comboBox_printlayouts.setCurrentIndex(active)
        else:
            self.__setUiEnabled(False)

    def __selectPrintLayout(self):
        self.__clearRubberBand()
        self.mapitem = None
        self.dialogui.previewGraphic.setScene(None)
        try:
            activeIndex = self.dialogui.comboBox_printlayouts.currentIndex()
            layout = self.dialogui.comboBox_printlayouts.itemData(activeIndex)
            layout.__class__ = QgsPrintLayout
            self.fixedSizeMode = layout.name() != "Custom"
        except Exception as e:
            self.__setUiEnabled(False)
            return

        if not self.fixedSizeMode and self.iface.mapCanvas().mapSettings().mapUnits() != QgsUnitTypes.DistanceMeters:
            self.__setUiEnabled(False)
            self.dialogui.label_unitWarning.setVisible(True)
            return

        referenceMap = layout.referenceMap()

        if not referenceMap:
            QMessageBox.warning(
                self.iface.mainWindow(),
                self.tr("Invalid layout"),
                self.tr("The layout must have exactly one map item."))
            self.__setUiEnabled(False)
            return

        self.__setUiEnabled(True)

        self.printLayout = layout
        # Default to twice the screen dpi
        self.printLayout.renderContext().setDpi(2 * QApplication.desktop().logicalDpiX())
        self.mapitem = referenceMap
        self.__initPrintLayout()

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

    def __generatePrintLayout(self):
        scale = self.dialogui.comboBox_scale.scale()
        extent = self.__getCustomExtent()
        if not extent:
            return
        border = self.dialogui.spinBox_border.value()
        borderdelta = border - self.mapitem.x()

        mapwidth = ((extent.xMaximum() - extent.xMinimum()) / scale * 1000.0)
        mapheight = ((extent.yMaximum() - extent.yMinimum()) / scale * 1000.0)

        self.mapitem.attemptSetSceneRect(QRectF(border, border, mapwidth, mapheight))
        # self.mapitem.setPos(border, border)
        self.mapitem.attemptMoveBy(border, border)
        self.mapitem.setExtent(extent)
        self.mapitem.setScale(scale)
        self.mapitem.updateItem()

        newwidth = 2 * border + mapwidth
        newheight = 2 * border + mapheight

        for item in self.printLayout.items():
            if item is not self.mapitem:
                item.attemptMoveBy(borderdelta, borderdelta)

        pageCollection = self.printLayout.pageCollection()
        page = pageCollection.page(0)
        page.setPageSize(QgsLayoutSize(newwidth, newheight))

        self.dialogui.label_paperSize.setText(
            self.tr("Paper size: %.2f cm x %.2f cm") % (
                newwidth / 10., newheight / 10.))

        self.rect = extent.toRectF()
        self.__createRubberBand()
        self.__resizePreview()
        self.__updateView()

    def __createRubberBand(self):
        self.__clearRubberBand()
        extent = self.mapitem.extent()
        center = extent.center()
        corner = QPointF(
            center.x() - 0.5 * extent.width(),
            center.y() - 0.5 * extent.height())
        self.rect = QRectF(
            corner.x(), corner.y(), extent.width(), extent.height())

        self.rubberband = QgsRubberBand(
            self.iface.mapCanvas(), QgsWkbTypes.PolygonGeometry)
        self.rubberband.setToCanvasRectangle(self.__canvasRect(self.rect))
        self.rubberband.setColor(QColor(127, 127, 255, 127))

    def __clearRubberBand(self):
        if self.rubberband:
            self.iface.mapCanvas().scene().removeItem(self.rubberband)
        if self.oldrubberband:
            self.iface.mapCanvas().scene().removeItem(self.oldrubberband)
        self.rubberband = None
        self.oldrubberband = None

    def __canvasRect(self, rect):
        mtp = self.iface.mapCanvas().mapSettings().mapToPixel()
        p1 = mtp.transform(QgsPointXY(rect.left(), rect.top()))
        p2 = mtp.transform(QgsPointXY(rect.right(), rect.bottom()))
        try:
            return QRect(int(p1.x()), int(p1.y()),
                         int(p2.x() - p1.x()), int(p2.y() - p1.y()))
        except:
            return QRect(0, 0, 0, 0)

    def __export(self):
        settings = QSettings()
        format = self.dialogui.comboBox_fileformat.itemData(
            self.dialogui.comboBox_fileformat.currentIndex())

        # Ensure output filename has correct extension
        filename = settings.value("/print/lastfile", "")
        if filename:
            filename = os.path.splitext(filename)[0] + "." + self.dialogui.comboBox_fileformat.currentText().lower()
        else:
            filename = QDir.homePath()

        filename = QFileDialog.getSaveFileName(
            self.iface.mainWindow(),
            self.tr("Print Layout"),
            filename,
            format)

        if type(filename) == tuple:
            filename = filename[0]
        if not filename:
            return

        self.printing = True
        self.dialogui.previewGraphic.setUpdatesEnabled(False)
        self.dialog.setEnabled(False)

        # Ensure output filename has correct extension
        filename = os.path.splitext(filename)[
            0] + "." + self.dialogui.comboBox_fileformat.currentText().lower()

        settings.setValue("/print/lastfile", filename)

        success = False
        exporter = QgsLayoutExporter(self.printLayout)
        if filename[-3:].lower() == u"pdf":
            success = exporter.exportToPdf(
                filename, QgsLayoutExporter.PdfExportSettings())
        else:
            success = exporter.exportToImage(
                filename, QgsLayoutExporter.ImageExportSettings())
        if success != QgsLayoutExporter.Success:
            self.iface.messageBar().clearWidgets()
            QMessageBox.warning(
                self.iface.mainWindow(),
                self.tr("Print Failed"),
                self.tr("Failed to print the layout."))

        self.dialog.setEnabled(True)
        self.dialogui.previewGraphic.setUpdatesEnabled(True)
        self.printing = False

    def __print(self):
        if not QPrinterInfo.availablePrinterNames():
            QMessageBox.warning(
                self.dialog,
                self.tr("No Printers"),
                self.tr("No printers were found."))
        else:
            exporter = QgsLayoutExporter(self.printLayout)
            printdialog = QPrintDialog(self.printer)

            if printdialog.exec_() != QDialog.Accepted:
                return

            success = exporter.print(
                self.printer, QgsLayoutExporter.PrintExportSettings())
            if success != 0:
                QMessageBox.warning(
                    self.iface.mainWindow(),
                    self.tr("Print Failed"),
                    self.tr("Failed to print the layout."))

    def __setUiEnabled(self, enabled):
        self.dialogui.lineEdit_title.setEnabled(enabled)
        self.dialogui.comboBox_scale.setEnabled(enabled)
        self.dialogui.button_mapCartouche.setEnabled(
            self.dialogui.checkBox_mapCartouche.isChecked())
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

    # def __advanced(self):
    #     self.iface.showComposer(self.printLayout)
