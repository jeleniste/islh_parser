from lxml import etree
from psk_znacka import psk_znacka

#doc = etree.parse(open('../sample_dta/210405.xml','r'))
doc = etree.parse(open('../sample_dta/213401.xml','r'))
root = doc.getroot()

#psk_list = root.xpath('LHC/ODD/DIL/POR/PSK[count(ETZ) > 1]')
psk_list = root.xpath('LHC/ODD/DIL/POR/PSK')

for psk in psk_list:
    zn1 = int(psk.get('PSK_ZNACKA'))
    zn2 = psk_znacka(psk).vrat_znacku()
    if zn1 != zn2:
        print("%s  %s --- %s"%(psk.get('PSK'), zn1, zn2))
        for etz in psk.xpath('ETZ'):
            print("vek %s, zakmeneni %s"%(etz.get('VEK'), etz.get('ZAKM')))
