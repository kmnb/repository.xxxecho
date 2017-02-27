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
from resources.lib.modules  import downloader
from resources.lib.modules  import plugintools
import datetime

#Default veriables
AddonTitle       = "[COLOR red]XXX-O-DUS[/COLOR]"
addon_id         = 'plugin.video.xxx-o-dus'
dialog           = xbmcgui.Dialog()
fanart           = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/xnxx/fanart.jpg'))
icon             = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/xnxx/icon.png'))
next_icon        = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/xnxx/next.png'))
search_icon      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/xnxx/search.png'))
HISTORY_FILE     = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'history.xml'))
FAVOURITES_FILE  = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'favourites.xml'))
DOWNLOADS_FILE   = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'downloads.xml'))
DATA_FOLDER      = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id))
SEARCH_FILE      = xbmc.translatePath(os.path.join(DATA_FOLDER , 'search.xml'))

NEW_VIDS       = 'http://www.xnxx.com/new'
BEST_VIDS      = 'http://www.xnxx.com/best'
HOT_VIDS       = 'http://www.xnxx.com/hot'
HITS_VIDS      = 'http://www.xnxx.com/hits'
featured_url   = 'http://www.xnxx.com'

def MAIN_MENU():

				
	common.addDir("[COLOR red][B]SEARCH[/B][/COLOR]","url",29,search_icon,fanart)
	common.addDir("[COLOR pink][I]Featured Videos[/I][/COLOR]",featured_url,31,icon,fanart)
	common.addDir("[COLOR pink][I]New Videos[/I][/COLOR]",NEW_VIDS,31,icon,fanart)
	common.addDir("[COLOR pink][I]Hot Videos[/I][/COLOR]",HOT_VIDS,31,icon,fanart)
	common.addDir("[COLOR pink][I]Best of[/I][/COLOR]",BEST_VIDS,31,icon,fanart)
	common.addDir("[COLOR pink][I]Top Hits[/I][/COLOR]",HITS_VIDS,31,icon,fanart)
	common.addDir("[COLOR pink][I]Pictures[/I][/COLOR]",featured_url,34,icon,fanart)
	common.addDir("[COLOR pink][I]Stories[/I][/COLOR]",featured_url,38,icon,fanart)

	result = common.open_url('http://www.xnxx.com')
	
	match = re.compile('<div id="side-categories" class="mobile-hide">(.+?)<div id="content-ad-side" class="mobile-hide">',re.DOTALL).findall(result)
	string = str(match)
	match2 = re.compile('{(.+?)}',re.DOTALL).findall(string)

	for item in match2:
		title=re.compile('label":"(.+?)"').findall(item)[0]
		url=re.compile('"url":".+?/(.+?)"').findall(item)[0]
		url3 = url
		url4 = url3.replace('\\','')
		url = "http://www.xnxx.com/" + url4
		name = "[COLOR white]" + title + "[/COLOR]"
		common.addDir(name,url,31,icon,fanart)

	kodi_name = common.GET_KODI_VERSION()

	if kodi_name == "Jarvis":
		xbmc.executebuiltin('Container.SetViewMode(50)')
	elif kodi_name == "Krypton":
		xbmc.executebuiltin('Container.SetViewMode(55)')
	else: xbmc.executebuiltin('Container.SetViewMode(50)')
	
def PICTURE_MENU():
	
	result = common.open_url('http://multi.xnxx.com')
	
	match = re.compile('visible-md visible-sm " id="leftPanel">(.+?)<div class="row"><div  class="boxImg',re.DOTALL).findall(result)
	string = str(match)
	match2 = re.compile('<a hre(.+?)/a>',re.DOTALL).findall(string)

	for item in match2:
		title=re.compile('f=".+?" />(.+?)<').findall(item)[0]
		url=re.compile('f="(.+?)" />.+?<').findall(item)[0]
		url3 = url
		url4 = url3.replace('\\','')
		url = "http://multi.xnxx.com" + url4
		name = "[COLOR white]" + title.title() + "[/COLOR]"
		common.addDir(name,url,35,icon,fanart)

	kodi_name = common.GET_KODI_VERSION()

	if kodi_name == "Jarvis":
		xbmc.executebuiltin('Container.SetViewMode(50)')
	elif kodi_name == "Krypton":
		xbmc.executebuiltin('Container.SetViewMode(55)')
	else: xbmc.executebuiltin('Container.SetViewMode(50)')

