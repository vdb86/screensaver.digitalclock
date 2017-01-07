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
import random
import os
from datetime import datetime

Addon = xbmcaddon.Addon('screensaver.digitalclock')
path = Addon.getAddonInfo('path').decode("utf-8")
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
        self.date_control = self.getControl(30100)
        self.hour_control = self.getControl(30101)
        self.colon_control = self.getControl(30102)
        self.minute_control = self.getControl(30103)
        self.ampm_control = self.getControl(30104)
        self.information_control = self.getControl(30110)		
        self.container = self.getControl(30002)
        self.image_control = self.getControl(30020)
        self.icon_control = self.getControl(30021)	
        self.waitcounter = 0
        self.switchcounter = 0
        self.iconswitchcounter = 0
        self.logoutcounter = 0		
        self.switch = 0
        self.iconswitch = 0	
        self.movementtype = int(Addon.getSetting('movementtype'))
        self.movementspeed = int(Addon.getSetting('movementspeed'))
        self.stayinplace = int(Addon.getSetting('stayinplace'))
        self.datef=Addon.getSetting('dateformat')
        self.customdateformat=Addon.getSetting('customdateformat')		
        self.colonblink=Addon.getSetting('colonblink')		
        self.timef=Addon.getSetting('timeformat')
        self.shadowf=Addon.getSetting('shadowformat')		
        self.ampm_control.setVisible(False)
        self.informationshow = Addon.getSetting('additionalinformation')	
        self.nowplayinginfoshow = Addon.getSetting('nowplayinginfoshow')
        self.cpuusage = Addon.getSetting('cpuusage')
        self.batterylevel = Addon.getSetting('batterylevel')
        self.freememory = Addon.getSetting('freememory')
        self.movies = Addon.getSetting('movies')
        self.tvshows = Addon.getSetting('tvshows')
        self.music = Addon.getSetting('music')		
        self.weatherinfoshow = Addon.getSetting('weatherinfoshow')
        self.albumartshow = Addon.getSetting('albumartshow')		
        self.weathericonf=Addon.getSetting('weathericonformat')		
        self.infoswitch = int(Addon.getSetting('infoswitch'))				
        self.background = Addon.getSetting('backgroundchoice')
        self.randomimages = Addon.getSetting('randomimages')
        self.skinhelper = int(Addon.getSetting('skinhelper'))
        self.randomcolor = Addon.getSetting('randomcolor')
        self.randomtr = Addon.getSetting('randomtr')
        self.trh = int(Addon.getSetting('hourtr'))
        self.trc = int(Addon.getSetting('colontr'))
        self.trm = int(Addon.getSetting('minutetr'))
        self.trampm = int(Addon.getSetting('ampmtr'))
        self.trd = int(Addon.getSetting('datetr'))
        self.tri = int(Addon.getSetting('informationtr'))
        self.trw = int(Addon.getSetting('icontr'))		
        self.ch = int(Addon.getSetting('hourcolor'))
        self.cc = int(Addon.getSetting('coloncolor'))
        self.cm = int(Addon.getSetting('minutecolor'))
        self.campm = int(Addon.getSetting('ampmcolor'))
        self.cd = int(Addon.getSetting('datecolor'))
        self.ci = int(Addon.getSetting('informationcolor'))
        self.cw = int(Addon.getSetting('iconcolor'))
        self.zoom = float(Addon.getSetting('zoomlevel'))
        self.logout = Addon.getSetting('logout')
        self.logoutplaying = Addon.getSetting('logoutplaying')
        self.logouttime = int(Addon.getSetting('logouttime'))
        self.hour_colorcontrol = self.getControl(30105)
        self.colon_colorcontrol = self.getControl(30106)
        self.minute_colorcontrol = self.getControl(30107)
        self.ampm_colorcontrol = self.getControl(30108)
        self.date_colorcontrol = self.getControl(30109)
        self.information_colorcontrol = self.getControl(30111)
        self.shadow_colorcontrol = self.getControl(30112)
        self.monitor = xbmc.Monitor()
			
		#setting up background and slideshow
        self.timer = ['15','30','60','120','180','240','300','360','420','480','540','600']
        self.slideshowcounter = 0		
        if self.background == '0':
            self.image = ['white.png','red.png','green.png','blue.png','yellow.png','black.png']		
            self.image_control.setImage(os.path.join(path,"resources/media/", self.image[int(Addon.getSetting('image'))]))
        elif self.background == '1':
            self.image_control.setImage(Addon.getSetting('file'))
        elif self.background == '2':
            self.folder = Addon.getSetting('folder')
            self.imagetimer = int(self.timer[int(Addon.getSetting('imagetimer'))])
            self.number = len(os.walk(self.folder).next()[2])-1
            self.files = os.walk(self.folder).next()[2]
            self.files.sort()
            self.nextfile = 0
            if self.randomimages =='true':
                self.nextfile = random.randint(0,self.number)
            self.path = self.folder + self.files[self.nextfile]
            self.nextfile += 1
            if self.nextfile > self.number:
                self.nextfile = 0
            self.image_control.setImage(self.path)
        else:
            self.imagetimer = int(self.timer[int(Addon.getSetting('imagetimer'))])		
            xbmc.executebuiltin('Skin.SetString(SkinHelper.RandomFanartDelay,%s)' %self.imagetimer)
            if self.skinhelper == 0:
                self.skinhelperimage = "$INFO[Window(Home).Property(SkinHelper.AllMoviesBackground)]"
            elif self.skinhelper == 1:
                self.skinhelperimage = "$INFO[Window(Home).Property(SkinHelper.AllTvShowsBackground)]"			
            elif self.skinhelper == 2:
                self.skinhelperimage = "$INFO[Window(Home).Property(SkinHelper.AllMusicBackground)]"
            else:
                self.skinhelperimage = "$INFO[Window(Home).Property(SkinHelper.GlobalFanartBackground)]"			
            self.image_control.setImage(xbmc.getInfoLabel(self.skinhelperimage))
			
		#setting up color transparency
        self.transparency = ['FF','E5','CC','B2','99','7F','66','4C','33','19','00']
		
		#setting up colors
        self.color = ['FFFFFF','FF0000','00FF00','0000FF','FFFF00','000000']
		
		#setting up shadow colors
        self.shadowcolor = ['00000000','FFFFFFFF','FF808080','FF000000']
        self.shadow_colorcontrol.setLabel(self.shadowcolor[int(self.shadowf)])
     
        #setting up information
        self.informationlist = []		
        if self.informationshow == 'true':		
            if self.nowplayinginfoshow == 'true':
                if xbmc.getInfoLabel('MusicPlayer.Artist') and xbmc.getInfoLabel('MusicPlayer.Title'):
                    self.informationlist.append('$INFO[MusicPlayer.Artist]')
                    self.informationlist.append('$INFO[MusicPlayer.Title]')					
                if xbmc.getInfoLabel('VideoPlayer.TVShowTitle'):
                    self.informationlist.append('$INFO[VideoPlayer.TVShowTitle]')				
                if xbmc.getInfoLabel('VideoPlayer.Title'):
                    self.informationlist.append('$INFO[VideoPlayer.Title]')
            if self.cpuusage == 'true' and xbmc.getInfoLabel('System.CpuUsage'):
                self.informationlist.append("$LOCALIZE[140] $INFO[System.CpuUsage]")			
            if self.batterylevel == 'true' and xbmc.getInfoLabel('System.BatteryLevel'):
                self.informationlist.append("$LOCALIZE[12395]: $INFO[System.BatteryLevel]")			
            if self.freememory == 'true' and xbmc.getInfoLabel('System.FreeMemory'):
                self.informationlist.append("$LOCALIZE[158]: $INFO[System.FreeMemory]")			
            if self.movies == 'true' and xbmc.getInfoLabel('Window(Home).Property(Movies.Count)'):
                self.informationlist.append("$LOCALIZE[20342]: $INFO[Window(Home).Property(Movies.Count)]")
                self.informationlist.append("$LOCALIZE[20342]-$LOCALIZE[16102]: $INFO[Window(Home).Property(Movies.Watched)]")
                self.informationlist.append("$LOCALIZE[20342]-$LOCALIZE[16101]: $INFO[Window(Home).Property(Movies.UnWatched)]")				
            if self.tvshows == 'true' and xbmc.getInfoLabel('Window(Home).Property(TVShows.Count)'):
                self.informationlist.append("$LOCALIZE[20343]: $INFO[Window(Home).Property(TVShows.Count)]")
                self.informationlist.append("$LOCALIZE[20360]: $INFO[Window(Home).Property(Episodes.Count)]")
                self.informationlist.append("$LOCALIZE[20343]-$LOCALIZE[16102]: $INFO[Window(Home).Property(TVShows.Watched)]")
                self.informationlist.append("$LOCALIZE[20360]-$LOCALIZE[16102]: $INFO[Window(Home).Property(Episodes.Watched)]")
                self.informationlist.append("$LOCALIZE[20343]-$LOCALIZE[16101]: $INFO[Window(Home).Property(TVShows.UnWatched)]")
                self.informationlist.append("$LOCALIZE[20360]-$LOCALIZE[16101]: $INFO[Window(Home).Property(Episodes.UnWatched)]")				
            if self.music == 'true' and xbmc.getInfoLabel('Window(Home).Property(Music.SongsCount)'):
                self.informationlist.append("$LOCALIZE[133]: $INFO[Window(Home).Property(Music.ArtistsCount)]")
                self.informationlist.append("$LOCALIZE[132]: $INFO[Window(Home).Property(Music.AlbumsCount)]")
                self.informationlist.append("$LOCALIZE[134]: $INFO[Window(Home).Property(Music.SongsCount)]")				
            if self.weatherinfoshow == 'true' and xbmc.getInfoLabel('Weather.Location'):
                self.informationlist.append("$INFO[Weather.Temperature] - $INFO[Weather.Conditions]")				
            if len(self.informationlist) != 0:
                self.information = self.informationlist[0]

		#setting up the date format and positions
        self.dateformat = ['Hide date','$INFO[System.Date(DDD dd. MMM yyyy)]','$INFO[System.Date(dd.mm.yyyy)]','$INFO[System.Date(mm.dd.yyyy)]']		
        if self.datef == '0':
            self.date_control.setVisible(False)
            if self.informationshow == 'true':
                if len(self.informationlist) != 0:
                    self.information_control.setPosition(0, 85)				
                    if ((self.weathericonf != '0' and xbmc.getInfoLabel('Weather.Location')) or (self.albumartshow =='true' and xbmc.getInfoLabel('MusicPlayer.Artist'))):
                        self.icon_control.setPosition(115, 120)					
                        self.container.setHeight(int(240 + 30 * (self.zoom / 100 - 1)))
                    else:
                        self.container.setHeight(int(150 + 50 * (self.zoom / 100 - 1)))
                        self.icon_control.setVisible(False)						
                else:
                    if ((self.weathericonf != '0' and xbmc.getInfoLabel('Weather.Location')) or (self.albumartshow =='true' and xbmc.getInfoLabel('MusicPlayer.Artist'))):
                        self.icon_control.setPosition(115, 90)					
                        self.container.setHeight(int(210 + 50 * (self.zoom / 100 - 1)))
                    else:
                        self.container.setHeight(int(90 + 110 * (self.zoom / 100 - 1)))
                        self.icon_control.setVisible(False)				
                    self.information_control.setVisible(False)					
            else:
                self.container.setHeight(int(100 + 110 * (self.zoom / 100 - 1)))
                self.icon_control.setVisible(False)					
                self.information_control.setVisible(False)
        else:
            if self.informationshow == 'true':
                if len(self.informationlist) != 0:
                    if not((self.weathericonf != '0' and xbmc.getInfoLabel('Weather.Location')) or (self.albumartshow =='true' and xbmc.getInfoLabel('MusicPlayer.Artist'))):
                        self.container.setHeight(int(180 + 50 * (self.zoom / 100 - 1)))
                        self.icon_control.setVisible(False)						
                else:
                    if ((self.weathericonf != '0' and xbmc.getInfoLabel('Weather.Location')) or (self.albumartshow =='true' and xbmc.getInfoLabel('MusicPlayer.Artist'))):
                        self.icon_control.setPosition(115, 120)					
                        self.container.setHeight(int(240 + 30 * (self.zoom / 100 - 1)))
                    else:
                        self.container.setHeight(int(140 + 50 * (self.zoom / 100 - 1)))
                        self.icon_control.setVisible(False)				
                    self.information_control.setVisible(False)					
            else:
                self.container.setHeight(int(150 + 50 * (self.zoom / 100 - 1)))
                self.icon_control.setVisible(False)					
                self.information_control.setVisible(False)
				
		#setting up custom format		
        if int(self.datef) == 4:		
            self.date = ('$INFO[System.Date(%s)]' %self.customdateformat)
        else:				
            self.date = self.dateformat[int(self.datef)]

		#setting weather icon set
        self.weathericonset = ['Hide weather icon','set1','set2','set3','set4']
	
		#setting the icon image
        if self.weathericonf != '0':
            self.icon = os.path.join(path,"resources/weathericons/",self.weathericonset[int(self.weathericonf)],xbmc.getInfoLabel('Window(Weather).Property(Current.FanartCode)')) + ".png"
        elif self.albumartshow == 'true':
            self.icon = xbmc.getInfoLabel('Player.art(thumb)')
        else:
            self.icon_control.setImage(os.path.join(path,"resources/weathericons/",self.weathericonset[int(self.weathericonf)],xbmc.getInfoLabel('Window(Weather).Property(Current.FanartCode)')) + ".png")
			
		#setting up the time format
        self.timeformat = ['%H','%I','%I']
        if self.timef == '2':
           self.ampm_control.setVisible(True)
        self.time = self.timeformat[int(self.timef)]
		
		#setting up movement type and wait timer	
        if self.movementtype == 0:
            self.waittimer = 0.5
            self.multiplier = 2
        elif self.movementtype == 1:
            self.waittimer = 0.02
            self.multiplier = 50
            self.dx = random.choice([-(self.movementspeed+1),(self.movementspeed+1)])
            self.dy = random.choice([-(self.movementspeed+1),(self.movementspeed+1)])
        elif self.movementtype == 3:
            self.waittimer = 0.5
            self.multiplier = 2
            self.container.setPosition(int(Addon.getSetting('customx')),int(Addon.getSetting('customy')))			
        else:
            self.waittimer = 0.5
            self.multiplier = 2
		
		#setting up the screen size
        self.height = self.container.getHeight()
        self.width = self.container.getWidth()
        self.screenye = int(720 + 120 * (self.zoom / 100 - 1) - self.height * self.zoom / 100)
        self.screenys = int(280 * (self.zoom / 100 - 1) - 18 * (self.zoom / 100 - 1))		
        self.screenxe = int(1280 - self.width * self.zoom / 100)
        self.screenxs = int(360 * (self.zoom / 100 - 1))		
		
		#combining transparency and color
        self.setCTR()
        self.Display()
		
        self.DisplayTime()
        
    def DisplayTime(self):
        while not self.abort_requested:				
		
            #switching information	
            self.Switch()

			#movement
            if self.movementtype == 0:			
                #random movement
                self.waitcounter += 1			
                if self.waitcounter >= (self.multiplier*self.stayinplace):
                    new_x = random.randint(self.screenxs,self.screenxe)
                    new_y = random.randint(self.screenys,self.screenye)
                    self.container.setPosition(new_x,new_y)
                    self.waitcounter = 0
                    self.setCTR()
            elif self.movementtype == 1:
                #bounce
                self.currentposition = self.container.getPosition()
                new_x = self.currentposition[0] + self.dx
                new_y = self.currentposition[1] + self.dy
                if new_x >= self.screenxe or new_x <= self.screenxs:
                    self.dx = self.dx*-1
                    new_x = self.currentposition[0] + self.dx					
                    self.setCTR()					
                if new_y >= self.screenye or new_y <= self.screenys:
                    self.dy = self.dy*-1
                    new_y = self.currentposition[1] + self.dy					
                    self.setCTR()					
                self.container.setPosition(new_x,new_y)

		    #display time
            self.Display()			
				
			#slideshow
            if self.background == '2':
                self.slideshowcounter +=1
                if self.slideshowcounter >= (self.multiplier*self.imagetimer):
                    if self.randomimages =='true':
                        self.nextfile = random.randint(0,self.number)
                    self.path = self.folder + self.files[self.nextfile]
                    self.image_control.setImage(self.path)	
                    self.nextfile +=1
                    self.slideshowcounter = 0
                    if self.nextfile > self.number:
                        self.nextfile = 0

			#skin helper
            if self.background == '3':
                self.slideshowcounter +=1
                if self.slideshowcounter >= (self.multiplier*self.imagetimer):
                    self.image_control.setImage(xbmc.getInfoLabel(self.skinhelperimage))
                    self.slideshowcounter = 0
				
			#colon blink
            if self.colonblink == 'true':			
                if datetime.now().second%2==0:
                    self.colon_control.setVisible(True)
                else:
                    self.colon_control.setVisible(False)
            else:					
                self.colon_control.setVisible(True)
				
			#log out
            if self.logout == 'true' and xbmc.getCondVisibility('Window.Previous(loginscreen)') == 0:
                self.logoutcounter +=1
                if self.logoutcounter >= (self.multiplier*self.logouttime*60):
                    if xbmc.getCondVisibility('Player.HasMedia') == 1:
                        if self.logoutplaying == 'true':
                            xbmc.executebuiltin("PlayerControl(Stop)")
                            xbmc.log('Digital Clock Screensaver %s: Stopping media' %Addonversion)							
                            xbmc.executebuiltin("System.LogOff")
                            xbmc.log('Digital Clock Screensaver %s: Logging out' %Addonversion)						
                            self.logoutcounter = 0
                    else:
                        xbmc.executebuiltin("System.LogOff")
                        xbmc.log('Digital Clock Screensaver %s: Logging out' %Addonversion)						
                        self.logoutcounter = 0			
				
            self.monitor.waitForAbort(self.waittimer)
					
    def setCTR(self):
        if self.randomcolor == 'false' and self.randomtr == 'false':
            self.hourcolor = self.transparency[self.trh] + self.color[self.ch]
            self.coloncolor = self.transparency[self.trc] + self.color[self.cc]
            self.minutecolor = self.transparency[self.trm] + self.color[self.cm]
            self.ampmcolor = self.transparency[self.trampm] + self.color[self.campm]
            self.datecolor = self.transparency[self.trd] + self.color[self.cd]
            self.informationcolor = self.transparency[self.tri] + self.color[self.ci]
            self.iconcolor = self.transparency[self.trw] + self.color[self.cw]		
        elif self.randomcolor == 'true' and self.randomtr == 'false':
            self.rc = str("%06x" % random.randint(0, 0xFFFFFF))
            self.hourcolor = self.transparency[self.trh] + self.rc
            self.coloncolor = self.transparency[self.trc] + self.rc
            self.minutecolor = self.transparency[self.trm] + self.rc
            self.ampmcolor = self.transparency[self.trampm] + self.rc
            self.datecolor = self.transparency[self.trd] + self.rc
            self.informationcolor = self.transparency[self.tri] + self.rc
            self.iconcolor = self.transparency[self.trw] + self.rc			
        elif self.randomcolor == 'false' and self.randomtr == 'true':
            self.rtr = str("%02x" % random.randint(0x4C, 0xFF))
            self.hourcolor = self.rtr + self.color[self.ch]
            self.coloncolor = self.rtr + self.color[self.cc]
            self.minutecolor = self.rtr + self.color[self.cm]
            self.ampmcolor = self.rtr + self.color[self.campm]
            self.datecolor = self.rtr + self.color[self.cd]
            self.informationcolor = self.rtr + self.color[self.ci]
            self.iconcolor = self.rtr + self.color[self.cw]			
        elif self.randomcolor == 'true' and self.randomtr == 'true':
            self.rc = str("%06x" % random.randint(0, 0xFFFFFF))
            self.rtr = str("%02x" % random.randint(0x4C, 0xFF))
            self.hourcolor = self.rtr + self.rc
            self.coloncolor = self.rtr + self.rc
            self.minutecolor = self.rtr + self.rc
            self.ampmcolor = self.rtr + self.rc
            self.datecolor = self.rtr + self.rc
            self.informationcolor = self.rtr + self.rc
            self.iconcolor = self.rtr + self.rc		

    def Display(self):
        self.hour_control.setLabel(datetime.now().strftime(self.time))
        self.colon_control.setLabel(" : ")   			
        self.minute_control.setLabel(datetime.now().strftime("%M"))
        self.ampm_control.setLabel(datetime.now().strftime("%p"))
        self.date_control.setLabel(self.date)
        if len(self.informationlist) != 0:
            self.information_control.setLabel(self.information)
        if self.weathericonf != '0' or self.albumartshow == 'true':
            self.icon_control.setImage(self.icon)
        self.hour_colorcontrol.setLabel(self.hourcolor)
        self.colon_colorcontrol.setLabel(self.coloncolor)   			
        self.minute_colorcontrol.setLabel(self.minutecolor)
        self.ampm_colorcontrol.setLabel(self.ampmcolor)
        self.date_colorcontrol.setLabel(self.datecolor)
        self.information_colorcontrol.setLabel(self.informationcolor)
        self.icon_control.setColorDiffuse(self.iconcolor)		

    def Switch(self):
        if len(self.informationlist) > 1:
            self.switchcounter += 1
            if self.switchcounter == (self.multiplier*self.infoswitch):
                self.switch += 1
                self.switchcounter = 0
                self.information = self.informationlist[self.switch]
                if self.switch == len(self.informationlist)-1:
                    self.switch = -1				
	
        if self.weathericonf != '0' and self.albumartshow == 'true' and xbmc.getInfoLabel('Player.art(thumb)'):
            self.iconswitchcounter += 1
            if self.iconswitchcounter == (self.multiplier*self.infoswitch):
                self.iconswitch += 1
                self.iconswitchcounter = 0
                if self.iconswitch == 2:
                    self.iconswitch = 0
            if self.iconswitch == 0:
                self.icon = os.path.join(path,"resources/weathericons/",self.weathericonset[int(self.weathericonf)],xbmc.getInfoLabel('Window(Weather).Property(Current.FanartCode)')) + ".png"
            else:
                self.icon = xbmc.getInfoLabel('Player.art(thumb)')			
		
    def exit(self):
        self.abort_requested = True
        self.exit_monitor = None
        xbmc.log('Digital Clock Screensaver %s: Abort requested' %Addonversion)
        self.close()

