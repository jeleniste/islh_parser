# -*- coding: utf-8 -*-
"""
/***************************************************************************
 islhParser
                                 A QGIS plugin
 načte a zobrazí formát ISLH
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2018-11-27
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Jan Michálek (Je;)
        email                : godzilalalala@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QAction, QMessageBox, QFileDialog, QInputDialog\
        , QDialog
# Initialize Qt resources from file resources.py
from .resources import *

# Import the code for the DockWidget
from .islh_parser_dockwidget import islhParserDockWidget
from .hk_dockwidget import hkDisplayDockWidget
#import os.path
import os

from lxml import etree
#import simplejson as json
import json
##from osgeo import ogr
from qgis.core import QgsFeatureRequest, QgsGeometry, QgsProject\
        , QgsCoordinateReferenceSystem, QgsField\
        , QgsFeature, QgsPoint, QgsProject, QgsVectorLayer\
        , QgsSpatialIndex

from . import ciselniky

from . import islh_geom #prevod geometrie do qgs


class islhParser:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'islhParser_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&ISLH parser')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'islhParser')
        self.toolbar.setObjectName(u'islhParser')

        #print "** INITIALIZING islhParser"

        self.pluginIsActive = False
        self.dockwidget = None
        self.hk_widget = None



    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('islhParser', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/islh_parser/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'ISLH parser'),
            callback=self.run,
            parent=self.iface.mainWindow())

    #--------------------------------------------------------------------------

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        #print "** CLOSING islhParser"

        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:

        self.dockwidget = None

        self.pluginIsActive = False

        del(self.psk_layer)
        del(self.klo_layer)
        del(self.kto_layer)
        del(self.kpo_layer)
        del(self.kbo_layer)
        del(self.bzl_layer)
        del(self.jp_layer)
        del(self.op_layer)

        del(self.doc)
        del(self.root)

        self = None


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        #print "** UNLOAD islhParser"

        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&ISLH parser'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

        #smaze fci znacka
        #del islh_parser.znacka

    #--------------------------------------------------------------------------


    #widget functions
    #--------------------------------------------------------------------------

    def select_input_xml(self):
        filename, _ = QFileDialog.getOpenFileName(self.dockwidget, "Select ISLH XML file ","", '*.xml')
        self.dockwidget.input_file.setText(filename)

    def read_islh(self):

        os.chdir(self.plugin_dir) #musim do plugin diru, abysem nacet svg

        if not self.dockwidget.input_file.text():
            QMessageBox.critical(QDialog()
                    ,u"Missing file",u"Není vybrán žádný soubor")
        else:
            #self.f = open(self.dockwidget.input_file.text(), 'r', encoding='windows-1250')
            try:
                #nachroustam xml
                self.dockwidget.output_working_on.setText(u"načítám XML")
                self.load_xml()

            except:
                QMessageBox.critical(QDialog()
                        ,u"vadný soubor",u"soubor se nepodařilo načíst")

            self.dockwidget.output_working_on.setText(u"Začínám tvořit grafiku")

            self.add_layers()

            self.dockwidget.output_working_on.setText(u"přidávám vrstvy do mapové kompozice")

            self.dockwidget.progressBar.setRange(0,8)
            self.dockwidget.progressBar.setValue(0)

            self.layerTreeRoot = QgsProject.instance().layerTreeRoot()
            self.por_mapa_group = self.layerTreeRoot.insertGroup(0, u'Porostní mapa')
            self.bzl_jp_op_mapa_group = self.layerTreeRoot.insertGroup(1, u'BZL, JP, OP')

            #self.iface.mapCanvas().setRenderFlag(False)


            if hasattr(self, 'psk_layer'):
                QgsProject.instance().addMapLayer(self.psk_layer, False)
                self.psk_layer.loadNamedStyle('styles/por_mapa.qml')
                self.por_mapa_group.insertLayer(0, self.psk_layer)

            self.dockwidget.progressBar.setValue(1)

            if hasattr(self, 'bzl_layer'):
                QgsProject.instance().addMapLayer(self.bzl_layer, False)
                self.bzl_jp_op_mapa_group.insertLayer(0, self.bzl_layer)

            self.dockwidget.progressBar.setValue(2)

            if hasattr(self, 'jp_layer'):
                QgsProject.instance().addMapLayer(self.jp_layer, False)
                self.bzl_jp_op_mapa_group.insertLayer(0, self.jp_layer)

            self.dockwidget.progressBar.setValue(3)

            if hasattr(self, 'op_layer'):
                QgsProject.instance().addMapLayer(self.op_layer, False)
                self.bzl_jp_op_mapa_group.insertLayer(0, self.op_layer)

            self.dockwidget.progressBar.setValue(4)

            if hasattr(self, 'kpo_layer'):
                QgsProject.instance().addMapLayer(self.kpo_layer, False)
                self.kpo_layer.loadNamedStyle('styles/por_mapa_kpo.qml')
                self.por_mapa_group.insertLayer(0, self.kpo_layer)

            self.dockwidget.progressBar.setValue(5)

            if hasattr(self, 'klo_layer'):
                QgsProject.instance().addMapLayer(self.klo_layer, False)
                self.klo_layer.loadNamedStyle('styles/porostni_mapa_linie.qml')
                self.por_mapa_group.insertLayer(0, self.klo_layer)

            self.dockwidget.progressBar.setValue(6)

            if hasattr(self, 'kbo_layer'):
                QgsProject.instance().addMapLayer(self.kbo_layer, False)
                self.kbo_layer.loadNamedStyle('styles/styly_body.qml')
                self.por_mapa_group.insertLayer(0, self.kbo_layer)

            self.dockwidget.progressBar.setValue(7)

            if hasattr(self, 'kto_layer'):
                QgsProject.instance().addMapLayer(self.kto_layer, False)
                self.kto_layer.loadNamedStyle('styles/styly_txt.qml')
                self.por_mapa_group.insertLayer(0, self.kto_layer)

            self.dockwidget.progressBar.setValue(8)

            #self.bzl_jp_op_mapa_group.setVisible(Qt.Unchecked)
            self.bzl_jp_op_mapa_group.setItemVisibilityChecked(False)
            #self.por_mapa_group.setVisible(Qt.Unchecked)

            lhc_list = [self.lhc.get('LHC_KOD')]
            self.dockwidget.input_lhc.clear()
            self.dockwidget.input_lhc.addItems(lhc_list)

            #nastavit komba na zacatek
            self.select_lhc()
            self.select_odd()
            self.select_dil()
            self.select_por()
            self.select_psk()
            self.iface.setActiveLayer(self.psk_layer)

            #self.iface.mapCanvas().zoomScale(5000)
            #self.por_mapa_group.setVisible(Qt.Checked)

    def add_layers(self):
        self.dockwidget.output_working_on.setText(u"Začátek migrace geometrie")
        psk_mustr = self.root.find('LHC/ODD/DIL/POR/PSK')
        bzl_mustr = self.root.find('LHC/ODD/DIL/POR/BZL')
        jp_mustr = self.root.find('LHC/ODD/DIL/POR/JP')
        op_mustr = self.root.find('LHC/ODD/DIL/POR/OP')

        self.dockwidget.output_working_on.setText(u"Vytvářím vrstvy JPRL")


        if psk_mustr is not None:
            self.psk_layer = islh_geom.createLayer([psk_mustr], 'PSK',['lhc_kod','odd','dil','por','etz'])

        if bzl_mustr is not None:
            self.bzl_layer = islh_geom.createLayer([bzl_mustr], 'BZL',['lhc_kod','odd','dil','por'])

        if jp_mustr is not None:
            self.jp_layer = islh_geom.createLayer([jp_mustr], 'JP',['lhc_kod','odd','dil','por'])

        if op_mustr is not None:
            self.op_layer = islh_geom.createLayer([op_mustr], 'OP',['lhc_kod','odd','dil','por'])

        self.dockwidget.output_working_on.setText(u"Generuji vrstvy JPRL")

        featureCount = len(self.root.xpath('LHC/ODD/DIL/POR'))
        pbar = self.dockwidget.progressBar
        pbar.setRange(0, featureCount)
        progres = iter(range(0, featureCount + 1))
        pbar.setValue(next(progres))

        for lhc in self.root.xpath('LHC'):
            lhc_kod = lhc.get('LHC_KOD')
            for odd in lhc.xpath('ODD'):
                odd_kod = odd.get('ODD')
                for dil in odd.xpath('DIL'):
                    dil_kod = dil.get('DIL')
                    for por in dil.xpath('POR'):
                        por_kod = por.get('POR')
                        extra_attrs = {
                                'lhc_kod':lhc_kod
                                , 'odd':odd_kod
                                , 'dil':dil_kod
                                , 'por':por_kod}

                        bzl_dta = por.xpath('BZL')
                        jp_dta = por.xpath('JP')
                        op_dta = por.xpath('OP')

                        if bzl_dta:
                            islh_geom.populateLayer(self.bzl_layer, bzl_dta, extra_attrs)

                        if jp_dta:
                            islh_geom.populateLayer(self.jp_layer, jp_dta, extra_attrs)

                        if op_dta:
                            islh_geom.populateLayer(self.op_layer, op_dta, extra_attrs)

                        for psk in por.xpath('PSK'):
                            #etz = \
                            #json.dumps([dict(etz.attrib) for etz in psk.xpath('ETZ')])

                            #pridane dreviny pro Oldu Cizka
                            etz = \
                            json.dumps([
                                (lambda x,y: dict(x, **y))(dict(etz.attrib),
                                    {'DRV':[dict(drv.attrib) for drv in
                                        etz.xpath('DRV')]}) for etz in psk.xpath('ETZ')
                                ])
                            
                            extra_attrs = {
                                    'lhc_kod':lhc_kod
                                    , 'odd':odd_kod
                                    , 'dil':dil_kod
                                    , 'por':por_kod
                                    , 'etz':etz}
                                    
                            islh_geom.populateLayer(self.psk_layer, [psk], extra_attrs)

                        pbar.setValue(next(progres))

        self.dockwidget.output_working_on.setText(u"Vytvářím karto vrstvy")

        self.klo_layer = islh_geom.createLayer([self.root.find('LHC/KLO')], 'klo')
        self.kbo_layer = islh_geom.createLayer([self.root.find('LHC/KBO')], 'kbo')
        self.kpo_layer = islh_geom.createLayer([self.root.find('LHC/KPO')], 'kpo')
        self.kto_layer = islh_geom.createLayer([self.root.find('LHC/KTO')], 'kto')

        self.dockwidget.output_working_on.setText(u"Nahrávám data do karto vrstev")
        self.dockwidget.output_working_on.setText(u"Nahrávám data do vrstvy KLO")
        islh_geom.populateLayer(self.klo_layer, self.root.xpath('LHC/KLO'), {}, self.dockwidget.progressBar)
        self.dockwidget.output_working_on.setText(u"Nahrávám data do vrstvy KBO")
        islh_geom.populateLayer(self.kbo_layer, self.root.xpath('LHC/KBO'), {}, self.dockwidget.progressBar)
        self.dockwidget.output_working_on.setText(u"Nahrávám data do vrstvy KPO")
        islh_geom.populateLayer(self.kpo_layer, self.root.xpath('LHC/KPO'), {}, self.dockwidget.progressBar)
        self.dockwidget.output_working_on.setText(u"Nahrávám data do vrstvy KTO")
        islh_geom.populateLayer(self.kto_layer, self.root.xpath('LHC/KTO'), {}, self.dockwidget.progressBar)

        if 'PSK_ZNACKA' not in [f.name() for f in self.psk_layer.fields()]:
            self.psk_layer.addExpressionField('znacka(etz)', QgsField('PSK_ZNACKA',QVariant.Int))


        self.dockwidget.output_working_on.setText(u"Hotovo")







    def select_lhc(self):
        self.dockwidget.input_odd.clear()
        self.dockwidget.input_dil.clear()
        self.dockwidget.input_por.clear()
        self.dockwidget.input_psk.clear()

        self.dockwidget.input_odd.addItems(
                [ odd.get('ODD') for odd in self.lhc.xpath('ODD')]
                )

    def select_odd(self):
        self.odd = self.lhc.find("ODD[@ODD='%s']"%self.dockwidget.input_odd.currentText())

        self.dockwidget.input_dil.clear()
        self.dockwidget.input_por.clear()
        self.dockwidget.input_psk.clear()
        self.dockwidget.input_dil.addItems(
                [ dil.get('DIL') for dil in self.odd.xpath('DIL')]
                )

        self.jprl = (
                self.lhc.get('LHC_KOD')
                , self.odd.get('ODD'))

        #zrus vybrane graficky
        self.psk_layer.selectByIds([])

        #vyber
        request = QgsFeatureRequest().setFilterExpression( 
                "lhc_kod = '%s' AND odd = '%s'"%
                self.jprl)

        it = self.psk_layer.getFeatures( request )
        self.psk_layer.selectByIds([f.id() for f in it])

        box = self.psk_layer.boundingBoxOfSelected()
        self.iface.mapCanvas().setExtent(box)
        self.iface.mapCanvas().refresh()

    def select_dil(self):
        self.dil = self.odd.find("DIL[@DIL='%s']"%self.dockwidget.input_dil.currentText())

        self.dockwidget.input_por.clear()
        self.dockwidget.input_psk.clear()
        self.dockwidget.input_por.addItems(
                [ por.get('POR') for por in self.dil.xpath('POR')]
                )


        self.jprl = (
                self.lhc.get('LHC_KOD')
                , self.odd.get('ODD')
                , self.dil.get('DIL'))

        #zrus vybrane graficky
        self.psk_layer.selectByIds([])

        #vyber
        request = QgsFeatureRequest().setFilterExpression( 
                "lhc_kod = '%s' AND odd = '%s' AND dil ='%s'"%
                self.jprl)

        it = self.psk_layer.getFeatures( request )
        self.psk_layer.selectByIds([f.id() for f in it])

        box = self.psk_layer.boundingBoxOfSelected()
        self.iface.mapCanvas().setExtent(box)
        self.iface.mapCanvas().refresh()

    def select_por(self):
        self.por = self.dil.find("POR[@POR='%s']"%self.dockwidget.input_por.currentText())

        self.dockwidget.input_psk.clear()
        self.dockwidget.input_psk.addItems(
                [ psk.get('PSK') for psk in self.por.xpath('PSK')]
                )


        self.jprl = (
                self.lhc.get('LHC_KOD')
                , self.odd.get('ODD')
                , self.dil.get('DIL')
                , self.por.get('POR'))

        #zrus vybrane graficky
        self.psk_layer.selectByIds([])

        #vyber
        request = QgsFeatureRequest().setFilterExpression( 
                "lhc_kod = '%s' AND odd = '%s' AND dil ='%s' AND por = '%s'"%
                self.jprl)

        it = self.psk_layer.getFeatures( request )
        self.psk_layer.selectByIds([f.id() for f in it])

        box = self.psk_layer.boundingBoxOfSelected()
        self.iface.mapCanvas().setExtent(box)
        self.iface.mapCanvas().refresh()


    def select_psk(self):

        self.psk = self.por.find("PSK[@PSK='%s']"%self.dockwidget.input_psk.currentText())

        self.jprl = (
                self.lhc.get('LHC_KOD')
                , self.odd.get('ODD')
                , self.dil.get('DIL')
                , self.por.get('POR')
                , self.psk.get('PSK'))

        #zrus vybrane graficky
        self.psk_layer.selectByIds([])

        #vyber
        request = QgsFeatureRequest().setFilterExpression( 
                "lhc_kod = '%s' AND odd = '%s' AND dil ='%s' AND por = '%s' AND psk = '%s'"%
                self.jprl)

        it = self.psk_layer.getFeatures( request )
        self.psk_layer.selectByIds([f.id() for f in it])

        box = self.psk_layer.boundingBoxOfSelected()
        self.iface.mapCanvas().setExtent(box)
        self.iface.mapCanvas().refresh()

    def show_hk(self):
        #nejdriv zjistim, jestli je vybrany nejaky prvek graficky
        #pak musim u vyberu pomoci roletek dat odselektovani vseho

        if len(self.psk_layer.selectedFeatures()) == 0 and len(self.jprl) < 5:
            QMessageBox.critical(QDialog()
                    ,u"Chyba výběru",u"Není vybrána žádná porostní skupina")

            return(None)

        if len(self.psk_layer.selectedFeatures()) > 0: #musi bejt prave jeden
            #kdyz je jich vic, vem prvni
            selected_psk = self.psk_layer.selectedFeatures()[0]
            self.jprl = (selected_psk['lhc_kod']
                    , selected_psk['odd']
                    , selected_psk['dil']
                    , selected_psk['por']
                    , selected_psk['psk'])

            #nastavim comba
            index = self.dockwidget.input_lhc.findText(selected_psk['lhc_kod'])
            if index >= 0:
                self.dockwidget.input_lhc.setCurrentIndex(index)

            self.select_lhc()

            index = self.dockwidget.input_odd.findText(selected_psk['odd'])
            if index >= 0:
                self.dockwidget.input_odd.setCurrentIndex(index)

            self.select_odd()

            index = self.dockwidget.input_dil.findText(selected_psk['dil'])
            if index >= 0:
                self.dockwidget.input_dil.setCurrentIndex(index)

            self.select_dil()

            index = self.dockwidget.input_por.findText(selected_psk['por'])
            if index >= 0:
                self.dockwidget.input_por.setCurrentIndex(index)

            self.select_por()

            index = self.dockwidget.input_psk.findText(selected_psk['psk'])
            if index >= 0:
                self.dockwidget.input_psk.setCurrentIndex(index)

            self.select_psk()

            #self.psk_layer.selectByIds([])



        if self.hk_widget == None:
            self.hk_widget = hkDisplayDockWidget()

        self.iface.addDockWidget(Qt.TopDockWidgetArea, self.hk_widget)

        self.result = self.transform(self.root
                , ODD="'%s'"%self.jprl[1]
                , DIL="'%s'"%self.jprl[2]
                , POR="'%s'"%self.jprl[3]
                , PSK="'%s'"%self.jprl[4])

        self.hk_widget.webView.setHtml(
                etree.tostring(self.result, encoding = 'unicode')
                )

        self.hk_widget.show()



    

    #--------------------------------------------------------------------------
    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True

            #print "** STARTING islhParser"

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget == None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = islhParserDockWidget()

            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            # show the dockwidget
            # TODO: fix to allow choice of dock location
            self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dockwidget)
            self.dockwidget.show()


            #buttons actions
            self.dockwidget.input_file.clear()
            self.dockwidget.input_file_button.clicked.connect(self.select_input_xml)

            self.dockwidget.input_read.clicked.connect(self.read_islh)

            self.dockwidget.input_lhc.activated.connect(self.select_lhc)
            self.dockwidget.input_odd.activated.connect(self.select_odd)
            self.dockwidget.input_dil.activated.connect(self.select_dil)
            self.dockwidget.input_por.activated.connect(self.select_por)
            self.dockwidget.input_psk.activated.connect(self.select_psk)


            self.dockwidget.input_hk_button.clicked.connect(self.show_hk)

            #load xslt stuff

            self.ns = etree.FunctionNamespace("http://ciselniky")
            self.ns.prefix = "cis"
            self.ns['lesni_oblast'] = ciselniky.lesni_oblast
            self.ns['slt'] = ciselniky.slt
            self.ns['katuze'] = ciselniky.katuze
            self.ns['lvs'] = ciselniky.lvs
            self.ns['zvl_statut'] = ciselniky.zvl_statut

            self.xslt_root = etree.XML(open('%s/xslt/hk.xsl'%self.plugin_dir,'r').read())
            self.transform = etree.XSLT(self.xslt_root)

            #nastavim barvu na neco, co neni v por mape
            self.iface.mapCanvas().setSelectionColor(QColor('#f40'))

            from . import karto_fce


    #----------------------------------------------------
    #plugin logic
    def load_xml(self):
        """:param f: file with islh xml data"""
        #self.doc = etree.parse(self.f)
        self.doc = etree.parse(self.dockwidget.input_file.text())
        self.root = self.doc.getroot()
        self.lhc = self.root.find("./LHC")

    def xx_populate_layer(self, PATH, layer):
        """return layer with psk as geoJSON"""

        layer_data = self.lhc.xpath(PATH)

        if not layer_data:
            return(None)

        featureCount = len(layer_data)
        self.dockwidget.progressBar.setRange(0, featureCount)
        self.progres = iter(range(0, featureCount))

        pr = layer.dataProvider()

        attnames = [k for k in layer_data[0].attrib.keys()]

        tag = layer_data[0].tag

        if tag in ['PSK', 'BZL', 'JP', 'OP']:
            attnames = ['lhc_kod','odd','dil','por'] + attnames
            
        if tag == 'PSK':
            attnames.append('etz')

        pr.addAttributes(
            [QgsField(k
                , QVariant.String
                ) for k in attnames]
            )
                

                
        layer.updateFields()

        geom_tag = {
                'PSK':'PSK_OBRAZ'
                , 'BZL':'BZL_OBRAZ'
                , 'JP':'JP_OBRAZ'
                , 'OP':'OP_OBRAZ'
                , 'KLO':'LIN_OBRAZ'
                , 'KTO':'TXT_OBRAZ'
                , 'KBO':'BOD_OBRAZ'
                , 'KPO':'PLO_OBRAZ'
                }[tag]

        for feature_data in layer_data:
            feature = QgsFeature()
            
            if tag in ['BZL', 'JP', 'OP']:
                feature.setAttributes([
                        feature_data.find('../../../..').get('LHC_KOD')
                        , feature_data.find('../../..').get('ODD')
                        , feature_data.find('../..').get('DIL')
                        , feature_data.find('..').get('POR')]
                    +[feature_data.get(a) for a in attnames if a not in [
                        'lhc_kod', 'odd', 'dil', 'por']
                    ])
            elif tag == 'PSK':
                feature.setAttributes([
                        feature_data.find('../../../..').get('LHC_KOD')
                        , feature_data.find('../../..').get('ODD')
                        , feature_data.find('../..').get('DIL')
                        , feature_data.find('..').get('POR')]
                    +[feature_data.get(a) for a in attnames if a not in [
                        'lhc_kod', 'odd', 'dil', 'por','etz']]
                    #+ [ json.dumps(dict(etz.attrib)) for etz in feature_data.xpath('ETZ')]
                    #+ [json.dumps([dict(etz.attrib) for etz in feature_data.xpath('ETZ')])]
                    + [json.dumps([
                        (lambda x,y: dict(x, **y))(etz.attrib,
                            {'DRV':[drv.attrib for drv in etz.xpath('DRV')]}) for etz in feature_data.xpath('ETZ')
                        ])]
                    #pridany dreviny pro Oldu Cizka
                    )
            else:
                feature.setAttributes([feature_data.get(a) for a in attnames])

            try:
                feature.setGeometry(
                    islh_parser.parse_geometry(feature_data.find(geom_tag))
                    )
            except TypeError:
                QMessageBox.critical(QDialog()
                        ,u"Prvek se nepodařilo vytvořit",u"%s"%etree.tostring(feature_data))


            pr.addFeatures([feature])

            #posunu progres bar
            self.dockwidget.progressBar.setValue(next(self.progres))

        #nakonec se mrknu, esli je PSK ZNACKA
        if tag == 'PSK' and not 'PSK_ZNACKA' in attnames:
            layer.addExpressionField('znacka(etz)', QgsField('PSK_ZNACKA',QVariant.Int))

            