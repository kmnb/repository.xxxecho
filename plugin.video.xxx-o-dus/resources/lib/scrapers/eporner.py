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
fanart            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'resources/art/eporner/fanart.jpg'))
icon              = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/eporner/icon.png'))
HISTORY_FILE      = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'history.xml'))
FAVOURITES_FILE   = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'favourites.xml'))
DOWNLOADS_FILE    = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'downloads.xml'))
DATA_FOLDER       = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id))
SEARCH_FILE       = xbmc.translatePath(os.path.join(DATA_FOLDER , 'search.xml'))

def MAIN_MENU():

	common.addDir("[COLOR red][B]SEARCH[/B][/COLOR]","url",244,icon,fanart)

	try:
		link = common.open_url('https://www.eporner.com/0/').replace('/n','')
	except:
		dialog.ok(AddonTitle, "Error connecting to website. Please try again.")
		quit()
		
	match=re.compile('<div id="categories-list-left">(.+?)<div class="clear">',re.DOTALL).findall(link)[0]
	match2=re.compile('<a(.+?)/div></div>').findall(match)
	for links in match2:
		name=re.compile('href=".+?"><strong>(.+?)</strong></a> <div class="cllnumber">',re.DOTALL).findall(links)[0]
		url=re.compile('href="(.+?)".+?<strong>.+?</strong></a> <div class="cllnumber">',re.DOTALL).findall(links)[0]
		vids=re.compile('<div class="cllnumber">\((.+?)\)<',re.DOTALL).findall(links)[0]
		url='https://www.eporner.com' + url
		common.addDir(name + " - " + vids + " videos",url,241,icon,fanart)

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
	try:
		link = common.open_url(url).replace('/n','').replace("'",'"')
	except:
		dialog.ok(AddonTitle, "Error connecting to website. Please try again.")
		quit()
	match=re.compile('<div class="mb(.+?)<div class="mbrate">',re.DOTALL).findall(link)
	for links in match:
			name=re.compile('<a href=".+?" title="(.+?)"',re.DOTALL).findall(links)[0]
			url=re.compile('<a href="(.+?)" title=".+?"',re.DOTALL).findall(links)[0]
			try:
				quality=re.compile('<div class="mvhdico"><span>(.+?)</span>',re.DOTALL).findall(links)[0]
			except: quality == "null"
			iconimage=re.compile('src="(.+?)"',re.DOTALL).findall(links)[0]
			name = common.CLEANUP(name)
			url='https://www.eporner.com' + url
			url = name + "|SPLIT|" + url + "|SPLIT|" + iconimage
			if not quality == "null":
				common.addLink("[COLOR pink]" + quality + "[/COLOR] - " + name,url,243,iconimage,fanart)
			else: common.addLink(name,url,243,iconimage,fanart)

	if nextpage == 1:
		try:
			try:
				np=re.compile('<a href=\'([^"]*).+?title=.+?ext page\'>').findall(link)[0]
			except:
				try:
					np=re.compile('<a href=\"([^"]*)\" title=\"Next page\">',re.DOTALL).findall(link)[0]
				except: pass
			np=np.replace("'","").replace('"','')
			np = 'https://www.eporner.com' + np
			common.addDir('[COLOR white]Next Page >>[/COLOR]',np,241,icon,fanart)       
		except: pass
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
		url = "242"
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
			string = keyboard.getText().replace(' ','-')
			if len(string)>1:
				url = "https://www.eporner.com/search/" + string.lower()
				GET_CONTENT(url)
			else: quit()
	else:
		string = url.replace(' ','-')
		url = "https://www.eporner.com/search/" + string.lower()
		GET_CONTENT(url)

def PLAY_URL(name,url,iconimage):

	name,url,iconimage = url.split('|SPLIT|')
	name = name.replace('[COLOR white]','').replace('[/COLOR]','').replace(' - ','')
	ref_url = url
	dp = common.GET_LUCKY()
	try:
		result = common.open_url(url).replace('/n','')
	except:
		dialog.ok(AddonTitle, "Error connecting to website. Please try again.")
		quit()
	links = re.compile('<a href="/dload(.+?)">Download.+?\((.+?)\)',re.DOTALL).findall(result)
	streamurl=[]
	streamquality=[]
	for url,quality in links:
		if not "<script>" in quality:
			streamurl.append(url)
			streamquality.append("[COLOR pink][B]" + quality + "[/B][/COLOR]")

	streamquality.reverse();
	select = dialog.select(name,streamquality)
	if select < 0:
		quit()
	else:
		url = "https://www.eporner.com/dload" + streamurl[select]
	#url = re.compile('<a href="([^"]*)">Download',re.DOTALL).findall(result)[-1]
	#url = 'https://www.eporner.com' + url
	url = url.replace("['",'').replace("']",'').replace('%3A%2F%2F','://').replace('%2F','/').replace('amp;','')
	choice = dialog.select("[COLOR red]Please select an option[/COLOR]", ['[COLOR pink]Watch Video[/COLOR]','[COLOR pink]Add to Favourites[/COLOR]','[COLOR pink]Download Video[/COLOR]'])

	if choice == 1:
		a=open(FAVOURITES_FILE).read()
		b=a.replace('#START OF FILE#', '#START OF FILE#\n<item>\n<name>'+str(name)+'</name>\n<link>'+str(url)+'</link>\n<site>Eporner</site>\n<icon>'+str(iconimage)+'</icon>\n</item>\n')
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
			b=a.replace('#START OF FILE#', '#START OF FILE#\n<item>\n<date>'+str(date_now)+'</date>\n<time>'+str(time_now)+'</time>\n<name>'+str(name)+'</name>\n<link>'+str(url)+'</link>\n<site>Eporner</site>\n<icon>'+str(iconimage)+'</icon>\n</item>\n')
			f= open(HISTORY_FILE, mode='w')
			f.write(str(b))
			f.close()

		url = url + '|User-Agent=Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
		liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
		dp.close()
		xbmc.Player ().play(url, liz, False)
		quit()
	else:
		dp.close()
		quit()