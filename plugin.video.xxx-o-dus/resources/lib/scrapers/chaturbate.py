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
fanart         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/chaturbate/fanart.jpg'))
icon           = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/chaturbate/icon.png'))
next_icon      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/chaturbate/next.png'))
twitter_icon   = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/chaturbate/twitter.png'))
pc_icon        = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/chaturbate/pc.png'))
featured_icon  = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/chaturbate/featured.png'))
female_icon    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/chaturbate/female.png'))
male_icon      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/chaturbate/male.png'))
couple_icon    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/chaturbate/couples.png'))
trans_icon     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/chaturbate/trans.png'))
BASE 		   = 'http://www.chaturbate.com'
F4M            = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.f4mTester'))
HISTORY_FILE   = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'history.xml'))
FAVOURITES_FILE= xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'favourites.xml'))

def MAIN_MENU():

	result = common.open_url(BASE)
	
	match = re.compile('<ul class="sub-nav">(.+?)<div class="content">',re.DOTALL).findall(result)
	string = str(match)
	match2 = re.compile("<li(.+?)</li>",re.DOTALL).findall(string)
	fail = 0
	videos = 0
	for item in match2:
		url=re.compile('<a href="(.+?)">.+?</a>').findall(item)[0]
		title=re.compile('<a href=".+?">(.+?)</a>').findall(item)[0]
		url3 = url
		url4 = url3.replace('\\','')
		url = "http://www.chaturbate.com" + url4
		if "featured" in title.lower():
			name = "[COLOR white]" + title + "[/COLOR]"
			common.addDir(name,url,21,featured_icon,fanart)
		elif "female" in title.lower():
			name = "[COLOR white]Females[/COLOR]"
			common.addDir(name,url,21,female_icon,fanart)
		elif "male" in title.lower():
			name = "[COLOR white]Males[/COLOR]"
			common.addDir(name,url,21,male_icon,fanart)
		elif "couple" in title.lower():
			name = "[COLOR white]Couples[/COLOR]"
			common.addDir(name,url,21,couple_icon,fanart)
		elif "trans" in title.lower():
			name = "[COLOR white]Transexual[/COLOR]"
			common.addDir(name,url,21,trans_icon,fanart)


	common.addLink("[COLOR pink] ################# RANDOM PICKS #################[/COLOR]","url",999,twitter_icon,fanart)

	POP_NOW(BASE)

	kodi_name = common.GET_KODI_VERSION()

	if kodi_name == "Jarvis":
		xbmc.executebuiltin('Container.SetViewMode(50)')
	elif kodi_name == "Krypton":
		xbmc.executebuiltin('Container.SetViewMode(55)')
	else: xbmc.executebuiltin('Container.SetViewMode(50)')

def POP_NOW(url):

	i = 1
	result = common.open_url(url)
	match = re.compile('<ul class="list">(.+?)<ul class="paging">',re.DOTALL).findall(result)
	string = str(match)
	match2 = re.compile("<li>(.+?)</li>",re.DOTALL).findall(string)
	for item in match2:
		if i <= 7:
			try:
				title=re.compile('<a href=".+?"> (.+?)</a>').findall(item)[0]
				url=re.compile('<a href="(.+?)">.+?</a>').findall(item)[0]
				iconimage=re.compile('<img src="(.+?)"').findall(item)[0]
				try:
					age=re.compile('<span class="age gender.+?">(.+?)</span>').findall(item)[0]
				except: age = "Unknown"
				if 'thumbnail_label_c_hd">' in item:
					name = "[COLOR pink]HD[/COLOR][COLOR yellow] - " + title + " - Age " + age + "[/COLOR]"
				elif 'label_c_new' in item:
					name = "[COLOR blue]NEW[/COLOR][COLOR yellow] - " + title + " - Age " + age + "[/COLOR]"
				else:
					name = "[COLOR yellow]" + title + " - Age " + age + "[/COLOR]"
				url2 = title + '|SPLIT|' + url + '|SPLIT|' + iconimage
				common.addLink(name,url2,23,iconimage,fanart)
				i = i + 1
			except: pass


