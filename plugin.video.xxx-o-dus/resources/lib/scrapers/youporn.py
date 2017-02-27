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
AddonTitle     = "[COLOR red]XXX-O-DUS[/COLOR]"
addon_id       = 'plugin.video.xxx-o-dus'
dialog         = xbmcgui.Dialog()
fanart         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/youporn/fanart.jpg'))
icon           = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/youporn/icon.png'))
next_icon      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/youporn/next.png'))
search_icon    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/youporn/search.png'))
discussed_icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/youporn/discussed.png'))
fav_icon       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/youporn/fav.png'))
new_icon       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/youporn/new.png'))
pc_icon        = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/youporn/pc.png'))
top_icon       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/youporn/top.png'))
twitter_icon   = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/youporn/twitter.png'))
viewed_icon    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/youporn/viewed.png'))
HISTORY_FILE   = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'history.xml'))
FAVOURITES_FILE= xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'favourites.xml'))
DOWNLOADS_FILE = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'downloads.xml'))
DATA_FOLDER    = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id))
SEARCH_FILE    = xbmc.translatePath(os.path.join(DATA_FOLDER , 'search.xml'))

NEW_VIDS       = 'http://www.youporn.com/'
TOP_VIDS       = 'http://www.youporn.com/top_rated/'
MOST_FAV       = 'http://www.youporn.com/most_favorited/'
MOST_VIEW      = 'http://www.youporn.com/most_viewed/'
MOST_DIS       = 'http://www.youporn.com/most_discussed/'

def MAIN_MENU():

	common.addDir("[COLOR red][B]SEARCH[/B][/COLOR]","url",74,search_icon,fanart)
	common.addDir("[COLOR pink][I]New Videos[/I][/COLOR]",NEW_VIDS,71,new_icon,fanart)
	common.addDir("[COLOR pink][I]Top Rated[/I][/COLOR]",TOP_VIDS,71,top_icon,fanart)
	common.addDir("[COLOR pink][I]Most Viewed[/I][/COLOR]",MOST_VIEW,71,viewed_icon,fanart)
	common.addDir("[COLOR pink][I]Most Favourited[/I][/COLOR]",MOST_FAV,71,fav_icon,fanart)
	common.addDir("[COLOR pink][I]Most Discussed[/I][/COLOR]",MOST_DIS,71,discussed_icon,fanart)

	result = common.open_url('http://www.youporn.com/categories')
	
	match = re.compile("id='categoryList'>(.+?)<div class='title-bar sixteen-column'>",re.DOTALL).findall(result)
	string = str(match)
	match2 = re.compile("<a h(.+?)</p>",re.DOTALL).findall(string)
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
		name = "[COLOR white]" + title + " - " + number + "[/COLOR]"
		common.addDir(name,url,71,icon_cat,fanart)
		
	try:
		common.addDir("[COLOR red]Total Videos: {:,}".format(videos) + "[/COLOR]",NEW_VIDS,71,icon,fanart)
	except:
		try:
			common.addDir("[COLOR red]Total Videos: " + str(videos) + "[/COLOR]",NEW_VIDS,71,icon,fanart)
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
	match = re.compile('video-box four-column(.+?)<div class="video-box-title">',re.DOTALL).findall(result)
	for item in match:
		try:
			title=re.compile("alt=(.+?)'").findall(item)[0]
			url=re.compile('<a href="(.+?)"').findall(item)[0]
			iconimage=re.compile('<img src="(.+?)"').findall(item)[0]
			if "icon-hd-text" in item:
				name = "[COLOR orangered]HD[/COLOR][COLOR white] - " + title + "[/COLOR]"
			else:
				name = "[COLOR yellow]SD[/COLOR][COLOR white] - " + title + "[/COLOR]"
			name = name.replace("'",'')
			name = common.CLEANUP(name)
			url2 = name + '|SPLIT|' + url + '|SPLIT|' + iconimage 
			common.addLink(name,url2,73,iconimage,iconimage)
		except: pass
	
	if nextpage == 1:
		try:
			np=re.compile('<li class="current"(.+?)<div id="next">',re.DOTALL).findall(result)
			for item in np:
				current=re.compile('<div class="currentPage" data-page-number=".+?">(.+?)</div>').findall(item)[0]
				url=re.compile('<a href="(.+?)=').findall(item)[0]
				next = int(float(current)) + 1
				url = "http://youporn.com" + str(url) + "=" + str(next)
				common.addDir('[COLOR pink]Next Page >>[/COLOR]',url,71,next_icon,fanart)       
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
		url = "72"
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
				url = "http://www.youporn.com/search/?query=" + string.lower()
				GET_CONTENT(url)
			else: quit()
	else:
		string = url.replace(' ','+')
		url = "http://www.youporn.com/search/?query=" + string.lower()
		GET_CONTENT(url)

def PLAY_URL(name,url,iconimage):

	name,url,iconimage = url.split('|SPLIT|')
	name = name.replace("[COLOR orangered]HD[/COLOR][COLOR white] - ",'').replace("[COLOR yellow]SD[/COLOR][COLOR white] - ",'').replace('[/COLOR]','').replace(' - ','')
	dp = common.GET_LUCKY()
	url = "http://www.youporn.com" + url
	ref_url = url
	result = common.open_url(url)
	match = re.compile('sources: {(.+?)}',re.DOTALL).findall(result)
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

	url = url_play
	
	choice = dialog.select("[COLOR red]Please select an option[/COLOR]", ['[COLOR pink]Watch Video[/COLOR]','[COLOR pink]Add to Favourites[/COLOR]','[COLOR pink]Download Video[/COLOR]'])

	if choice == 1:
		a=open(FAVOURITES_FILE).read()
		b=a.replace('#START OF FILE#', '#START OF FILE#\n<item>\n<name>'+str(name)+'</name>\n<link>'+str(url)+'</link>\n<site>YouPorn</site>\n<icon>'+str(iconimage)+'</icon>\n</item>\n')
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
			b=a.replace('#START OF FILE#', '#START OF FILE#\n<item>\n<date>'+str(date_now)+'</date>\n<time>'+str(time_now)+'</time>\n<name>'+str(name)+'</name>\n<link>'+str(url)+'</link>\n<site>YouPorn</site>\n<icon>'+str(iconimage)+'</icon>\n</item>\n')
			f= open(HISTORY_FILE, mode='w')
			f.write(str(b))
			f.close()

		url = url + '|User-Agent=Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36&Referer=' + ref_url
		liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
		dp.close()
		xbmc.Player ().play(url, liz, False)
	else:
		dp.close()
		quit()
