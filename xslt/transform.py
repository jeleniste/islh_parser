# -*- coding: utf-8 -*-
from lxml import etree

##ciselniky

import ciselniky

ns = etree.FunctionNamespace("http://ciselniky")
ns.prefix = "cis"
ns['lesni_oblast'] = ciselniky.lesni_oblast
ns['slt'] = ciselniky.slt
ns['katuze'] = ciselniky.katuze
ns['lvs'] = ciselniky.lvs
ns['zvl_statut'] = ciselniky.zvl_statut


xslt_root = etree.XML(open('hk.xsl','r').read())
transform = etree.XSLT(xslt_root)
doc = etree.parse(open('../../sample_dta/213801.xml','r'))
root = doc.getroot()
result = transform(root, ODD="'4'", DIL="'B'", POR="'a'", PSK="'7/4'")
f = open('test.html','w')
f.write(etree.tostring(result, pretty_print = True))
f.close()

#print(root.xpath('lesni_oblast("1")'))
