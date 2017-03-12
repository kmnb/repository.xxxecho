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
import re
from resources.lib.modules  import common
from resources.lib.modules  import plugintools
import datetime

#Default veriables
AddonTitle     = "[COLOR red]XXX-O-DUS[/COLOR]"
dialog         = xbmcgui.Dialog()
addon_id       = 'plugin.video.xxx-o-dus'
fanart         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/motherless/fanart.jpg'))
icon           = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/motherless/icon.png'))
BASE_VIDEOS    = 'http://motherless.com/videos'
BASE_IMAGE     = 'http://motherless.com/images'
HISTORY_FILE   = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'history.xml'))
FAVOURITES_FILE= xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'favourites.xml'))
DATA_FOLDER    = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id))
SEARCH_FILE    = xbmc.translatePath(os.path.join(DATA_FOLDER , 'search.xml'))

def MAIN_MENU():

	common.addDir("[COLOR red][B]SEARCH[/B][/COLOR]","url",97,icon,fanart)

	link = common.open_url(BASE_VIDEOS).replace('\n','').replace('\r','')

	match=re.compile('<div class="sub_menu dark-menu">(.+?)</div>').findall(link)[0]
	match2=re.compile('<a(.+?)/a>').findall(match)

	for items in match2:
		name=re.compile('href=.+?>(.+?)<').findall(items)[0]
		url=re.compile('href="(.+?)"').findall(items)[0]
		url = "http://motherless.com" + url
		common.addDir('[COLOR white]' + name + '[/COLOR]',url,94,icon,fanart)

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
    
    link = common.open_url(url).replace('\n','').replace('\r','')
    match=re.compile('<div class="thumb video medium"(.+?)<div class="clear').findall(link)
    for links in match:
        url=re.compile('<a href="(.+?)"',re.DOTALL).findall(links)[0]
        name=re.compile('<h2 class="caption title">(.+?)</h2>',re.DOTALL).findall(links)[0].replace('.mp4', '').replace('.flv', '').replace('.wmv', '').replace('.avi', '')
        duration=re.compile('<div class="caption left">(.+?)</div>',re.DOTALL).findall(links)[0]
        iconimage=re.compile('<img class="static" src="(.+?)"',re.DOTALL).findall(links)[0].replace('?from_helper', '')
        name = common.CLEANUP(name)
        url2 = name + "|SPLIT|" + url
        if not "files" in duration.lower():
            common.addLink("[COLOR white]" + name + "[/COLOR] - [COLOR pink]" + duration + "[/COLOR]",url2,96,iconimage,fanart)

    if nextpage == 1:
        try:
            np=re.compile('<a href="([^"]*)" class="pop" rel=".+?">NEXT').findall(link)[0]
            np = np.replace('&amp;','&')
            np = 'http://motherless.com' + np
            common.addDir('[COLOR yellow]Next Page >>[/COLOR]',np,94,icon,fanart)       
        except:pass

def SEARCH_DECIDE():

	search_on_off  = plugintools.get_setting("search_setting")
	if search_on_off == "true":
		name = "null"
		url = "95"
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
			string = keyboard.getText().replace(' ','%20')
			if len(string)>1:
				url = "http://motherless.com/term/" + string.lower()
				GET_CONTENT(url)
			else: quit()
	else:
		string = url.replace(' ','%20')
		url = "http://motherless.com/term/" + string.lower()
		GET_CONTENT(url)

def MAIN_MENU_PICTURES():

	result = common.open_url(BASE_IMAGE)
	
	match = re.compile('<div class="sub_menu dark-menu">(.+?)<a class="feed-link medium"',re.DOTALL).findall(result)
	string = str(match)
	match2 = re.compile("<a(.+?)/a>",re.DOTALL).findall(string)

	for item in match2:
		url=re.compile('href="(.+?)" title=".+?">.+?<').findall(item)[0]
		name=re.compile('href=".+?" title=".+?">(.+?)<').findall(item)[0]
		url = "http://www.motherless.com" + url
		name = "[COLOR white]" + name + "[/COLOR]"
		common.addDir(name,url,91,icon,fanart)

	kodi_name = common.GET_KODI_VERSION()

	if kodi_name == "Jarvis":
		xbmc.executebuiltin('Container.SetViewMode(50)')
	elif kodi_name == "Krypton":
		xbmc.executebuiltin('Container.SetViewMode(55)')
	else: xbmc.executebuiltin('Container.SetViewMode(50)')

