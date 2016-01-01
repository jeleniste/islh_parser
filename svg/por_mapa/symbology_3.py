iface.mapCanvas().mapRenderer().setDestinationCrs(crs)

src = '/home/jelen/jelen_dta/projekty/qgis_islh/sample_dta/psk.geojson'

lyr = QgsVectorLayer(src, 'pokus','ogr')

crs = QgsCoordinateReferenceSystem()

crs.createFromSrid(5514)
lyr.setCrs(crs)

props = {
#   "outline_width": "0.3",
#   "outline_color": "0,0,0,255",
#   "angle": "0",
   "width": "8",
#   "color": "0,0,0,255",
   "svgFile_dd_useexpr": "1",
   "svgFile": "",
   "svgFile_dd_expression": "'/home/jelen/.qgis2/svg/prsi/'+\"PSK_ZNACKA\"+'.svg'",
   "outline_width_unit": "MM",
   "svg_outline_width_map_unit_scale": "0,0",
#   "svgFile_dd_field": "",
   "pattern_width_unit": "MM",
   "svgFile_dd_active": "1",
   "outline_width_map_unit_scale": "0,0",
   "svg_outline_width_unit": "MM",
   "pattern_width_map_unit_scale": "0,0"
}

symLyr1 = QgsSVGFillSymbolLayer.create(props)

lyr.rendererV2().symbols()[0].changeSymbolLayer(0, symLyr1)

lyr.setLayerTransparency(50)

QgsMapLayerRegistry.instance().addMapLayer(lyr)