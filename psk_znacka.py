# -*- coding: utf-8 -*-
#import simplejson as json
import json
from math import floor

##TODO prepsat na etaz v jsonu kvuli pouziti na vyrazy u vrstvy psk

class psk_znacka():
    """spocte znacku psk z etree elementu"""

    #def __init__(self, psk):
    def __init__(self, etz):
        """:param psk: etree element"""

        #self.etaze = psk.xpath('ETZ')
        #self.psk = psk

#        self.etaze = {etaz.get('ETAZ'):{\
#                'ZAKM':int(etaz.get('ZAKM'))\
#                , 'VEK':int(etaz.get('VEK'))}\
#                for etaz in psk.xpath('ETZ')}

        self.etaze = {etaz['ETAZ']:{\
                'ZAKM':int(etaz['ZAKM'])\
                , 'VEK':int(etaz['VEK'])}\
                for etaz in json.loads(etz)}


        self.spocti_znacku()

    @staticmethod
    def vekova_trida(vek):
        return(floor(min((vek + 19), 179) /20))

    def spocti_znacku(self):
        """spocita znacku"""

#        Jediná etáž ve věku A se zakmeněním 7-10
#        10100 + Min((A+19),  179) div 20
#        Jediná etáž ve věku A se zakmeněním 4-6
#        10000 + Min((A+19),  179) div 20
#        Jediná etáž ve věku A se zakmeněním 1-3
#        20000 + Min((A+19),  179) div 20

        if len(self.etaze) == 1: #jedina etaz
            etaz = self.etaze[list(self.etaze.keys())[0]]
            vekova_trida = psk_znacka.vekova_trida(etaz['VEK'])
            zakmeneni = etaz['ZAKM']
            self.psk_znacka = vekova_trida + (
                    10100 if 7 <= zakmeneni 
                    else 10000 if 4 <= zakmeneni <= 6
                    else 20000 if 1 <= zakmeneni <= 3
                    else 0)

        elif len(self.etaze) == 2:
            #vymazu vek nula (holina)
            self.etaze = {k:v for k, v in self.etaze.iteritems() if v['VEK'] > 0}
            if len(self.etaze) < 2:
                self.spocti_znacku()
                return(None)


            klice = list(self.etaze.keys())


            # a je etaz s vetsim zakmenenim
            (etaz_a, etaz_b) = (self.etaze[klice[0]], self.etaze[klice[1]]) if \
                    self.etaze[klice[0]]['ZAKM'] > self.etaze[klice[1]]['ZAKM'] \
                    else (self.etaze[klice[1]], self.etaze[klice[0]])

            vekova_trida_a = psk_znacka.vekova_trida(etaz_a['VEK'])
            vekova_trida_b = psk_znacka.vekova_trida(etaz_b['VEK'])

            if 7 <= etaz_a['ZAKM']  and 1 <= etaz_b['ZAKM'] <= 3:
#                Dvě etáže, etáž se zakmeněním 7-10 ve věku A a další etáž se zakmeněním 1-3 ve věku B
#                pokud Min((A+19),  179) div 20 <> Min((B+19, 179):   20000 + 10*(Min((A+19),  179) div 20) + Min((B+19),  179) div 20
#                pokud Min((A+19),  179) div 20 = Min((B+19, 179):
#                10100 + Min((A+19),  179) div 20
                if vekova_trida_a == vekova_trida_b:
                    self.psk_znacka = 10100 + vekova_trida_a

                else:
                    self.psk_znacka = 20000 + 10 * vekova_trida_a + vekova_trida_b



            elif 7 <= etaz_a['ZAKM']  and 4 <= etaz_b['ZAKM'] <= 10:
                if etaz_b['VEK'] < etaz_a['VEK']:
                    (etaz_a, etaz_b) = (etaz_b, etaz_a) #kdyz je b mladsi, tak prehodim
                    vekova_trida_a = psk_znacka.vekova_trida(etaz_a['VEK'])
                    vekova_trida_b = psk_znacka.vekova_trida(etaz_b['VEK'])


