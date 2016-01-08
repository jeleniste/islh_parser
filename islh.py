# -*- coding: utf-8 -*-
"""
/***************************************************************************
 islh_parser
                                 A QGIS plugin
 Display data from forest plan format
                              -------------------
        begin                : 2015-12-18
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Jelen
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt, QVariant\
        ,QUrl
from PyQt4.QtGui import QAction, QIcon, QFileDialog, QDialog, QMessageBox, QInputDialog\
        , QColor
# Initialize Qt resources from file resources.py
import resources

# Import the code for the DockWidget
from islh_dockwidget import islh_parserDockWidget
from hk_dockwidget import hk_displayDockWidget
#import os.path
import os

from lxml import etree
import simplejson as json
##from osgeo import ogr
from qgis.core import QgsFeatureRequest, QgsGeometry, QgsMapLayerRegistry\
        , QgsCoordinateReferenceSystem, QgsField\
        , QgsFeature, QgsPoint, QgsProject, QgsVectorLayer\
        , QgsSpatialIndex

import ciselniky


class islh_parser:
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
            'islh_parser_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&LHPO data viewer')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'islh_parser')
        self.toolbar.setObjectName(u'islh_parser')

        #print "** INITIALIZING islh_parser"

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
        return QCoreApplication.translate('islh_parser', message)


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
            text=self.tr(u'ISLH'),
            callback=self.run,
            parent=self.iface.mainWindow())

    #--------------------------------------------------------------------------

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        #print "** CLOSING islh_parser"

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

        #print "** UNLOAD islh_parser"

        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&LHPO data viewer'),
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
        filename = QFileDialog.getOpenFileName(self.dockwidget, "Select ISLH XML file ","", '*.xml')
        self.dockwidget.input_file.setText(filename)

    def read_islh(self):

        os.chdir(self.plugin_dir) #musim do plugin diru, abysem nacet svg

        if not self.dockwidget.input_file.text():
            QMessageBox.critical(QDialog()
                    ,u"Missing file",u"Není vybrán žádný soubor")
        else:
            self.f = open(self.dockwidget.input_file.text())
            try:
                #nachroustam xml
                self.dockwidget.output_working_on.setText(u"načítám XML")
                self.load_xml()

            except:
                QMessageBox.critical(QDialog()
                        ,u"vadný soubor",u"soubor se nepodařilo načíst")

            #pridam skupinu
            self.layerTreeRoot = QgsProject.instance().layerTreeRoot()
            self.por_mapa_group = self.layerTreeRoot.insertGroup(0, u'Porostní mapa')


            #self.psk_layer = self.iface.addVectorLayer('MultiPolygon'
            self.psk_layer = QgsVectorLayer('MultiPolygon'
                    , 'PSK', 'memory')

            self.psk_layer.loadNamedStyle('styles/por_mapa.qml')

            #self.crs = self.psk_layer.crs()
            #self.crs.createFromId(5514)
            #self.psk_layer.setCrs(self.crs)
            self.crs = QgsCoordinateReferenceSystem()
            self.crs.createFromId(5514)
            self.psk_layer.setCrs(self.crs)

            self.dockwidget.output_working_on.setText(u"generuji vrstvu PSK")

            try:

                self.populate_layer('ODD/DIL/POR/PSK', self.psk_layer)

                #pridam index

                self.psk_index = QgsSpatialIndex()
                for f in self.psk_layer.getFeatures():
                    self.psk_index.insertFeature(f)

                
                QgsMapLayerRegistry.instance().addMapLayer(self.psk_layer, False)
                self.por_mapa_group.addLayer(self.psk_layer)

            except:
                QMessageBox.critical(QDialog()
                        ,u"Nevhodný formát dat",u"nepodařilo se vytvořit vrstvu PSK")


            #kpo
            self.kpo_layer = QgsVectorLayer('Multipolygon'
                    , 'KPO', 'memory')

            self.kpo_layer.loadNamedStyle('styles/por_mapa_kpo.qml')

            self.kpo_layer.setCrs(self.crs)

            self.dockwidget.output_working_on.setText(u"generuji vrstvu KPO")

            try:

                self.populate_layer('KPO', self.kpo_layer)

                #index nepridam, je to jen kartoska

                QgsMapLayerRegistry.instance().addMapLayer(self.kpo_layer, False)
                #self.por_mapa_group.addLayer(self.kpo_layer)
                self.por_mapa_group.insertLayer(0, self.kpo_layer)

            except:
                QMessageBox.critical(QDialog()
                        ,u"Chyba vytváření KPO",u"nepodařilo se vytvořit vrstvu KPO")

            #-----

            #klo
            self.klo_layer = QgsVectorLayer('Linestring'
                    , 'KLO', 'memory')

            self.klo_layer.loadNamedStyle('styles/porostni_mapa_linie.qml')

            self.klo_layer.setCrs(self.crs)

            self.dockwidget.output_working_on.setText(u"generuji vrstvu KLO")

            try:

                self.populate_layer('KLO', self.klo_layer)

                #index nepridam, je to jen kartoska

                QgsMapLayerRegistry.instance().addMapLayer(self.klo_layer, False)
                #self.por_mapa_group.addLayer(self.klo_layer)
                self.por_mapa_group.insertLayer(0, self.klo_layer)

            except:
                QMessageBox.critical(QDialog()
                        ,u"Chyba vytváření KLO",u"nepodařilo se vytvořit vrstvu KLO")

            #-----

            #kbo
            self.kbo_layer = QgsVectorLayer('MultiPoint'
                    , 'KBO', 'memory')

            self.kbo_layer.loadNamedStyle('styles/styly_body.qml')

            self.kbo_layer.setCrs(self.crs)

            self.dockwidget.output_working_on.setText(u"generuji vrstvu KBO")

            try:

                self.populate_layer('KBO', self.kbo_layer)

                #index nepridam, je to jen kartoska

                QgsMapLayerRegistry.instance().addMapLayer(self.kbo_layer, False)
                #self.por_mapa_group.addLayer(self.kbo_layer)
                self.por_mapa_group.insertLayer(0, self.kbo_layer)

            except:
                QMessageBox.critical(QDialog()
                        ,u"Chyba vytváření KBO",u"nepodařilo se vytvořit vrstvu KBO")

            #-----

            #kto
            self.kto_layer = QgsVectorLayer('Point'
                    , 'KTO', 'memory')

            self.kto_layer.loadNamedStyle('styles/styly_txt.qml')

            self.kto_layer.setCrs(self.crs)

            self.dockwidget.output_working_on.setText(u"generuji vrstvu KTO")

            try:

                self.populate_layer('KTO', self.kto_layer)

                #index nepridam, je to jen kartoska

                QgsMapLayerRegistry.instance().addMapLayer(self.kto_layer, False)
                #self.por_mapa_group.addLayer(self.kto_layer)
                self.por_mapa_group.insertLayer(0, self.kto_layer)

            except:
                QMessageBox.critical(QDialog()
                        ,u"Chyba vytváření KTO",u"nepodařilo se vytvořit vrstvu KTO")

            #-----
            #BZL JP OP
            #skupina
            self.bzl_jp_op_mapa_group = self.layerTreeRoot.insertGroup(1, u'BZL, JP, OP')

            #-----

            #bzl
            self.bzl_layer = QgsVectorLayer('Multipolygon'
                    , 'BZL', 'memory')

            #self.psk_layer.loadNamedStyle('styles/por_mapa.qml')

            self.bzl_layer.setCrs(self.crs)

            self.dockwidget.output_working_on.setText(u"generuji vrstvu BZL")


            try:
                self.populate_layer('ODD/DIL/POR/BZL', self.bzl_layer)

                #index nepridam, je to jen kartoska

                QgsMapLayerRegistry.instance().addMapLayer(self.bzl_layer, False)
                #self.por_mapa_group.addLayer(self.bzl_layer)
                self.bzl_jp_op_mapa_group.insertLayer(0, self.bzl_layer)

            except:
                QMessageBox.critical(QDialog()
                        ,u"Chyba vytváření BZL",u"nepodařilo se vytvořit vrstvu BZL")


            #------

            #jp
            self.jp_layer = QgsVectorLayer('Multipolygon'
                    , 'JP', 'memory')

            #self.psk_layer.loadNamedStyle('styles/por_mapa.qml')

            self.jp_layer.setCrs(self.crs)

            self.dockwidget.output_working_on.setText(u"generuji vrstvu JP")


            self.populate_layer('ODD/DIL/POR/JP', self.jp_layer)

            #index nepridam, je to jen kartoska

            QgsMapLayerRegistry.instance().addMapLayer(self.jp_layer, False)
            #self.por_mapa_group.addLayer(self.jp_layer)
            self.bzl_jp_op_mapa_group.insertLayer(0, self.jp_layer)
            try:
                a=1

            except:
                QMessageBox.critical(QDialog()
                        ,u"Chyba vytváření JP",u"nepodařilo se vytvořit vrstvu JP")


            #------

            #op
            self.op_layer = QgsVectorLayer('Multipolygon'
                    , 'OP', 'memory')

            #self.psk_layer.loadNamedStyle('styles/por_mapa.qml')

            self.op_layer.setCrs(self.crs)

            self.dockwidget.output_working_on.setText(u"generuji vrstvu OP")

            #try:

            self.populate_layer('ODD/DIL/POR/OP', self.op_layer)

            #index nepridam, je to jen kartoska

            QgsMapLayerRegistry.instance().addMapLayer(self.op_layer, False)
            #self.por_mapa_group.addLayer(self.op_layer)
            self.bzl_jp_op_mapa_group.insertLayer(0, self.op_layer)

            try:
                a=1

            except:
                QMessageBox.critical(QDialog()
                        ,u"Chyba vytváření OP",u"nepodařilo se vytvořit vrstvu OP")


            #------
            self.bzl_jp_op_mapa_group.setVisible(Qt.Unchecked)



            lhc_list = [self.lhc.get('LHC_KOD')]
            self.dockwidget.input_lhc.clear()
            self.dockwidget.input_lhc.addItems(lhc_list)

            #nastavit komba na zacatek
            self.select_lhc()
            self.select_odd()
            self.select_dil()
            self.select_por()
            self.select_psk()

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
        self.psk_layer.setSelectedFeatures([])

        #vyber
        request = QgsFeatureRequest().setFilterExpression( 
                "lhc_kod = '%s' AND odd = '%s'"%
                self.jprl)

        it = self.psk_layer.getFeatures( request )
        self.psk_layer.setSelectedFeatures([f.id() for f in it])

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
        self.psk_layer.setSelectedFeatures([])

        #vyber
        request = QgsFeatureRequest().setFilterExpression( 
                "lhc_kod = '%s' AND odd = '%s' AND dil ='%s'"%
                self.jprl)

        it = self.psk_layer.getFeatures( request )
        self.psk_layer.setSelectedFeatures([f.id() for f in it])

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
        self.psk_layer.setSelectedFeatures([])

        #vyber
        request = QgsFeatureRequest().setFilterExpression( 
                "lhc_kod = '%s' AND odd = '%s' AND dil ='%s' AND por = '%s'"%
                self.jprl)

        it = self.psk_layer.getFeatures( request )
        self.psk_layer.setSelectedFeatures([f.id() for f in it])

        box = self.psk_layer.boundingBoxOfSelected()
        self.iface.mapCanvas().setExtent(box)
        self.iface.mapCanvas().refresh()

        self.select_psk() #workaround kvuli 


    def select_psk(self):

        self.psk = self.por.find("PSK[@PSK='%s']"%self.dockwidget.input_psk.currentText())

        self.jprl = (
                self.lhc.get('LHC_KOD')
                , self.odd.get('ODD')
                , self.dil.get('DIL')
                , self.por.get('POR')
                , self.psk.get('PSK'))

        #zrus vybrane graficky
        self.psk_layer.setSelectedFeatures([])

        #vyber
        request = QgsFeatureRequest().setFilterExpression( 
                "lhc_kod = '%s' AND odd = '%s' AND dil ='%s' AND por = '%s' AND psk = '%s'"%
                self.jprl)

        it = self.psk_layer.getFeatures( request )
        self.psk_layer.setSelectedFeatures([f.id() for f in it])

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

        if len(self.psk_layer.selectedFeatures()) == 1: #musi bejt prave jeden
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

            #self.psk_layer.setSelectedFeatures([])



        if self.hk_widget == None:
            self.hk_widget = hk_displayDockWidget()

        self.iface.addDockWidget(Qt.TopDockWidgetArea, self.hk_widget)

        self.result = self.transform(self.root
                , ODD="'%s'"%self.jprl[1]
                , DIL="'%s'"%self.jprl[2]
                , POR="'%s'"%self.jprl[3]
                , PSK="'%s'"%self.jprl[4])

        self.hk_widget.webView.setHtml(
                etree.tostring(self.result)
                )

        self.hk_widget.show()



    

    #--------------------------------------------------------------------------
    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True

            #print "** STARTING islh_parser"

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget == None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = islh_parserDockWidget()

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

            from karto_fce import *


    #----------------------------------------------------
    #plugin logic
    def load_xml(self):
        """:param f: file with islh xml data"""
        self.doc = etree.parse(self.f)
        self.root = self.doc.getroot()
        self.lhc = self.root.find("./LHC")

    def populate_layer(self, PATH, layer):
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
                    + [json.dumps([dict(etz.attrib) for etz in feature_data.xpath('ETZ')])]
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
            self.dockwidget.progressBar.setValue(self.progres.next())

        #nakonec se mrknu, esli je PSK ZNACKA
        if tag == 'PSK' and not 'PSK_ZNACKA' in attnames:
            layer.addExpressionField('znacka(etz)', QgsField('PSK_ZNACKA',QVariant.Int))

            
    #------------------------------------
    ##geometry
    @staticmethod
    def parse_geometry(gr):
        """node s ISLH grafikou"""

        g = gr[0] #obraz ma jen jeden prvek

        geom = (
                QgsGeometry.fromPoint(islh_parser.parse_point(g)) if g.tag == 'B'
                else QgsGeometry.fromPolyline(islh_parser.parse_line(g)) if g.tag == 'L'
                else QgsGeometry.fromMultiPoint(islh_parser.parse_multipoint(g)) if g.tag == 'MB'
                else QgsGeometry.fromMultiPolyline(islh_parser.parse_multiline(g)) if g.tag == 'ML'
                else QgsGeometry.fromPolygon(islh_parser.parse_polygon(g)) if g.tag == 'P'
                else QgsGeometry.fromMultiPolygon(islh_parser.parse_multipolygon(g)) if g.tag == 'MP' 
                else None) 

        return(geom)

    @staticmethod
    def parse_point(p):
        """udělá z bodu ogr bod"""

        (y,x) = map(lambda x: -float(x), p.get('S').split('$'))
        return(
                QgsPoint(x,y)
                )

    @staticmethod
    def parse_line(l):
        """udělá z bodu ogr bod"""

        return(
                [islh_parser.parse_point(point) for point in l.xpath('B')]
                )

    @staticmethod
    def parse_multipoint(l):

        return(
                [islh_parser.parse_point(point) for point in l.xpath('B')]
                )

    @staticmethod
    def parse_multiline(p):

        return(
                [islh_parser.parse_line(line) for line in p.xpath('L')]
                )

    @staticmethod
    def parse_polygon(p):

        return(
                [islh_parser.parse_line(line) for line in p.xpath('L')]
                )


    @staticmethod
    def parse_multipolygon(p):
        return(
                [islh_parser.parse_polygon(polygon) for polygon in p.xpath('P')]
                )

