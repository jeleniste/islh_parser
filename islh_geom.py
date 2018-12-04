from qgis.core import QgsVectorLayer, QgsFeature, QgsField, QgsGeometry
from PyQt4.QtCore import QVariant

def createLayer(data, lname='default', extra_attrs=[]):
    feature = data[0]
    geomtag = {
            'PSK':'PSK_OBRAZ'
            , 'BZL':'BZL_OBRAZ'
            , 'JP':'JP_OBRAZ'
            , 'OP':'OP_OBRAZ'
            , 'KLO':'LIN_OBRAZ'
            , 'KTO':'TXT_OBRAZ'
            , 'KBO':'BOD_OBRAZ'
            , 'KPO':'PLO_OBRAZ'
            }[feature.tag]
    
    geomtype = {
            'L':'Linestring'
            , 'P':'Polygon'
            , 'B':'Point'
            , 'MB':'MultiPoint'
            , 'ML':'Multilinestring'
            , 'MP':'MultiPolygon'
            }[list(feature.find(geomtag))[0].tag]

    layer = QgsVectorLayer(geomtype + '?crs=EPSG:5514', lname, 'memory')
    
    attnames = feature.keys()
    attnames = attnames + extra_attrs
 
    pr = layer.dataProvider()
    
    pr.addAttributes(
            [QgsField(a, QVariant.String) for a in attnames])
            
    layer.updateFields()
    
    #populateLayer(layer, data)
       
    return(layer)
    
def populateLayer(layer, data, extra_attrs={}, pbar = None):
    """:param extra_attrs: dict s extra atributama"""
    #jeste sem prijde progresbarr a extra attrs v dict

    if pbar is not None:
        featureCount = len(data)
        pbar.setRange(0, featureCount)
        progres = iter(range(0, featureCount + 1))
        pbar.setValue(progres.next())

    
    feature_list = []
    
    pr = layer.dataProvider()
    
    attnames = [f.name() for f in layer.pendingFields()\
            if f.name() not in extra_attrs.keys()]
    
    
    geomtag = {
            'PSK':'PSK_OBRAZ'
            , 'BZL':'BZL_OBRAZ'
            , 'JP':'JP_OBRAZ'
            , 'OP':'OP_OBRAZ'
            , 'KLO':'LIN_OBRAZ'
            , 'KTO':'TXT_OBRAZ'
            , 'KBO':'BOD_OBRAZ'
            , 'KPO':'PLO_OBRAZ'
            }[data[0].tag]
    
    for item in data:
        feature = QgsFeature()
        
        feature.setGeometry(islhToQgs(item.find(geomtag)))
        
        feature.setAttributes(
                [item.get(a) for a in attnames] +\
                        [extra_attrs[a] for a in\
                        [x.name() for x in layer.pendingFields()] \
                        if a in extra_attrs.keys()]
                )   
        
        feature_list.append(feature)
        if pbar is not None: pbar.setValue(progres.next())
        
        
    pr.addFeatures(feature_list)




#def islhToOgr(islh_obraz):
#    return(
#            ogr.CreateGeometryFromWkt(
#                    islhToWkt(lin_obraz)
#                    )
#            )
            
def islhToQgs(islh_obraz):
    return(
            QgsGeometry.fromWkt(
                    islhToWkt(islh_obraz)
                    )
            )
##pridat dalsi typy
def islhToWkt(islh_obraz):
    obraz = list(islh_obraz)[0]

    if obraz.tag == 'B':
        return(
                'POINT (' + islh_point(obraz) + ')'
                )
    elif obraz.tag == 'ML':
        return(
                'MULTILINESTRING ' + islh_multiline(obraz)
                )
    elif obraz.tag == 'L':
        return(
                'LINESTRING ' + islh_line(obraz)
                )
    elif obraz.tag == 'MP':
        return(
                'MULTIPOLYGON ' + islh_multipolygon(obraz)
                )
    elif obraz.tag == 'P':
        return(
                'POLYGON ' + islh_polygon(obraz)
                )                  
    elif obraz.tag == 'MB':
        return(
                'MULTIPOINT ' + islh_multipoint(obraz)
                )  
                
def islh_multiline(ml):
    return('(' + ','.join([
            islh_line(l) for l in list(ml)]) + ')')
            
def islh_line(l):
    return('(' + ','.join([
            islh_point(p) for p in list(l)]) + ')' )
            
def islh_point(p):
    (y, x) = [ -1 * float(i) for  i in p.get('S').split('$')]
    return( ' '.join((str(x), str(y))))
    
def islh_multipoint(mb):
    return('(' + ','.join([
            '(' + islh_point(p) + ')' for p in list(mb)]) + ')')
            
def islh_multipolygon(mp):
    return( '(' + ','.join([
            islh_polygon(p) for p in list(mp)]) + ')')
            
            
def islh_polygon(p):
    return( '(' + ','.join([
            islh_line(r) for r in list(p)]) + ')')
