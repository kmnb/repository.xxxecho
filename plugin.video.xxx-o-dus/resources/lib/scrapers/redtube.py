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
AddonTitle        = "[COLOR red]XXX-O-DUS[/COLOR]"
dialog            = xbmcgui.Dialog()
addon_id          = 'plugin.video.xxx-o-dus'
fanart            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'resources/art/redtube/fanart.jpg'))
icon              = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/redtube/icon.png'))
next_icon         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/redtube/next.png'))
search_icon       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/redtube/search.png'))
discussed_icon    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/redtube/discussed.png'))
fav_icon          = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/redtube/fav.png'))
new_icon          = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/redtube/new.png'))
pc_icon           = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/redtube/pc.png'))
top_icon          = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/redtube/top.png'))
twitter_icon      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/redtube/twitter.png'))
viewed_icon       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/redtube/viewed.png'))
HISTORY_FILE      = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'history.xml'))
FAVOURITES_FILE   = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'favourites.xml'))
DOWNLOADS_FILE    = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'downloads.xml'))
DATA_FOLDER       = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id))
SEARCH_FILE       = xbmc.translatePath(os.path.join(DATA_FOLDER , 'search.xml'))

NEW_VIDS       = 'http://www.redtube.com/'
TOP_VIDS       = 'http://www.redtube.com/top/'
MOST_FAV       = 'http://www.redtube.com/mostfavored/'
MOST_VIEW      = 'http://www.redtube.com/mostviewed/'
RECOM          = 'http://www.redtube.com/recommended/'

def MAIN_MENU():

	common.addDir("[COLOR red][B]SEARCH[/B][/COLOR]","url",45,search_icon,fanart)
	common.addDir("[COLOR pink][I]Newest[/I][/COLOR]",NEW_VIDS,42,new_icon,fanart)
	common.addDir("[COLOR pink][I]Recommended[/I][/COLOR]",RECOM,42,discussed_icon,fanart)
	common.addDir("[COLOR pink][I]Top Rated[/I][/COLOR]",TOP_VIDS,42,top_icon,fanart)
	common.addDir("[COLOR pink][I]Most Viewed[/I][/COLOR]",MOST_VIEW,42,viewed_icon,fanart)
	common.addDir("[COLOR pink][I]Most Favourited[/I][/COLOR]",MOST_FAV,42,fav_icon,fanart)

	result = common.open_url('http://www.redtube.com/categories')
	
	match = re.compile('<div class="content channelsPage">(.+?)<div class="footerWrapper">',re.DOTALL).findall(result)
	string = str(match)
	match2 = re.compile('<div class="video">(.+?)</li>',re.DOTALL).findall(string)
	fail = 0
	videos = 0
	for item in match2:
		url=re.compile('<a title=".+?" href="(.+?)">').findall(item)[0]
		title=re.compile('<a title="(.+?)" href=".+?">').findall(item)[0]
		icon_cat=re.compile('data-src="(.+?)"').findall(item)[0]
		a = str(icon_cat)
		icon_cat = "http:" + a
		number=re.compile('<p class="numberVideos">(.+?) V').findall(item)[0]
		b = str(number)
		c = b.replace(',','').replace(' Videos','').replace('\\n','').replace('\\r','').replace('\\t','').replace('\n','').replace('\r','').replace('\t','')
		videos = videos + int(float(c))
		url3 = url
		url4 = url3.replace('\\','')
		url = "http://www.redtube.com" + url4
		name = "[COLOR white]" + title + " [COLOR white] - " + c + " Videos[/COLOR]"
		name = common.CLEANUP(name)
		common.addDir(name,url,42,icon_cat,fanart)
		
	try:
		common.addDir("[COLOR white]Total Videos: [COLOR white]{:,}".format(videos) + "[/COLOR]",NEW_VIDS,42,icon,fanart)
	except:
		try:
			common.addDir("[COLOR white]Total Videos: [COLOR white]" + str(videos) + "[/COLOR]",NEW_VIDS,42,icon,fanart)
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
	match = re.compile('class="video-listing two-in-row(.+?)<div class="pages">',re.DOTALL).findall(result)
	string = str(match)
	match2 = re.compile('<li(.+?)</li>',re.DOTALL).findall(string)
	for item in match2:
		try:
			title=re.compile('<a href=".+?" title="(.+?)" class=".+?" >').findall(item)[0]
			url=re.compile('<a href="(.+?)" title=".+?" class=".+?" >').findall(item)[0]
			rating=re.compile('<span class="video-percent">(.+?)</span>').findall(item)[0]
			video_views=re.compile('<span class="video-views">(.+?)</span>').findall(item)[0]
			iconimage=re.compile('data-src="(.+?)"').findall(item)[0]
			icon = "http:" + iconimage
			url = "http://www.redtube.com" + str(url)
			percent = "[COLOR red]" + rating + "[/COLOR]"
			name = "[COLOR white] - " + title + "[/COLOR]"
			views = "[COLOR grey] | [I]" + video_views + " Views[/I][/COLOR]"
			name = common.CLEANUP(name)
			url2 = name + '|SPLIT|' + url + '|SPLIT|' + icon
			common.addLink(percent + name + views,url2,44,icon,fanart)
		except: pass

	if nextpage == 1:
		try:
			np=re.compile('<link rel="next" href="(.+?)"').findall(result)[0]
			common.addDir('[COLOR white]Next Page >>[/COLOR]',np,42,next_icon,fanart)       
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
		url = "43"
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
				url = "http://www.redtube.com/?search=" + string.lower()
				GET_CONTENT(url)
			else: quit()
	else:
		string = url.replace(' ','+')
		url = "http://www.redtube.com/?search=" + string.lower()
		GET_CONTENT(url)

def PLAY_URL(name,url,iconimage):

	name,url,iconimage = url.split('|SPLIT|')
	name = name.replace('[COLOR white]','').replace('[/COLOR]','').replace(' - ','')
	ref_url = url
	dp = common.GET_LUCKY()
	result = common.open_url(url)
	url = re.compile('<source src="//(.+?)" type="video/mp4">',re.DOTALL).findall(result)
	a = str(url)
	url = 'http://' + str(a)
	url = url.replace("['",'').replace("']",'').replace('%3A%2F%2F','://').replace('%2F','/').replace('amp;','')

	choice = dialog.select("[COLOR red]Please select an option[/COLOR]", ['[COLOR pink]Watch Video[/COLOR]','[COLOR pink]Add to Favourites[/COLOR]','[COLOR pink]Download Video[/COLOR]'])

	if choice == 1:
		a=open(FAVOURITES_FILE).read()
		b=a.replace('#START OF FILE#', '#START OF FILE#\n<item>\n<name>'+str(name)+'</name>\n<link>'+str(url)+'</link>\n<site>RedTube</site>\n<icon>'+str(iconimage)+'</icon>\n</item>\n')
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
			b=a.replace('#START OF FILE#', '#START OF FILE#\n<item>\n<date>'+str(date_now)+'</date>\n<time>'+str(time_now)+'</time>\n<name>'+str(name)+'</name>\n<link>'+str(url)+'</link>\n<site>RedTube</site>\n<icon>'+str(iconimage)+'</icon>\n</item>\n')
			f= open(HISTORY_FILE, mode='w')
			f.write(str(b))
			f.close()

		url = url + '|User-Agent=Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36&Referer=' + ref_url
		liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
		dp.close()
		xbmc.Player ().play(url, liz, False)
		quit()
	else:
		dp.close()
		quit()