# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Frames
                                 A QGIS plugin
 This plugin extract  image from video
                              -------------------
        begin                : 2017-04-04
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Katerina Sharlamanova
        email                : kate_sarlamanova@hotmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from ffm_dialog import FramesDialog
import os.path
import cv2
import Tkinter, tkFileDialog
import math
import os


class Frames:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.
        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Frames_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Frames from video')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Frames')
        self.toolbar.setObjectName(u'Frames')


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Frames', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = FramesDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Frames/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Frames from video'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Frames from video'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def video(self):
        root = Tkinter.Tk()
        root.withdraw()  # use to hide tkinter window

        self.file = tkFileDialog.askopenfile(parent=root, mode='rb', title='Choose a file')
        if self.file != None:
            data = self.file.read()
            print "You chose %s" % self.file.name
            print "I got %d bytes from this file." % len(data)
            print ""

        self.dlg.textEdit.setText(str(self.file.name))


    def directory(self):
        root = Tkinter.Tk()
        root.withdraw()  # use to hide tkinter window

        currdir = os.getcwd()
        self.tempdir = tkFileDialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
        if len(self.tempdir) > 0:
            print "You chose %s" % self.tempdir
            print ""

        self.dlg.textEdit_5.setText(str(self.tempdir))


    def currentTime(self):
        videoFile = self.file
        imagesFolder = self.tempdir

        x = float(self.dlg.textEdit_4.toPlainText())
        y = x * 1000

        vidcap = cv2.VideoCapture(str(videoFile.name))
        vidcap.set(cv2.CAP_PROP_POS_MSEC, y)  # just cue to x sec. position

        success, image = vidcap.read()

        if success:
            print 'Read a new frame: ', success
            cv2.imwrite(imagesFolder + "/image_%d.jpg" % x, image)

        vidcap.release()
        print ""
        print "Done!"


    def everySecond(self):
        videoFile = self.file
        imagesFolder = self.tempdir

        vidcap = cv2.VideoCapture(str(videoFile.name))

        frameRate = vidcap.get(5)  # frame rate

        while (vidcap.isOpened()):
            frameId = vidcap.get(1)  # current frame number
            success, image = vidcap.read()
            if (success != True):
                break
            if (frameId % math.floor(frameRate) == 0):
                filename = imagesFolder + "/image_" + str(int(frameId)) + ".jpg"
                print 'Read a new frame: ', success
                cv2.imwrite(filename, image)

        vidcap.release()
        print ""
        print "Done!"


    def all(self):
        videoFile = self.file
        imagesFolder = self.tempdir

        vidcap = cv2.VideoCapture(str(videoFile.name))

        count = 0
        success = True

        while success:
            success, image = vidcap.read()
            print 'Read a new frame: ', success
            cv2.imwrite(imagesFolder + "/image_%d.jpg" % count, image)  # save frame as JPEG file
            count += 1

        vidcap.release()
        print ""
        print "Done!"


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()

        self.dlg.pushButton.clicked.connect(self.video)
        self.dlg.pushButton_3.clicked.connect(self.directory)

        self.dlg.pushButton_2.clicked.connect(self.currentTime)
        self.dlg.pushButton_5.clicked.connect(self.everySecond)
        self.dlg.pushButton_8.clicked.connect(self.all)

        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            pass