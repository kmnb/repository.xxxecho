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
AddonTitle       = "[COLOR red]XXX-O-DUS[/COLOR]"
addon_id         = 'plugin.video.xxx-o-dus'
dialog           = xbmcgui.Dialog()
ADDON            = xbmcaddon.Addon(id=addon_id)
HOME             = xbmc.translatePath('special://home/')
fanart           = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/porncom/fanart.jpg'))
icon             = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/porncom/icon.png'))
next_icon        = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/porncom/next.png'))
search_icon      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/porncom/search.png'))
twitter_icon     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/porncom/twitter.png'))
pc_icon          = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/porncom/pc.png'))
HISTORY_FILE     = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'history.xml'))
FAVOURITES_FILE  = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'favourites.xml'))
DOWNLOADS_FILE   = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'downloads.xml'))
DATA_FOLDER      = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id))
SEARCH_FILE      = xbmc.translatePath(os.path.join(DATA_FOLDER , 'search.xml'))

def MAIN_MENU():

	common.addDir("[COLOR red][B]SEARCH[/B][/COLOR]","url",64,search_icon,fanart)

	result = common.open_url('http://www.porn.com/categories')
	match = re.compile('<div class="main"><h1>Featured Categories</h1>(.+?)<h2>All Categories</h2>',re.DOTALL).findall(result)
	string = str(match)
	match2 = re.compile('<a class="thum(.+?)data-id="',re.DOTALL).findall(string)
	for item in match2:
		url=re.compile('bs" href="(.+?)"').findall(item)[0]
		title=re.compile('title="(.+?)"').findall(item)[0]
		icon_cat=re.compile('<img src="(.+?)"').findall(item)[0]
		title = title.replace("porn",'')
		name = "[COLOR white]" + title + "[/COLOR]"
		name = common.CLEANUP(name)
		url = 'http://porn.com' + url
		common.addDir(name,url,61,icon_cat,fanart)

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

	namelist=[]
	urllist=[]
	iconlist=[]
	ratinglist=[]

	result = common.open_url(url)
	match = re.compile('<ul class="listThumbs">(.+?)<span class="numbers">',re.DOTALL).findall(result)
	string = str(match)
	match2 = re.compile('<a(.+?)class="icon-thumbs-up">',re.DOTALL).findall(string)
	for item in match2:
		title=re.compile('class="title">(.+?)<').findall(item)[0]
		url=re.compile('href="(.+?)"').findall(item)[0]
		iconimage=re.compile('src="(.+?)"').findall(item)[0]
		url = "http://porn.com" + str(url)
		try:
			rating=re.compile('class="rating">(.+?)<i').findall(item)[0]
			rating = rating.replace('% ','')
			rating = int(rating)
		except:
			rating = 0
		name = common.CLEANUP(title)
		if '<span class="hd">' in item:
			name = '[COLOR white] - [/COLOR][COLOR deepskyblue]HD[/COLOR] - [COLOR white]' + name + '[/COLOR]'
		else:
			name = '[COLOR white] - [/COLOR][COLOR orange]SD[/COLOR] - [COLOR white]' + name + '[/COLOR]'

		namelist.append(name)   
		urllist.append(url)		
		iconlist.append(iconimage)
		ratinglist.append(rating)
		combinedlists = list(zip(ratinglist,namelist,urllist,iconlist))

	tup = sorted(combinedlists, key=lambda x: int(x[0]),reverse=True)
	for rating,name,url,iconimage in tup:
		url2 = name+'|SPLIT|'+url
		common.addLink('[COLOR red]' + str(rating) + '%[/COLOR]' + name,url2,63,iconimage,iconimage)

	if nextpage == 1:	
		try:
			np=re.compile('<link rel="next" href="(.+?)"').findall(result)[0]
			url = "http://porn.com" + str(np) 
			common.addDir('[COLOR red]Next Page >>[/COLOR]',url,61,next_icon,fanart)       
		except:pass

	kodi_name = common.GET_KODI_VERSION()

	if kodi_name == "Jarvis":
		xbmc.executebuiltin('Container.SetViewMode(500)')
	elif kodi_name == "Krypton":
		xbmc.executebuiltin('Container.SetViewMode(52)')
	else: xbmc.executebuiltin('Container.SetViewMode(500)')

def SEARCH_DECIDE():

	search_on_off  = plugintools.get_setting("search_setting")
	if search_on_off == "true":
		name = "null"
		url = "62"
		common.SEARCH_HISTORY(name,url)
	else:
		url = "null"
		SEARCH(url)

def SEARCH(url):

	if url == "null":
		string =''
		keyboard = xbmc.Keyboard(string, 'Enter Search Term')
		keyboard.doModal()
		if keyboard.isConfirmed():
			search_on_off  = plugintools.get_setting("search_setting")
			if search_on_off == "true":
				term = keyboard.getText()
				a=open(SEARCH_FILE).read()
				b=a.replace('#START OF FILE#', '#START OF FILE#\n<item>\n<term>'+str(term)+'</term>\n</item>\n')
				f= open(SEARCH_FILE, mode='w')
				f.write(str(b))
			string = keyboard.getText().replace(' ','+')
			if len(string)>1:
				url = "http://www.porn.com/videos/search?q=" + string.lower()
				GET_CONTENT(url)
			else: quit()
	else:
		string = url.replace(' ','+')
		url = "http://www.porn.com/videos/search?q=" + string.lower()
		GET_CONTENT(url)