#                Dvě etáže, etáž se zakmeněním 7-10 ve věku A a další etáž se zakmeněním 4-10 ve věku B
#                pokud Min((A+19),  179) div 20 <> Min((B+19, 179):   10000 + 10*(Min((A+19),  179) div 20) + Min((B+19),  179) div 20
#                pokud Min((A+19),  179) div 20 = Min((B+19, 179):
#                10100 + Min((A+19),  179) div 20


                if vekova_trida_a == vekova_trida_b:
                    self.psk_znacka = 10100 + vekova_trida_a

                else:
                    self.psk_znacka = 10000 + 10 * vekova_trida_a + vekova_trida_b

            elif 4 <= etaz_a['ZAKM'] <= 6 and 4 <= etaz_b['ZAKM'] <= 6:
                if etaz_b['VEK'] < etaz_a['VEK']:
#                Dvě etáže, obě etáže se zakmeněním 4-6, mladší ve věku A a starší  B
#                pokud Min((A+19),  179) div 20 <> Min((B+19, 179):   10000 + 10*(Min((A+19),  179) div 20) + Min((B+19),  179) div 20
#                pokud Min((A+19),  179) div 20 = Min((B+19, 179):
#                10100 + Min((A+19),  179) div 20
                    (etaz_a, etaz_b) = (etaz_b, etaz_a) #kdyz je b mladsi, tak prehodim
                    vekova_trida_a = psk_znacka.vekova_trida(etaz_a['VEK'])
                    vekova_trida_b = psk_znacka.vekova_trida(etaz_b['VEK'])

                if vekova_trida_a == vekova_trida_b:
                    self.psk_znacka = 10100 + vekova_trida_a

                else:
                    self.psk_znacka = 10000 + 10 * vekova_trida_a + vekova_trida_b

            elif 4 <= etaz_a['ZAKM'] <= 6 and 1 <= etaz_b['ZAKM'] <= 3:
#                Dvě etáže, etáž se zakmeněním 4-6 ve věku A a druhá etáž se zakmeněním 1-3 ve věku B
#                25000 + 10*(Min((A+19),  179) div 20) + Min((B+19),  179) div 20
                self.psk_znacka = 25000 + 10 * vekova_trida_a + vekova_trida_b


            elif 1 <= etaz_a['ZAKM'] <= 3 and 1 <= etaz_b['ZAKM'] <= 3:
#                Dvě etáže, obě etáže se zakmeněním 1-3, mladší ve věku A a starší  B
#                26000 + 10*(Min((A+19),  179) div 20) + Min((B+19),  179) div 20
                if etaz_b['VEK'] < etaz_a['VEK']:
                    (etaz_a, etaz_b) = (etaz_b, etaz_a) #kdyz je b mladsi, tak prehodim
                    vekova_trida_a = psk_znacka.vekova_trida(etaz_a['VEK'])
                    vekova_trida_b = psk_znacka.vekova_trida(etaz_b['VEK'])

                self.psk_znacka = 26000 + 10 * vekova_trida_a + vekova_trida_b

            else:
                self.psk_znacka = 0

        else:
#        Více než dvě etáže
#        použije se značka určená pomocí výše uvedených pravidel použitím hodnot pro dvě nejstarší etáže; v případě, že dvě nejstarší etáže mají obě zakmenění 1-3, pak se použije nejstarší etáž a nejstarší etáž se zakmeněním 4-10, pokud taková existuje
            etaze_vyber = sorted(\
                    [(int(v['VEK']), k) for k,v in self.etaze.iteritems()]
                    )[-2:]

            etaze_nove = {klic:self.etaze[klic] for klic in [vyber[1] for vyber in etaze_vyber]}

            if len([v for k, v in etaze_nove.iteritems() if 1<= v['ZAKM'] <=3 ]) == 2 \
                    and len([v for k,v in self.etaze.iteritems() if 4<= v['ZAKM'] <=10 ]):

                etaze_vyber = sorted(\
                        [(int(v['VEK']), k) for k,v in etaze.iteritems()]
                        )[-1] + \
                        sorted([(int(v['VEK']), k) for k,v in etaze.iteritems() if 4 <= v['ZAKM'] ]
                        )[-1] 

                etaze_nove = {klic:etaze[klic] for klic in [vyber[1] for vyber in etaze_vyber]}

            self.etaze = etaze_nove

            self.spocti_znacku()


    def vrat_znacku(self):
        """vrati znacku"""

        return( self.psk_znacka)

