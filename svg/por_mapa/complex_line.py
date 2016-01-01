
#First, we load our line shapefile:

lyr = iface.activeLayer()

#Next we get the symbol list and reference the default symbol:

symbolList = lyr.rendererV2().symbols()

symbol = symbolList[0]

#Then we create a shorter variable name for the symbol layer registry:

symLyrReg = QgsSymbolLayerV2Registry

#Now we set up the line style for the simple line using a python dictionary:

lineStyle = {'width':'0.26', 'color':'#FF0000'}

#Then we create an abstract symbol layer for a simple line:

symLyr1Meta = symLyrReg.instance().symbolLayerMetadata("SimpleLine")

#We instantiate a symbol layer from the abstract layer using the line style properties:

symLyr1 = symLyr1Meta.createSymbolLayer(lineStyle)

#Now we add the symbol layer to the layer's symbol:

symbol.appendSymbolLayer(symLyr1)

#Now to create the rails on the railroad, we begin building a marker line style with another python dictionary:

markerStyle = {}

markerStyle['width'] = '0.26'

markerStyle['color'] = '0,0,0'

markerStyle['interval'] = '3'

markerStyle['interval_unit'] = 'MM'

markerStyle['placement'] = 'interval'

markerStyle['rotate'] = '1'

#Then we create the marker line abstract symbol layer for the second symbol:

symLyr2Meta = symLyrReg.instance().symbolLayerMetadata("MarkerLine")

#We instatiate the symbol layer:

symLyr2 = symLyr2Meta.createSymbolLayer(markerStyle)

#Now we must work with a sub symbol that defines the markers along the marker line

sybSym = symLyr2.subSymbol()

#We must delete the default sub symbol:

sybSym.deleteSymbolLayer(0)

#Now we set up the style for our rail marker using a dictionary:

railStyle = {'size':'2', 'color':'0,0,0', 'name':'line', 'angle':'0'}

#Now we repeat the process of building a symbol layer and add it to the sub symbol:

railMeta = symLyrReg.instance().symbolLayerMetadata("SimpleMarker")

rail = railMeta.createSymbolLayer(railStyle)

sybSym.appendSymbolLayer(rail)

#Then we add the sub-symbol to the second symbol layer

symbol.appendSymbolLayer(symLyr2)

#Finally we add the layer to the map:

QgsMapLayerRegistry.instance().addMapLayer(lyr)

lyr.triggerRepaint()