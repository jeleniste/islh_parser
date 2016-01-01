xslt_root = etree.XML(open('../islh_parser/xslt/hk.xsl','r').read())
transform = etree.XSLT(xslt_root)
result = transform(dil, PSK="'6'", POR="'a'")
etree.tostring(result.getroot())
