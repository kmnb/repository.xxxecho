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
from resources.lib.modules  import plugintools
from resources.lib.modules  import downloader
import datetime

#Default veriables
AddonTitle       = "[COLOR red]XXX-O-DUS[/COLOR]"
addon_id         = 'plugin.video.xxx-o-dus'
dialog           = xbmcgui.Dialog()
fanart           = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/xhamster/fanart.jpg'))
icon             = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/xhamster/icon.png'))
HISTORY_FILE     = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'history.xml'))
FAVOURITES_FILE  = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'favourites.xml'))
DOWNLOADS_FILE   = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'downloads.xml'))
DATA_FOLDER      = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id))
SEARCH_FILE      = xbmc.translatePath(os.path.join(DATA_FOLDER , 'search.xml'))

NEW_VIDS       = 'https://xhamster.com/last50.php'
TOP_VIDS       = 'https://xhamster.com/rankings/weekly-top-videos.html'
MOST_COM       = 'https://xhamster.com/rankings/weekly-top-commented.html'
MOST_VIEW      = 'https://xhamster.com/rankings/weekly-top-viewed.html'

def MAIN_MENU():

	common.addDir("[COLOR red][B]SEARCH[/B][/COLOR]","url",14,icon,fanart)
	common.addDir("[COLOR pink][I]50 Newest Videos[/I][/COLOR]",NEW_VIDS,11,icon,fanart)
	common.addDir("[COLOR pink][I]Top Rated[/I][/COLOR]",TOP_VIDS,11,icon,fanart)
	common.addDir("[COLOR pink][I]Most Viewed[/I][/COLOR]",MOST_VIEW,11,icon,fanart)
	common.addDir("[COLOR pink][I]Most Commented[/I][/COLOR]",MOST_COM,11,icon,fanart)

	result = common.open_url('https://www.xhamster.com')
	match = re.compile('<div class="head" data-block="channels-straight">(.+?)<a href="https://xhamster.com/channels.php" class="bottom">',re.DOTALL).findall(result)
	string = str(match)
	match2 = re.compile('<a(.+?)/a>',re.DOTALL).findall(string)
	fail = 0
	videos = 0
	for item in match2:
		try:
			title=re.compile('href=".+?">(.+?)<').findall(item)[0]
			url=re.compile('href="(.+?)">.+?<').findall(item)[0]
			name = "[COLOR white]" + title + "[/COLOR]"
			name = common.CLEANUP(name)
			if not "<" in name:
				common.addDir(name,url,11,icon,fanart)
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
	if '<div id="searchLoader">' in result:
		match = re.compile('<div id="searchLoader">(.+?)iconPagerNextHover',re.DOTALL).findall(result)
	elif 'last50.php' in url:
		match = re.compile('href="/last50.php">(.+?)<div id="footer">',re.DOTALL).findall(result)
	elif '<div class="video new-date">' in result:
		match = re.compile('<div class="video new-date">(.+?)<div class="category-related-container">',re.DOTALL).findall(result)
	else:
		match = re.compile("id='vListTop'>(.+?)<div class='pager'>",re.DOTALL).findall(result)

	string = str(match)
	match2 = re.compile('<a(.+?)<div class="video">',re.DOTALL).findall(string)
	
	for item in match2:
		try:
			title=re.compile('alt="(.+?)"').findall(item)[0]
			url=re.compile('href="(.+?)"').findall(item)[0]
			rating=re.compile('<div class="fr">(.+?)</div>').findall(item)[0]
			duration=re.compile('<b>(.+?)</b>').findall(item)[0]
			try:
				vid_views=re.compile('<div class="views-value">(.+?)</div>').findall(item)[0]
			except: vid_views = "Unknown"
			try:
				iconimage=re.compile("<img src=(.+?) class").findall(item)[0]
				iconimage = iconimage.replace('\\','').replace("'",'')
			except: iconimage = "null"
			percent = "[COLOR red]" + rating + "[/COLOR]"
			name = "[COLOR white] - " + title + "[/COLOR]"
			length = "[COLOR grey] | [I]Length: " + duration + "[/I][/COLOR]"
			views = "[COLOR grey] | [I]Views: " + vid_views + "[/I][/COLOR]"
			url = url + "&Referer=" + checker
			name = common.CLEANUP(name)
			url2 = name + "|SPLIT|" + url
			common.addLink(percent + name + length + views,url2,13,iconimage,fanart)
		except: pass

	if nextpage == 1:
		try:
			if "class='last' overicon='iconPagerNextHover'>" in result:
				np=re.compile("<a href='([^']*)' class='last' overicon='iconPagerNextHover'>").findall(result)[0]
			else:
				np=re.compile('<link rel="next" href="(.+?)"').findall(result)[0]
			np = np.replace('&amp;','&')
			common.addDir('[COLOR white]Next Page >>[/COLOR]',np,11,icon,fanart)       
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
		url = "12"
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
				url = "https://xhamster.com/search.php?from=&new=&q=" + string.lower() + "&qcat=video"
				GET_CONTENT(url)
			else: quit()
	else:
		string = url.replace(' ','+')
		url = "https://xhamster.com/search.php?from=&new=&q=" + string.lower() + "&qcat=video"
		GET_CONTENT(url)

def PLAY_URL(name,url,iconimage):
	
	name,url = url.split('|SPLIT|')
	name = name.replace('[COLOR white]','').replace('[/COLOR]','').replace(' - ','')
	ref_url = url.split("&Referer")[0]
	dp = common.GET_LUCKY()
	result = common.open_url(url)
	url = re.compile("file: '(.+?)'",re.DOTALL).findall(result)[0]
	url = url.replace("['",'').replace("']",'').replace('%3A%2F%2F','://').replace('%2F','/')

	choice = dialog.select("[COLOR red]Please select an option[/COLOR]", ['[COLOR pink]Watch Video[/COLOR]','[COLOR pink]Add to Favourites[/COLOR]','[COLOR pink]Download Video[/COLOR]'])

	if choice == 1:
		a=open(FAVOURITES_FILE).read()
		b=a.replace('#START OF FILE#', '#START OF FILE#\n<item>\n<name>'+str(name)+'</name>\n<link>'+str(url)+'</link>\n<site>Xhamster</site>\n<icon>'+str(iconimage)+'</icon>\n</item>\n')
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
			b=a.replace('#START OF FILE#', '#START OF FILE#\n<item>\n<date>'+str(date_now)+'</date>\n<time>'+str(time_now)+'</time>\n<name>'+str(name)+'</name>\n<link>'+str(url)+'</link>\n<site>Xhamster</site>\n<icon>'+str(iconimage)+'</icon>\n</item>\n')
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