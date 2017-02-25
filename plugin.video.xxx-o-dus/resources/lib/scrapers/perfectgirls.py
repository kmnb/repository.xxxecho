"""
    Copyright (C) 2016 ECHO Coder

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
#Imports
import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import urllib2,urllib
import time
import base64
import re
from resources.lib.modules  import common
from resources.lib.modules  import downloader
from resources.lib.modules  import plugintools
import datetime

#Default veriables
AddonTitle           = "[COLOR red]XXX-O-DUS[/COLOR]"
addon_id             = 'plugin.video.xxx-o-dus'
dialog               = xbmcgui.Dialog()
fanart               = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/perfectgirls/fanart.jpg'))
icon                 = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/perfectgirls/icon.png'))
HISTORY_FILE         = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'history.xml'))
FAVOURITES_FILE      = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'favourites.xml'))
DOWNLOADS_FILE       = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'downloads.xml'))

def MAIN_MENU():

	common.addDir("[COLOR red][B]SEARCH[/B][/COLOR]","url",312,icon,fanart)

	result = common.open_url('http://www.perfectgirls.net')
	
	match = re.compile('<table id="cats">(.+?)</table>',re.DOTALL).findall(result)
	string = str(match)
	match2 = re.compile('<td>(.+?)</td>',re.DOTALL).findall(string)
	fail = 0
	videos = 0
	for item in match2:
		try:
			url=re.compile('<a href="(.+?)">.+?</a><br>').findall(item)[0]
			title=re.compile('<a href=".+?">(.+?)</a><br>').findall(item)[0]
			number=re.compile('<a href=".+?">.+?</a><br>.+?((.+?) clips)').findall(item)[0]
			url = 'http://www.perfectgirls.net' + url
			b = str(number)
			c = b.replace('\\n','').replace('\n','').replace(' ','').replace('clips','').replace('(','').replace(')','').replace('\\','').replace("'",'')
			c = c.split(',')[0]
			videos = videos + int(float(c))
			name = "[COLOR white]" + title + " [/COLOR]-[I] " + str(c) + " videos[/I]"
			common.addDir(name,url,311,icon,fanart)
		except: pass

	kodi_name = common.GET_KODI_VERSION()

	if kodi_name == "Jarvis":
		xbmc.executebuiltin('Container.SetViewMode(50)')
	elif kodi_name == "Krypton":
		xbmc.executebuiltin('Container.SetViewMode(55)')
	else: xbmc.executebuiltin('Container.SetViewMode(50)')

def GET_CONTENT(url):

	nextpage = 0
	try:
		a,url = url.split('|')
	except: nextpage = 1

	checker = url
	result = common.open_url(url)
	match = re.compile('<td>(.+?)</td>',re.DOTALL).findall(result)
	for item in match:
		try:
			title=re.compile('title="(.+?)"').findall(item)[0]
			url=re.compile('href="(.+?)"').findall(item)[0]
			iconimage=re.compile('src="(.+?)"').findall(item)[0]
			if "http" not in iconimage:
				iconimage=re.compile('data-original="(.+?)"').findall(item)[0]
			url = 'http://www.perfectgirls.net' + url
			url2 = title + '|SPLIT|' + url
			name = '[COLOR pink]' + title + '[/COLOR]'
			name = common.CLEANUP(name)
			common.addLink(name,url2,313,iconimage,iconimage)
		except: pass
	if nextpage == 1:
		try:
			np=re.compile('rel="next" href="(.+?)">').findall(result)[0]
			a = int(np) - 1
			b = str(a)
			if b in checker:
				url = checker.replace(b,np)
			else: url = checker + '/' + np
			common.addDir('[COLOR pink]Next Page >>[/COLOR]',url,311,icon,fanart)       
		except:pass

	kodi_name = common.GET_KODI_VERSION()

	if kodi_name == "Jarvis":
		xbmc.executebuiltin('Container.SetViewMode(500)')
	elif kodi_name == "Krypton":
		xbmc.executebuiltin('Container.SetViewMode(52)')
	else: xbmc.executebuiltin('Container.SetViewMode(500)')

def SEARCH():

    string =''
    keyboard = xbmc.Keyboard(string, 'Enter Search Term')
    keyboard.doModal()
    if keyboard.isConfirmed():
        string = keyboard.getText().replace(' ','%20')
        if len(string)>1:
            url = "http://www.perfectgirls.net/search/" + string.lower() + '/'
            GET_CONTENT(url)
        else: quit()

def PLAY_URL(name,url,iconimage):

	name,url = url.split('|SPLIT|')
	dp = common.GET_LUCKY()
	ref_url = url
	result = common.open_url(url)
	result2 = re.compile("get\(\"/get/(.*?).mp4\"",re.DOTALL).findall(result)[0]
	get_vid = "http://perfectgirls.net/get/" + result2 + ".mp4"
	result3 = common.open_url(get_vid)
	result4 = re.compile("http(.*?).mp4",re.DOTALL).findall(result3)[0]
	url = "http" + result4 + ".mp4"
	choice = dialog.select("[COLOR red]Please select an option[/COLOR]", ['[COLOR pink]Watch Video[/COLOR]','[COLOR pink]Add to Favourites[/COLOR]','[COLOR pink]Download Video[/COLOR]'])

	if choice == 1:
		a=open(FAVOURITES_FILE).read()
		b=a.replace('#START OF FILE#', '#START OF FILE#\n<item>\n<name>'+str(name)+'</name>\n<link>'+str(url)+'</link>\n<site>Perfect Girls</site>\n<icon>'+str(iconimage)+'</icon>\n</item>\n')
		f= open(FAVOURITES_FILE, mode='w')
		f.write(str(b))
		f.close()
		dp.close()
		dialog.ok(AddonTitle, "[COLOR pink]" + name + " has been added to your favourites. You can access your favourites on the main menu.[/COLOR]")
		quit()
	
	elif choice == 2:
		try:
			download_location   = plugintools.get_setting("download_location")
			download_folder = xbmc.translatePath(download_location)
			_in = url
			name = name.replace(' ','_').replace('[COLOR','').replace('[/COLOR','').replace('[I]','').replace(']','').replace('|','').replace('%','').replace('-','').replace('[/I','').replace('[/B','').replace('[','').replace('/','').replace(':','')
			_out = download_folder + name + '.mp4'
			dp.close()
			a=open(DOWNLOADS_FILE).read()
			b=a.replace('#START OF FILE#', '#START OF FILE#\n<item>\n<name>'+str(_out)+'</name>\n<icon>'+str(iconimage)+'</icon>\n</item>\n')
			f= open(DOWNLOADS_FILE, mode='w')
			f.write(str(b))
			f.close()
			downloader.download(_in,_out,dp=None)
			dialog.ok(AddonTitle, "[COLOR pink]Your video has been successfully downloaded and can be viewed from the Your Downloads section on the main menu.[/COLOR]") 
		except: 
			try:
				os.remove(_out)
			except: pass
			dp.close()
			dialog.ok(AddonTitle, "[COLOR pink]Sorry, there was an error trying to download the video.[/COLOR]")
			quit()
	
	elif choice == 0:
		history_on_off  = plugintools.get_setting("history_setting")
		if history_on_off == "true":	
			date_now = datetime.datetime.now().strftime("%d-%m-%Y")
			time_now = datetime.datetime.now().strftime("%H:%M")
			a=open(HISTORY_FILE).read()
			b=a.replace('#START OF FILE#', '#START OF FILE#\n<item>\n<date>'+str(date_now)+'</date>\n<time>'+str(time_now)+'</time>\n<name>'+str(name)+'</name>\n<link>'+str(url)+'</link>\n<site>Perfect Girls</site>\n<icon>'+str(iconimage)+'</icon>\n</item>\n')
			f= open(HISTORY_FILE, mode='w')
			f.write(str(b))
			f.close()

		import urlresolver
		if urlresolver.HostedMediaFile(url).valid_url(): 
			url = urlresolver.HostedMediaFile(url).resolve()
		liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
		dp.close()
		xbmc.Player ().play(url, liz, False)
	else:
		dp.close()
		quit()