def GET_CONTENT_PICTURES(url):

	checker = url
	result = common.open_url(url)
	match = re.compile('<div class="content-inner">(.+?)</html>',re.DOTALL).findall(result)
	string = str(match)
	match2 = re.compile('<div class="thumb-container(.+?)<div class="clear:both;">',re.DOTALL).findall(string)
	for item in match2:
		try:
			title=re.compile('<h2 class="caption title">(.+?)</h2>').findall(item)[0]
			url=re.compile('<a href="(.+?)"').findall(item)[0]
			iconimage=re.compile('<img class="static" src="(.+?)"').findall(item)[0]
			hits=re.compile('<div class="caption right">(.+?)</div>').findall(item)[0]
			date=re.compile('<div class="caption right">(.+?)</div>').findall(item)[1]
			title = common.CLEANUP(title)
			name = title + ' - ' + hits + ' | ' + date
			common.addLink(name,url,92,iconimage,fanart)
		except: pass

	try:
		next=re.compile('<a href="([^"]*)" class="pop".+?>NEXT').findall(result)[0]
		url = "http://motherless.com" + str(next)
		common.addDir('[COLOR orangered]Next Page >>[/COLOR]',url,91,icon,fanart)       
	except:pass

	kodi_name = common.GET_KODI_VERSION()

	if kodi_name == "Jarvis":
		xbmc.executebuiltin('Container.SetViewMode(500)')
	elif kodi_name == "Krypton":
		xbmc.executebuiltin('Container.SetViewMode(52)')
	else: xbmc.executebuiltin('Container.SetViewMode(500)')

def DISPLAY_PICTURE(url):

	result = common.open_url(url)
	match = re.compile('<link rel="image_src".+?href="(.+?)">',re.DOTALL).findall(result)[0]

	SHOW = "ShowPicture(" + match + ')'
	xbmc.executebuiltin(SHOW)
		
def PLAY_URL(name,url,iconimage):
	
	name,url = url.split('|SPLIT|')
	name = name.replace('[COLOR white]','').replace('[/COLOR]','').replace(' - ','')
	dp = common.GET_LUCKY()
	result = common.open_url(url)
	url = re.compile("fileurl.+?'(.+?)';",re.DOTALL).findall(result)[0]
	url = url.replace("?fs=opencloud",'').replace("']",'').replace('%3A%2F%2F','://').replace('%2F','/')

	choice = dialog.select("[COLOR red]Please select an option[/COLOR]", ['[COLOR pink]Watch Video[/COLOR]','[COLOR pink]Add to Favourites[/COLOR]','[COLOR pink]Download Video[/COLOR]'])

	if choice == 1:
		a=open(FAVOURITES_FILE).read()
		b=a.replace('#START OF FILE#', '#START OF FILE#\n<item>\n<name>'+str(name)+'</name>\n<link>'+str(url)+'</link>\n<site>Motherless</site>\n<icon>'+str(iconimage)+'</icon>\n</item>\n')
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
			b=a.replace('#START OF FILE#', '#START OF FILE#\n<item>\n<date>'+str(date_now)+'</date>\n<time>'+str(time_now)+'</time>\n<name>'+str(name)+'</name>\n<link>'+str(url)+'</link>\n<site>Motherless</site>\n<icon>'+str(iconimage)+'</icon>\n</item>\n')
			f= open(HISTORY_FILE, mode='w')
			f.write(str(b))
			f.close()

		url = url + '|User-Agent=Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
		liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
		dp.close()
		xbmc.Player ().play(url, liz, False)
	else:
		dp.close()
		quit()