def PLAY_URL(name,url,iconimage):

	name,url = url.split('|SPLIT|')
	name = name.replace('[COLOR white] - [/COLOR][COLOR deepskyblue]HD[/COLOR] - [COLOR white]','').replace('[COLOR white] - [/COLOR][COLOR orange]SD[/COLOR] - [COLOR white]','').replace('[/COLOR]','').replace(' - ','')
	ref_url = url
	result = common.open_url(url)
	match = re.compile('html>(.+?)</html>',re.DOTALL).findall(result)
	a = str(match)
	match = a.replace('\\','')
	
	choice = dialog.select("[COLOR red]Please select an option[/COLOR]", ['[COLOR pink]Watch Video[/COLOR]','[COLOR pink]Add to Favourites[/COLOR]','[COLOR pink]Download Video[/COLOR]'])

	dp = common.GET_LUCKY()

	if choice == 1:
		a=open(FAVOURITES_FILE).read()
		b=a.replace('#START OF FILE#', '#START OF FILE#\n<item>\n<name>'+str(name)+'</name>\n<link>'+str(url)+'</link>\n<site>Porn.com</site>\n<icon>'+str(iconimage)+'</icon>\n</item>\n')
		f= open(FAVOURITES_FILE, mode='w')
		f.write(str(b))
		f.close()
		dp.close()
		dialog.ok(AddonTitle, "[COLOR pink]" + name + " has been added to your favourites. You can access your favourites on the main menu.[/COLOR]")
		quit()

	elif choice == 2:
		try:
			try:
				size1 = re.compile('MP4 1080p<span class="hd"></span><span class="l1">(.+?)</span></a><a href=".+?"').findall(match)[0]
				url1 = re.compile('MP4 1080p<span class="hd"></span><span class="l1">.+?</span></a><a href="(.+?)"').findall(match)[0]
			except: 
				size1 = "null"
				url1  = "null"
			try:
				size2 = re.compile('MP4 720p<span class="hd"></span><span class="l1">(.+?)</span></a><a href=".+?.mp4"').findall(match)[0]
				url2 = re.compile('MP4 720p<span class="hd"></span><span class="l1">.+?</span></a><a href="(.+?)"').findall(match)[0]
			except: 
				size2 = "null"
				url2  = "null"
			try:
				size3 = re.compile('MP4 480p.+?<span class="l1">(.+?)</span></a><a href=".+?.mp4"').findall(match)[0]
				url3 = re.compile('MP4 480p.+?<span class="l1">.+?</span></a><a href="(.+?)"').findall(match)[0]
			except: 
				size3 = "null"
				url3  = "null"
			try:
				size4 = re.compile('MP4 360p.+?<span class="l1">(.+?)</span></a><a href=".+?.mp4"').findall(match)[0]
				url4 = re.compile('MP4 360p.+?<span class="l1">.+?</span></a><a href="(.+?)"').findall(match)[0]
			except: 
				size4 = "null"
				url4  = "null"
			if "download" in url1:
				choice = dialog.select("[COLOR red]Please select an option[/COLOR]", ['[COLOR deepskyblue]Download 1080p ' + str(size1) + '[/COLOR]','[COLOR deepskyblue]Download 720p ' + str(size2) + '[/COLOR]','[COLOR deepskyblue]Download 480p ' + str(size3) + '[/COLOR]','[COLOR deepskyblue]Download 360p ' + str(size4) + '[/COLOR]'])
				if choice == 0: url_play = url1
				elif choice == 1: url_play = url2
				elif choice == 2: url_play = url3
				elif choice == 3: url_play = url4
			elif "download" in url2:
				choice = dialog.select("[COLOR red]Please select an option[/COLOR]", ['[COLOR deepskyblue]Download 720p ' + str(size2) + '[/COLOR]','[COLOR deepskyblue]Download 480p ' + str(size3) + '[/COLOR]','[COLOR deepskyblue]Download 360p ' + str(size4) + '[/COLOR]'])
				if choice == 0: url_play = url2
				elif choice == 1: url_play = url3
				elif choice == 2: url_play = url4
			elif "download" in url3:
				choice = dialog.select("[COLOR red]Please select an option[/COLOR]", ['[COLOR deepskyblue]Download 480p ' + str(size3) + '[/COLOR]','[COLOR deepskyblue]Download 360p ' + str(size4) + '[/COLOR]'])
				if choice == 0: url_play = url3
				elif choice == 1: url_play = url4
			elif "download" in url4:
				url_play = url4
			
			download_location   = plugintools.get_setting("download_location")
			download_folder = xbmc.translatePath(download_location)
			_in = 'http://www.porn.com/' + url_play
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
			b=a.replace('#START OF FILE#', '#START OF FILE#\n<item>\n<date>'+str(date_now)+'</date>\n<time>'+str(time_now)+'</time>\n<name>'+str(name)+'</name>\n<link>'+str(url)+'</link>\n<site>Porn.com</site>\n<icon>'+str(iconimage)+'</icon>\n</item>\n')
			f= open(HISTORY_FILE, mode='w')
			f.write(str(b))
			f.close()

		url_play = re.compile('{id:".+?",url:"(.+?)"').findall(match)[-1]

		url = url_play + '|User-Agent=Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36&Referer=' + ref_url
		liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
		dp.close()
		xbmc.Player ().play(url, liz, False)
	else:
		dp.close()
		quit()