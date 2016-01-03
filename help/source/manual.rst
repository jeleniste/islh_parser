####################
Prohlížečka dat LHPO
####################

*****
Popis
*****

Qgis plugin slouží k načtení a zobrazení dat *lesních hospodářských plánů a
osnov* uložených ve `informačním standardu lesního hospodářství 
<http://www.uhul.cz/ke-stazeni/standardy/is-lhpo/129-informacni-standard-lesniho-hospodarstvi-pro-lhp-a-lho>`_.
Přidá vrstvy *jednotek prostorového rozdělení lesa*, tedy porostích skupin,
jiných ploch, ostatních ploch a bezlesí, dále přidá vrstvy kartografických
prvků, tedy KLO, KPO, KBO a KTO, tedy liniových, plošných, bodových a textových
značek. Zároveň je použito pro PSK, KLO, KPO, KBO a KTO zobrazení, které zhruba
odpovídá kartografii porostní mapy.

Zároveň modul umožňuje generovat a zobrazovat *hospodářskou knihu* pro
jednotlivé porostní skupiny a procházet porostní skupoiny hierarchicky. PSK pro
vygenerování hospodářské knihy je možné vybrat pomocí nabídky, nebo přímo v
mapě.

**********
Závislosti
**********

Plugin je testovaný pro Qgis 2.12 Lyon a pro jeho bezchybnou funkci je třeba mít
nainstalované moduly simplejson a lxml do pythonu 2.7 (obojí by mělo být v
`osgeo4w <https://trac.osgeo.org/osgeo4w/>`_), případně by neměl být problém je
doinstalovat pomocí `pip <https://trac.osgeo.org/osgeo4w/wiki/ExternalPythonPackages>`_,
případně z balíčků.


*********
Instalace
*********

K instalaci stačí stáhnout `celý repozitář <https://github.com/jeleniste/islh_parser>`_ 
jako zip (tlačítko *Download Zip*) a rozzipovat ho do vaší složky s moduly qgisu.
Potom se vám obejví plugin v nabídce instalovaných pluginů. Po jejím zaškrtnutí
vám přibude nová ikonka na horní liště.

*******
Použití
*******

Nahrání souboru s xml
=====================

Po kliknití na ikonku s výřezem porostní mapy se vám v levém dolním rohu objeví
nový *formulář*. Na kartě *soubor* stiskněte tlačítko s třemi tečkami a vyberte
soubor s xml. Poté stiskněte tlačítko *Read*. Proces může nějakou dobu trvat. Po
jeho skončení se vám v nabídce vrstev objeví dvě nové skupiny. *Porostní mapa* a
*BZL, JP, OP*, zároveň se naplní roletky na kartě *JPRL*. Postupným výběrem na
roletkách vám bude mapa zoomovat na oddělení, dílec, porost, psk. 

Generování hospodářské knihy
============================

Stisknutím tlačítka *Hospodářská kniha* se vygeneruje a zobrazí hospodářská
kniha pro vybranou porostní skupinu. PSK můžete vybrat buď pomocí roletek, nebo
v mapovém okně (musíte ale mít vybranou vrstvu PSK).

**********
Upozornění
**********

Modul byl vyvinut v důsledku dlouhé chvíle a výsledek není definitivní, ať co se
týče stávajícího řešení (které není technicky dotažené), nebo do nabídky
funkcionalit. Nejsem lesák a je pravděpodobné, že ne vše bude věcně správně.
Budu tedy vděčný za jakoukoliv zpětnou vazbu ať co se týče návrhů na další
funkcionality, nebo chyby, ať již věcné, nebo technické.
