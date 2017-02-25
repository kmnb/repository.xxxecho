#
#  Tron Wizard for Kodi
#
#  Copyright (C) 2016 
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
import os
import sys
import urllib
import urlparse
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import time
import base64
import requests
import re
import xbmcvfs
import urllib2,urllib


DIALOG         	= xbmcgui.Dialog()
DP             	= xbmcgui.DialogProgress()
HOME           	= xbmc.translatePath('special://home/')
ADDONS         	= os.path.join(HOME,     'addons')
USERDATA       	= os.path.join(HOME,     'userdata')
ADDON        	= xbmcaddon.Addon()
ADDONID      	= ADDON.getAddonInfo('id')
ADDONVERSION 	= ADDON.getAddonInfo('version')
CWD         	= ADDON.getAddonInfo('path').decode('utf-8')
ACTION_PREVIOUS_MENU = 10
ACTION_SELECT_ITEM = 7

AddonTitle = 'You Porn'
#Default veriables

NEW_VIDS       	= 'http://www.youporn.com/'
TOP_VIDS       	= 'http://www.youporn.com/top_rated/'
MOST_FAV       	= 'http://www.youporn.com/most_favorited/'
MOST_VIEW      	= 'http://www.youporn.com/most_viewed/'
MOST_DIS       	= 'http://www.youporn.com/most_discussed/'

class WindowXML(xbmcgui.WindowXML):
	def onInit(self):
		#Put list populating code/GUI startup things here
		self.window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
		self.list_control = self.window.getControl(401)
		self.pornvids = self.window.getControl(402)
		self.categories()
		self.GET_CONTENT(NEW_VIDS,self.pornvids)

	def categories(self):
		result = requests.get('http://www.youporn.com/categories')
		match = re.compile("id='categoryList'>(.+?)<div class='title-bar sixteen-column'>",re.DOTALL).findall(result.content)
		string = str(match)
		match2 = sorted(re.compile("<a h(.+?)</p>",re.DOTALL).findall(string))
		fail = 0
		videos = 0
		for item in match2:
			url=re.compile('ref="(.+?)"').findall(item)[0]
			title=re.compile('alt="(.+?)"').findall(item)[0]
			icon_cat=re.compile('original="(.+?)"').findall(item)[0]
			a = str(icon_cat)
			icon_cat = a.replace(' ','%20')
			if "http" not in str(icon_cat):
				icon_cat = icon
			number=re.compile('<span>(.+?)</span>').findall(item)[0]
			b = str(number)
			c = b.replace(',','').replace(' Videos','')
			videos = videos + int(float(c))
			url3 = url
			url4 = url3.replace('\\','')
			url = "http://www.youporn.com" + url4
			name = "[COLOR rose][B]" + title + " - " + number + "[/B][/COLOR]"
			self.list_control.addItem(xbmcgui.ListItem(name, label2=url, iconImage=icon_cat, thumbnailImage=icon_cat))

	def GET_CONTENT(self,url,currentlist):
		global souperback
		global souperbad
		checker = url
		result = requests.get(url)
		match = re.compile('video-box four-column(.+?)<div class="video-box-title">',re.DOTALL).findall(result.content)
		for item in match:
			try:
				title=re.compile("alt=(.+?)'").findall(item)[0]
				url=re.compile('<a href="(.+?)"').findall(item)[0]
				iconimage=re.compile('<img src="(.+?)"').findall(item)[0]
				if "icon-hd-text" in item:
					name = "[B][COLOR orangered]HD[/COLOR][COLOR rose] - " + title + "[/COLOR][/B]"
					name = name.replace("'",'')
					currentlist.addItem(xbmcgui.ListItem(name, label2=url, iconImage=iconimage, thumbnailImage=iconimage))
				else:
					name = "[B][COLOR yellow]SD[/COLOR][COLOR rose] - " + title + "[/COLOR][/B]"
				#name = name.replace("'",'')
				#xbmc.log(url)
				#currentlist.addItem(xbmcgui.ListItem(name, label2=url, iconImage=iconimage, thumbnailImage=iconimage))
			except: pass
#		try:
		np=re.compile('<li class="current"(.+?)<div id="next">',re.DOTALL).findall(result.content)
		for item in np:
			current=re.compile('<div class="currentPage" data-page-number=".+?">(.+?)</div>').findall(item)[0]
			url2=re.compile('<a href="(.+?)=').findall(item)[0]
			next1 = int(float(current)) + 1
			url = "http://youporn.com" + str(url2) + "=" + str(next1)
			souperbad = url
			if next1 != 2:
				back1 = int(float(current)) - 1
				souperback = "http://youporn.com" + str(url2) + "=" + str(back1)
			else:
				souperback = "http://youporn.com" + str(url2) + "=" + str(1)
			#currentlist.addItem(xbmcgui.ListItem(name, label2=url, iconImage=iconimage, thumbnailImage=iconimage))
			#addDir('[COLOR pink]Next Page >>[/COLOR]',url,1,next_icon,fanart,'')       
