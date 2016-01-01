src = '/home/jelen/jelen_dta/projekty/qgis_islh/sample_dta/kbo.geojson'

lyr = QgsVectorLayer(src, 'pokus','ogr')

svgStyle = {}

svgStyle['fill'] = '#0000ff'
svgStyle['name'] = 'landmark/tourism-museum.svg'
svgStyle['outline'] = '#000000'
svgStyle['outline-width'] = '6.8'
svgStyle['size'] = '6'

symLyr1 = QgsSvgMarkerSymbolLayerV2.create(svgStyle)
#symLyr1 = QgsSVGFillSymbolLayer.create(props)

lyr.rendererV2().symbols()[0].changeSymbolLayer(0, symLyr1)

QgsMapLayerRegistry.instance().addMapLayer(lyr)