def GET_CONTENT(url):

	checker = url
	result = common.open_url(url)
	match = re.compile('<ul class="list">(.+?)<ul class="paging">',re.DOTALL).findall(result)
	string = str(match)
	match2 = re.compile("<li>(.+?)</li>",re.DOTALL).findall(string)
	for item in match2:
		try:
			title=re.compile('<a href=".+?"> (.+?)</a>').findall(item)[0]
			url=re.compile('<a href="(.+?)">.+?</a>').findall(item)[0]
			iconimage=re.compile('<img src="(.+?)"').findall(item)[0]
			try:
				age=re.compile('<span class="age gender.+?">(.+?)</span>').findall(item)[0]
			except: age = "Unknown"
			if 'thumbnail_label_c_hd">' in item:
				name = "[COLOR pink]HD[/COLOR][COLOR yellow] - " + title + " - Age " + age + "[/COLOR]"
			elif 'label_c_new' in item:
				name = "[COLOR blue]NEW[/COLOR][COLOR yellow] - " + title + " - Age " + age + "[/COLOR]"
			else:
				name = "[COLOR yellow]" + title + " - Age " + age + "[/COLOR]"
			url2 = title + '|SPLIT|' + url + '|SPLIT|' + iconimage
			common.addLink(name,url2,23,iconimage,fanart)
		except: pass

	try:
		np=re.compile('<ul class="paging">(.+?)</ul>',re.DOTALL).findall(result)
		for item in np:
			next=re.compile('<li><a href="(.+?)" class="next endless_page_link">next</a></li>').findall(item)[0]
			url = "http://chaturbate.com" + str(next)
			common.addDir('[COLOR pink]Next Page >>[/COLOR]',url,21,next_icon,fanart)       
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
        string = keyboard.getText().replace(' ','').capitalize()
        if len(string)>1:
            url = "http://www.youporn.com/search/?query=" + string
            GET_CONTENT(url)
        else: quit()

def PLAY_URL(name,url,iconimage):
	
	dp = common.GET_LUCKY()
	name,url,iconimage = url.split('|SPLIT|')
	orig_url = "http://www.chaturbate.com" + url
	result = common.open_url(orig_url)
	match = re.compile('<head>(.+?)</html>',re.DOTALL).findall(result)
	string = str(match).replace('\\','').replace('(','').replace(')','')
	url = "null"
	try:
		url_fast = re.compile("hlsSourceFast = '(.+?)';").findall(string)[0]
	except: url_fast == "null"
	try:
		url_slow = re.compile("hlsSourceSlow = '(.+?)';").findall(string)[0]
	except: url_slow == "null"
	if not "http" in url_fast:
		url = url_slow
	if not "http" in url_slow:
		url = url_fast
	if url == "null":
		choice = dialog.select("[COLOR red]Please select an option[/COLOR]", ['[COLOR pink]Watch Fast Stream[/COLOR]','[COLOR pink]Watch Slow Stream[/COLOR]'])
		if choice == 0:
			url = url_fast
		elif choice == 1:
			url = url_slow
		else: quit()
	if os.path.exists(F4M):
		url2 = 'plugin://plugin.video.f4mTester/?streamtype=HLSRETRY&amp;name='+name+'&amp;url='+url+'&amp;iconImage='+iconimage
	else:
		url2 = url + '|Referer=' + orig_url
	dp.close()

	history_on_off  = plugintools.get_setting("history_setting")
	if history_on_off == "true":	
		date_now = datetime.datetime.now().strftime("%d-%m-%Y")
		time_now = datetime.datetime.now().strftime("%H:%M")
		a=open(HISTORY_FILE).read()
		b=a.replace('#START OF FILE#', '#START OF FILE#\n<item>\n<date>'+str(date_now)+'</date>\n<time>'+str(time_now)+'</time>\n<name>'+str(name)+'</name>\n<link>'+str(url2)+'</link>\n<site>Chaturbate</site>\n<icon>'+str(iconimage)+'</icon>\n</item>\n')
		f= open(HISTORY_FILE, mode='w')
		f.write(str(b))
		f.close()
	
	liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	xbmc.Player ().play(url2, liz, False)