#		except:pass
	def GET_LUCKY(self):

		import random
		lucky = random.randrange(10)
		
		dp = xbmcgui.DialogProgress()
		
		if lucky == 1:
			dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]We are getting the moisturiser.[/B][/COLOR]','[B][COLOR azure]Do you have the wipes ready?[/B][/COLOR]' )
		elif lucky == 2:
			dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]I am just taking off my pants.[/B][/COLOR]','[B][COLOR azure]Darn belt![/B][/COLOR]' )
		elif lucky == 3:
			dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]Are the curtains closed?[/B][/COLOR]')
		elif lucky == 4:
			dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]Its my fifth time today.[/B][/COLOR]','[B][COLOR azure]How about you?[/B][/COLOR]' )
		elif lucky == 5:
			dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]Please no buffer, please no buffer![/B][/COLOR]')
		elif lucky == 6:
			dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]I think I am goin blind :-/[/B][/COLOR]')
		elif lucky == 7:
			dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]Did I turn the oven off?[/B][/COLOR]','[B][COLOR azure]It can wait![/B][/COLOR]' )
		elif lucky == 8:
			dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]Your video is coming.[/B][/COLOR]','[B][COLOR azure]Do you get it?[/B][/COLOR]' )
		elif lucky == 9:
			dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]ISTV does not save your browsing history :-D[/B][/COLOR]')
		else:
			dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]There more XXX addons to come.[/B][/COLOR]','[B][COLOR azure]Just so you know.[/B][/COLOR]' )

		return dp
	def SEARCH(self):
	    string =''
	    keyboard = xbmc.Keyboard(string, 'Enter Search Term')
	    keyboard.doModal()
	    if keyboard.isConfirmed():
	        string = keyboard.getText().replace(' ','').capitalize()
	        if len(string)>1:
	            url = "http://www.youporn.com/search/?query=" + string + "&page="
	            xbmc.log(url)
	            self.GET_CONTENT(url,self.pornvids)
	        else: quit()
	def PLAY_URL(self,name,url,iconimage):
		dp = self.GET_LUCKY()
		url = "http://www.youporn.com" + url
		result = requests.get(url)
		match = re.compile('sources: {(.+?)}',re.DOTALL).findall(result.content)
		a = str(match)
		match = a.replace('\\','')
		try:
			url1 = re.compile("1080_60.+?'(.+?)',").findall(match)[0]
		except: url1 = "null"
		try:
			url2 = re.compile("1080.+?'(.+?)',").findall(match)[0]
		except:url2 = "null"
		try:
			url3 = re.compile("720_60+?'(.+?)',").findall(match)[0]
		except:url3 = "null"
		try:
			url4 = re.compile("720.+?'(.+?)',").findall(match)[0]
		except: url4 = "null"
		try:
			url5 = re.compile("480.+?'(.+?)',").findall(match)[0]
		except: url5 = "null"
		try:
			url6 = re.compile("240.+?'(.+?)',").findall(match)[0]
		except: url6 = "null"
		
		if "http" in url1:
			url_play = url1
		elif "http" in url2:
			url_play = url2
		elif "http" in url3:
			url_play = url3
		elif "http" in url4:
			url_play = url4
		elif "http" in url5:
			url_play = url5
		elif "http" in url6:
			url_play = url6
		liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
		time.sleep(2.00)
		dp.close()
		xbmc.Player ().play(url_play, liz, False)
	def onAction(self, action):
		if action == ACTION_PREVIOUS_MENU:
			self.close()
	def onClick(self,controlID):
		if controlID == 402:
			name = xbmc.getInfoLabel('Container(402).Listitem.Label')
			url = xbmc.getInfoLabel('Container(402).Listitem.Label2')
			icon = xbmc.getInfoLabel('Container(402).Listitem.Icon')
			self.PLAY_URL(name,url,icon)
		if controlID == 401:
			name = xbmc.getInfoLabel('Container(402).Listitem.Label')
			url = xbmc.getInfoLabel('Container(401).Listitem.Label2')
			try:
				while name:
					self.pornvids.removeItem(0)
			except:
				self.GET_CONTENT(url,self.pornvids)
				xbmc.log(self.soup)
		if controlID == 502:
			name = xbmc.getInfoLabel('Container(402).Listitem.Label')
			try:
				while name:
					self.pornvids.removeItem(0)
			except:
				xbmc.log(souperbad)
				self.GET_CONTENT(souperbad,self.pornvids)
		if controlID == 501:
			name = xbmc.getInfoLabel('Container(402).Listitem.Label')
			try:
				while name:
					self.pornvids.removeItem(0)
			except:
				self.GET_CONTENT(souperback,self.pornvids)
				xbmc.log(souperback)
		if controlID == 503:
			self.close()
		if controlID == 504:
			name = xbmc.getInfoLabel('Container(402).Listitem.Label')
			try:
				while name:
					self.pornvids.removeItem(0)
			except:
				self.SEARCH()
	def onFocus(self,controlID):
		pass
if __name__ == "__main__":
	scriptDir = xbmcaddon.Addon('plugin.video.youporn').getAddonInfo('path')
	sys.path.insert(0, os.path.join(scriptDir, 'resources', 'src'))
	w = WindowXML("home.xml", scriptDir)
	w.doModal()
	del w