from qgis.utils import qgsfunction
from psk_znacka import psk_znacka

@qgsfunction(args='auto', group='islh_parser')
def znacka(etz, feature, parent):
    return(psk_znacka(etz).vrat_znacku())


@qgsfunction(args='auto', group='islh_parser')
def barva(barva, feature, parent):
    return(
            {
               "0":"#BFBFBF",
               "1":"#0000BF",
               "2":"#00BF00",
               "3":"#00BFBF",
               "4":"#BF0000",
               "5":"#BF00BF",
               "6":"#BF7F00",
               "7":"#7F7F7F",
               "8":"#0000FF",
               "9":"#00FF00",
               "10":"#00FFFF",
               "11":"#FF0000",
               "12":"#FF00FF",
               "13":"#000000",
               "14":"#FFFF00",
               "15":"#FFFFFF",
               "17":"#FFBF00",
               "-9":"#000047",
               "-480":"#007700",
               "-512":"#007F00",
               "-602":"#008ECE",
               "-21504":"#A70000",
               "-23838":"#B73FF0",
               "-25600":"#C70000",
               "-31756":"#F7005F",
               "-32384":"#F79F00"
            }[barva]
            )

