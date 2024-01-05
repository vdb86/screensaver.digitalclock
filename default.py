#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Vojislav Vlasic
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
import xbmcaddon
import xbmcgui
import xbmc
import xbmcvfs
import random
import os
import time
from datetime import datetime

Addon = xbmcaddon.Addon('screensaver.digitalclock')
path = Addon.getAddonInfo('path')
location = xbmc.getSkinDir()
scriptname = location + '.xml'
Addonversion = Addon.getAddonInfo('version')

class Screensaver(xbmcgui.WindowXMLDialog):

	#setting up zoom
    window = xbmcgui.Window(12900)
    window.setProperty("zoomamount",Addon.getSetting('zoomlevel'))
    del window

    class ExitMonitor(xbmc.Monitor):

        def __init__(self, exit_callback):
            self.exit_callback = exit_callback

        def onScreensaverDeactivated(self):
            self.exit_callback()

    def onInit(self):
        xbmc.log('Digital Clock Screensaver %s: Initialising' %Addonversion)
        self.abort_requested = False
        self.started = False
        self.exit_monitor = self.ExitMonitor(self.exit)
        self.hour_control = self.getControl(30101)
        self.colon_control = self.getControl(30102)
        self.minute_control = self.getControl(30103)
        self.container = self.getControl(30002)
        self.image_control2 = self.getControl(30022)
        self.hour_colorcontrol = self.getControl(30105)
        self.colon_colorcontrol = self.getControl(30106)
        self.minute_colorcontrol = self.getControl(30107)
        self.monitor = xbmc.Monitor()


		#setting up the screen size
        self.height = self.container.getHeight()
        self.width = self.container.getWidth()
        self.screenye = int(680 + 120 * (100 / 100 - 1) - self.height * 100 / 100)
        self.screenys = int(280 * (100 / 100 - 1) - 18 * (100 / 100 - 1))
        self.screenxe = int(1280 - self.width * 100 / 100)
        self.screenxs = int(360 * (100 / 100 - 1))		


        self.backgroundcolor = 'FF000000'
        self.image_control2.setVisible(True)
        self.image_control2.setImage(os.path.join(path,"resources/media/white.png"))
        self.image_control2.setColorDiffuse(self.backgroundcolor)
        self.hourcolor = 'FFFFFFFF'
        self.coloncolor = 'FFFFFFFF'
        self.minutecolor = 'FFFFFFFF'
        self.hour_colorcontrol.setLabel(self.hourcolor)
        self.colon_colorcontrol.setLabel(self.coloncolor)
        self.minute_colorcontrol.setLabel(self.minutecolor)
        self.hour_control.setLabel("17")
        self.colon_control.setLabel(" : ")
        self.minute_control.setLabel("14")
        self.secondcounter=0
        self.new_x=0
        self.new_y=0
        self.dx=2
        self.dy=2
        self.DisplayTime()

    #The code below runs every 2 ms, this is needed for smooth movement.
	#As can be seen the code is minimal, the only time we're calling Kodi is to set the position of the container.
	#And yet even with the minimal code, the movement starts to stutter and becomes weird and choppy.
    def DisplayTime(self):
        while not self.abort_requested:
            self.new_x = self.new_x + self.dx
            self.new_y = self.new_y + self.dy
            if self.new_x >= self.screenxe or self.new_x <= self.screenxs:
                self.dx = self.dx*-1
            if self.new_y >= self.screenye or self.new_y <= self.screenys:
                self.dy = self.dy*-1
            self.container.setPosition(self.new_x,self.new_y)

		    #display time
            time.sleep(0.02)
            self.secondcounter=self.secondcounter+1
            if self.secondcounter == 50:
                self.secondcounter=0			
                self.monitor.waitForAbort(0.02)

    def exit(self):
        self.abort_requested = True
        self.exit_monitor = None
        xbmc.log('Digital Clock Screensaver %s: Abort requested' %Addonversion)
        self.close()

if __name__ == '__main__':
    xbmc.log('Digital Clock Screensaver %s: Started' %Addonversion)
    if(os.path.isfile(os.path.join(path,"resources/skins/default/720p/",scriptname))):
        screensaver = Screensaver(scriptname, path, 'default')
    else:
        screensaver = Screensaver('skin.default.xml', path, 'default')
    screensaver.doModal()
    screensaver.close()
    del screensaver
    xbmc.log('Digital Clock Screensaver %s: Stopped' %Addonversion)
    sys.modules.clear()
