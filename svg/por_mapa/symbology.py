layer = iface.activeLayer()
renderer = layer.rendererV2()
#props = layer.rendererV2().symbols()[0].symbolLayer(0).properties()
props = {
   "outline_width": "0.3",
   "outline_color": "0,0,0,255",
   "angle": "0",
   "width": "8",
   "color": "0,0,0,255",
   "svgFile_dd_useexpr": "1",
   "svgFile": "/home/jelen/jelen_dta/projekty/qgis_islh/plugin/symbology/10104.svg",
   "svgFile_dd_expression": "'/home/jelen/.qgis2/svg/prsi/'+\"PSK_ZNACKA\"+'.svg'",
   "outline_width_unit": "MM",
   "svg_outline_width_map_unit_scale": "0,0",
   "svgFile_dd_field": "",
   "pattern_width_unit": "MM",
   "svgFile_dd_active": "1",
   "outline_width_map_unit_scale": "0,0",
   "svg_outline_width_unit": "MM",
   "pattern_width_map_unit_scale": "0,0"
}

layer.rendererV2().setSymbol(
QgsFillSymbolV2().appendSymbolLayer(QgsSVGFillSymbolLayer.create(props)))

