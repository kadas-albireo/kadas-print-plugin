# -*- coding: utf-8 -*-
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    copyright            : (C) 2014-2015 by Sandro Mani / Sourcepole AG
#    email                : smani@sourcepole.ch

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import os

from PrintTool import PrintTool
import resources_rc


class PrintPlugin(QObject):
    def __init__(self, iface):
        QObject.__init__(self)

        self.iface = iface
        self.pluginDir = os.path.dirname(__file__)
        self.tool = PrintTool(self.iface)
        self.toolAction = None

        # Localize
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.pluginDir, 'i18n', 'print_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)
            QCoreApplication.installTranslator(self.translator)

    def initGui(self):
        try:
            printAction = self.iface.findAction("mActionPrint")
        except:
            printAction = None
        if printAction:
            printAction.setCheckable(True)
            printAction.triggered.connect(self.__toggleTool)
            self.tool.setAction(printAction)
        else:
            self.toolButton = QToolButton(self.iface.mapNavToolToolBar())
            self.toolButton.setIcon(QIcon(":/plugins/print/icons/icon.png"))
            self.toolButton.setText(self.tr(" Print"))
            self.toolButton.setToolTip(self.tr(" Print"))
            self.toolButton.setCheckable(True)
            self.toolButton.setObjectName("vbsprintaction")
            self.toolAction = self.iface.pluginToolBar().addWidget(self.toolButton)
            self.tool.setButton(self.toolButton)
            self.toolButton.toggled.connect(self.__toggleTool)

    def unload(self):
        self.tool.setToolEnabled(False)
        self.tool = None
        if self.toolAction:
            self.iface.pluginToolBar().removeAction(self.toolAction)

    def __toggleTool(self, active):
        self.tool.setToolEnabled(active)