def STORY_MENU():
	
	result = common.open_url('http://sexstories.com')
	
	match = re.compile('<div id="menu">.+?<h2>Genres</h2>(.+?)<div id="content">',re.DOTALL).findall(result)
	string = str(match)
	match2 = re.compile('<li>(.+?)</li>',re.DOTALL).findall(string)
	for item in match2:
		title=re.compile('<a href=".+?">(.+?)</a>').findall(item)[0]
		url=re.compile('<a href="(.+?)">.+?</a>').findall(item)[0]
		url3 = url
		url4 = url3.replace('\\','')
		url = "http://www.sexstories.com" + url4
		name = "[COLOR white]" + title + "[/COLOR]"
		common.addDir(name,url,39,icon,fanart)

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
	match = re.compile('<div id="video(.+?)</p></div>',re.DOTALL).findall(result)
	for item in match:
		title=re.compile('title=(.+?)">').findall(item)[0]
		try:
			res=re.compile('<span class="video-hd-mark">(.+?)</span>').findall(item)[0]
		except:
			res= 'SD'
			pass
		if str(res) == "HD":
			resolution = "[COLOR orangered]" + str(res) + "[/COLOR] - "
		else:
			resolution = "[COLOR yellow]" + str(res) + "[/COLOR] - "
		url=re.compile('<a href="(.+?)"').findall(item)[0]
		iconimage=re.compile('<img src="(.+?)"').findall(item)[0]
		iconimage = iconimage.replace("THUMBNUM","5")
		name = "[COLOR white]" + title + "[/COLOR]"
		name = name.replace('"','')
		name = common.CLEANUP(name)
		url2 = name + '|SPLIT|' + url
		common.addLink(resolution + name,url2,33,iconimage,iconimage)

	if nextpage == 1:
		try:
			np=re.compile('<a href="([^"]*)" class="no-page">Next</a></li></ul></div>').findall(result)[0]
			np = np.replace('&amp;','&')
			np = 'http://www.xnxx.com' + np
			common.addDir('[COLOR yellow]Next Page >>[/COLOR]',np,31,next_icon,fanart)       
		except:pass

		if not "http://www.xnxx.com/home/10" in checker:
			if "/home/" in checker:
				a,b,c,d,e = checker.split('/')
				new = int(float(e)) + 1
				url = "http://www.xnxx.com/home/" + str(new)
				common.addDir('[COLOR yellow]Next Page >>[/COLOR]',url,31,next_icon,fanart)   
			elif checker == "http://www.xnxx.com":
				url = "http://www.xnxx.com/home/1"
				common.addDir('[COLOR yellow]Next Page >>[/COLOR]',url,31,next_icon,fanart)

	kodi_name = common.GET_KODI_VERSION()

	if kodi_name == "Jarvis":
		xbmc.executebuiltin('Container.SetViewMode(500)')
	elif kodi_name == "Krypton":
		xbmc.executebuiltin('Container.SetViewMode(52)')
	else: xbmc.executebuiltin('Container.SetViewMode(500)')

def PICTURE_CONTENT(url):
	
	result = common.open_url(url)
	
	match = re.compile('<div class="smallMargin"></div><div class="clearfix">(.+?)<div class="bigMargin"></div><div class="clearfix">',re.DOTALL).findall(result)
	string = str(match)
	match2 = re.compile('<div class="boxImg size_small home1 thumb"(.+?)</div></a></div>',re.DOTALL).findall(string)

	for item in match2:
		url=re.compile('<a href="(.+?)" target=').findall(item)[0]
		image=re.compile('d=".+?" src="(.+?)"').findall(item)[0]
		title=re.compile('<span class="descHome"><.+?>(.+?)<').findall(item)[0]
		url3 = url
		url4 = url3.replace('//','')
		url = "http://multi.xnxx.com" + url4
		name = "[COLOR white]" + title + "[/COLOR]"
		common.addDir(name,url,36,image,image)

	kodi_name = common.GET_KODI_VERSION()

	if kodi_name == "Jarvis":
		xbmc.executebuiltin('Container.SetViewMode(500)')
	elif kodi_name == "Krypton":
		xbmc.executebuiltin('Container.SetViewMode(52)')
	else: xbmc.executebuiltin('Container.SetViewMode(500)')

