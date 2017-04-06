# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Frames
                                 A QGIS plugin
 This plugin extract image from video
                             -------------------
        begin                : 2017-04-05
        copyright            : (C) 2017 by Katerina Sharlamanova
        email                : kate_sarlamanova@hotmail.com
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
    """Load Frames class from file Frames.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .ffm import Frames
    return Frames(iface)
