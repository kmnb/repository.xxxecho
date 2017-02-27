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
fanart         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/spankbang/fanart.jpg'))
icon           = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/spankbang/icon.png'))
HISTORY_FILE   = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'history.xml'))
FAVOURITES_FILE= xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'favourites.xml'))
DOWNLOADS_FILE = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'downloads.xml'))
DATA_FOLDER    = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id))
SEARCH_FILE    = xbmc.translatePath(os.path.join(DATA_FOLDER , 'search.xml'))

TRENDING_URL   = 'http://spankbang.com/trending_videos/'
NEW_URL        = 'http://spankbang.com/new_videos/'
MOST_POP       = 'http://spankbang.com/most_popular/'
MOST_LIKE      = 'http://spankbang.com/top_rated/'

def MAIN_MENU():

	common.addDir("[COLOR red][B]SEARCH[/B][/COLOR]","url",205,icon,fanart)
	common.addDir("[COLOR pink][I]Trending[/I][/COLOR]",TRENDING_URL,202,icon,fanart)
	common.addDir("[COLOR pink][I]New[/I][/COLOR]",NEW_URL,202,icon,fanart)
	common.addDir("[COLOR pink][I]Most Popular[/I][/COLOR]",MOST_POP,201,icon,fanart)
	common.addDir("[COLOR pink][I]Most Liked[/I][/COLOR]",MOST_LIKE,201,icon,fanart)

	result = common.open_url('http://spankbang.com/categories')
	
	match = re.compile('<div class="categories">(.+?)</div>',re.DOTALL).findall(result)
	string = str(match)
	match2 = re.compile("<a h(.+?)</a>",re.DOTALL).findall(string)

	for item in match2:
		url=re.compile('ref="(.+?)"').findall(item)[0]
		title=re.compile('<span>(.+?)</span>').findall(item)[0]
		icon_cat=re.compile('src="(.+?)"').findall(item)[0]
		icon_cat = 'http://spankbang.com' + icon_cat
		url = 'http://spankbang.com' + url
		name = "[COLOR white]" + title + "[/COLOR]"
		common.addDir(name,url,202,icon_cat,fanart)

	kodi_name = common.GET_KODI_VERSION()

	if kodi_name == "Jarvis":
		xbmc.executebuiltin('Container.SetViewMode(50)')
	elif kodi_name == "Krypton":
		xbmc.executebuiltin('Container.SetViewMode(55)')
	else: xbmc.executebuiltin('Container.SetViewMode(50)')

def SUB_MENU(url):

	common.addDir("[COLOR pink][I]Today[/I][/COLOR]",url + '?period=today',202,icon,fanart)
	common.addDir("[COLOR pink][I]This Week[/I][/COLOR]",url + '?period=week',202,icon,fanart)
	common.addDir("[COLOR pink][I]This Month[/I][/COLOR]",url + '?period=month',202,icon,fanart)
	common.addDir("[COLOR pink][I]Three Months[/I][/COLOR]",url + '?period=season',202,icon,fanart)
	common.addDir("[COLOR pink][I]This Year[/I][/COLOR]",url + '?period=year',202,icon,fanart)

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
	match = re.compile('<div class="video-item"(.+?)</div>',re.DOTALL).findall(result)
	for item in match:
		title=re.compile('<img src=".+?" alt="(.+?)"').findall(item)[0]
		url=re.compile('<a href="(.+?)" class="thumb">').findall(item)[0]
		iconimage=re.compile('<img src="(.+?)"').findall(item)[0]
		uploaded=re.compile('<li>(.+?)</li>').findall(item)[0]
		views=re.compile('<li><i class="fa fa-eye"></i>(.+?)</li>').findall(item)[0]
		rating=re.compile('<li><i class="fa fa-thumbs-o-up"></i>(.+?)</li>').findall(item)[0]
		iconimage = 'http://' + iconimage
		url = 'http://spankbang.com' + url
		title = common.CLEANUP(title)
		url2 = title + '|SPLIT|' + url
		name = '[COLOR red][B]' + rating + '[/B][/COLOR] - ' + title + ' - ' + uploaded + ' |' + views + ' Views'
		common.addLink(name,url2,204,iconimage,iconimage)
	
	if nextpage == 1:
		try:
			np=re.compile('<link rel="next" href="(.+?)" />',re.DOTALL).findall(result)[0]
			common.addDir('[COLOR pink]Next Page >>[/COLOR]',np,202,icon,fanart)       
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
		url = "203"
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
				url = "http://spankbang.com/s/" + string.lower()
				GET_CONTENT(url)
			else: quit()
	else:
		string = url.replace(' ','+')
		url = "http://spankbang.com/s/" + string.lower()
		GET_CONTENT(url)

def PLAY_URL(name,url,iconimage):

	name,url = url.split('|SPLIT|')
	dp = common.GET_LUCKY()
	ref_url = url
	result = common.open_url(url)
	match = re.compile('<source src="(.+?)"',re.DOTALL).findall(result)[0]
	url = 'http://spankbang.com' + match
		
	choice = dialog.select("[COLOR red]Please select an option[/COLOR]", ['[COLOR pink]Watch Video[/COLOR]','[COLOR pink]Add to Favourites[/COLOR]','[COLOR pink]Download Video[/COLOR]'])

	if choice == 1:
		a=open(FAVOURITES_FILE).read()
		b=a.replace('#START OF FILE#', '#START OF FILE#\n<item>\n<name>'+str(name)+'</name>\n<link>'+str(url)+'</link>\n<site>Spankbang</site>\n<icon>'+str(iconimage)+'</icon>\n</item>\n')
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
			b=a.replace('#START OF FILE#', '#START OF FILE#\n<item>\n<date>'+str(date_now)+'</date>\n<time>'+str(time_now)+'</time>\n<name>'+str(name)+'</name>\n<link>'+str(url)+'</link>\n<site>Spankbang</site>\n<icon>'+str(iconimage)+'</icon>\n</item>\n')
			f= open(HISTORY_FILE, mode='w')
			f.write(str(b))
			f.close()

		url = url + '|User-Agent=Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.220203.207 Safari/537.36&Referer=' + ref_url
		liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
		dp.close()
		xbmc.Player ().play(url, liz, False)
	else:
		dp.close()
		quit()