if __name__ == '__main__':
    xbmc.log('Digital Clock Screensaver %s: Started' %Addonversion)
    if(os.path.isfile(xbmc.translatePath('special://skin/1080i/script-screensaver-digitalclock-custom.xml'))):
        screensaver = Screensaver('script-screensaver-digitalclock-custom.xml', xbmc.translatePath('special://skin/1080i/'), 'default')
    elif(os.path.isfile(xbmc.translatePath('special://skin/720p/script-screensaver-digitalclock-custom.xml'))):
        screensaver = Screensaver('script-screensaver-digitalclock-custom.xml', xbmc.translatePath('special://skin/720p/'), 'default')
    elif(os.path.isfile(xbmc.translatePath('special://skin/21x9/script-screensaver-digitalclock-custom.xml'))):
        screensaver = Screensaver('script-screensaver-digitalclock-custom.xml', xbmc.translatePath('special://skin/21x9/'), 'default')
    elif(os.path.isfile(xbmc.translatePath('special://skin/16x9/script-screensaver-digitalclock-custom.xml'))):
        screensaver = Screensaver('script-screensaver-digitalclock-custom.xml', xbmc.translatePath('special://skin/16x9/'), 'default')
    elif(os.path.isfile(xbmc.translatePath('special://skin/4x3Hirez/script-screensaver-digitalclock-custom.xml'))):
        screensaver = Screensaver('script-screensaver-digitalclock-custom.xml', xbmc.translatePath('special://skin/4x3Hirez/'), 'default')
    elif(os.path.isfile(os.path.join(path,"resources/skins/default/720p/",scriptname))):
        screensaver = Screensaver(scriptname, path, 'default')
    else:
        screensaver = Screensaver('skin.default.xml', path, 'default')	
    screensaver.doModal()
    screensaver.close()
    del screensaver
    xbmc.log('Digital Clock Screensaver %s: Stopped' %Addonversion)	
    sys.modules.clear()