def LIST_STORIES(url):
	
	result = common.open_url(url)
	
	match = re.compile('<ul class="stories_list">(.+?)<div class="pager">',re.DOTALL).findall(result)
	string = str(match)
	match2 = re.compile('<h4>(.+?)</h4>',re.DOTALL).findall(string)

	for item in match2:
		title=re.compile('<a href=".+?">(.+?)</a>.+?tby').findall(item)[0]
		url=re.compile('<a href="(.+?)">.+?</a>.+?by').findall(item)[0]
		author=re.compile('by <a href=".+?">(.+?)</a>').findall(item)[0]
		url3 = url
		url4 = url3.replace('\\','')
		url = "http://www.sexstories.com" + url4
		title = common.CLEANUP(title)
		name = "[COLOR white]" + title + " by " + author +"[/COLOR]"
		common.addLink(name,url,40,icon,fanart)

	kodi_name = common.GET_KODI_VERSION()

	if kodi_name == "Jarvis":
		xbmc.executebuiltin('Container.SetViewMode(50)')
	elif kodi_name == "Krypton":
		xbmc.executebuiltin('Container.SetViewMode(55)')
	else: xbmc.executebuiltin('Container.SetViewMode(50)')

def DISPLAY_STORY(url):
	
	result = common.open_url(url)

	try:
		match = re.compile('<!-- CONTENT -->.+?<div (.+?)story_info">',re.DOTALL).findall(result)
		string = str(match)
		match2 = re.compile('class="block(.+?)ass="',re.DOTALL).findall(string)

		for item in match2:
			content=re.compile('_panel">(.+?)<div cl').findall(item)[0]
			display=str(content).replace('<!-- VOTES -->','')
			#a = common.strip_tags(display)
			a = common.CLEANUP(display)
			common.TextBoxes("%s" % a)
	except:
		dialog=xbmcgui.Dialog()
		dialog.ok('XNXX.com','There was an error processing the request. Please try another link.')

def SCRAPE_GALLERY(url):
	
	i = 0
	result = common.open_url(url)
	
	match = re.compile('<div class="row galleryPage GalleryBlock" id="Gallery">(.+?)</div><div class="sponsorLink">',re.DOTALL).findall(result)
	string = str(match)
	match2 = re.compile('<a class="picture"(.+?) data-id',re.DOTALL).findall(string)

	for item in match2:
		i = i + 1
		image=re.compile('href="(.+?)"').findall(item)[0]
		common.addLink("[COLOR white]Picture " + str(i) + "[/COLOR]",image,37,image,image)

	kodi_name = common.GET_KODI_VERSION()

	if kodi_name == "Jarvis":
		xbmc.executebuiltin('Container.SetViewMode(500)')
	elif kodi_name == "Krypton":
		xbmc.executebuiltin('Container.SetViewMode(52)')
	else: xbmc.executebuiltin('Container.SetViewMode(500)')

def DISPLAY_PICTURE(url):

    SHOW = "ShowPicture(" + url + ')'
    xbmc.executebuiltin(SHOW)

def SEARCH_DECIDE():

	search_on_off  = plugintools.get_setting("search_setting")
	if search_on_off == "true":
		name = "null"
		url = "32"
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
				url = "http://www.xnxx.com/?k=" + string.lower()
				GET_CONTENT(url)
			else: quit()
	else:
		string = url.replace(' ','+')
		url = "http://www.xnxx.com/?k=" + string.lower()
		GET_CONTENT(url)

def PLAY_URL(name,url,iconimage):

	name,url = url.split('|SPLIT|')
	name = name.replace('[COLOR white]','').replace('[/COLOR]','').replace(' - ','')
	dp = common.GET_LUCKY()
	url = "http://www.xnxx.com/" + url
	ref_url = url
	result = common.open_url(url)
	match = re.compile('<head>(.+?)</html>',re.DOTALL).findall(result)
	string = str(match).replace('\\','').replace('(','').replace(')','')
	url = re.compile("setVideoHLS'(.+?)'").findall(string)[0]

	choice = dialog.select("[COLOR red]Please select an option[/COLOR]", ['[COLOR pink]Watch Video[/COLOR]','[COLOR pink]Add to Favourites[/COLOR]'])

	if choice == 1:
		a=open(FAVOURITES_FILE).read()
		b=a.replace('#START OF FILE#', '#START OF FILE#\n<item>\n<name>'+str(name)+'</name>\n<link>'+str(url)+'</link>\n<site>XNXX</site>\n<icon>'+str(iconimage)+'</icon>\n</item>\n')
		f= open(FAVOURITES_FILE, mode='w')
		f.write(str(b))
		f.close()
		dialog.ok(AddonTitle, "[COLOR pink]" + name + " has been added to your favourites. You can access your favourites on the main menu.[/COLOR]")
		dp.close()
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
			b=a.replace('#START OF FILE#', '#START OF FILE#\n<item>\n<date>'+str(date_now)+'</date>\n<time>'+str(time_now)+'</time>\n<name>'+str(name)+'</name>\n<link>'+str(url)+'</link>\n<site>XNXX</site>\n<icon>'+str(iconimage)+'</icon>\n</item>\n')
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