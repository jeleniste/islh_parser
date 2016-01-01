# -*- coding: utf-8 -*-
"""
/***************************************************************************
 islh_parser
                                 A QGIS plugin
 Display data from forest plan format
                             -------------------
        begin                : 2015-12-18
        copyright            : (C) 2015 by Jelen
        email                : godzilalalala@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load islh_parser class from file islh_parser.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .islh import islh_parser
    return islh_parser(iface)
