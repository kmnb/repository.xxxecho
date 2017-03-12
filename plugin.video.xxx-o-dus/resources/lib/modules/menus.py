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

addon_id            = 'plugin.video.xxx-o-dus'
AddonTitle          = '[COLOR orangered]XXX-O-DUS[/COLOR]'
fanart              = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon                = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
xhamster_icon       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/xhamster/icon.png'))
xhamster_fanart     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/xhamster/fanart.jpg'))
chaturbate_icon     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/chaturbate/icon.png'))
chaturbate_fanart   = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/chaturbate/fanart.jpg'))
xnxx_icon           = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/xnxx/icon.png'))
xnxx_fanart         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/xnxx/fanart.jpg'))
redtube_icon        = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/redtube/icon.png'))
redtube_fanart      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/redtube/fanart.jpg'))
pornhd_icon         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/pornhd/icon.png'))
pornhd_fanart       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/pornhd/fanart.jpg'))
porncom_icon        = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/porncom/icon.png'))
porncom_fanart      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/porncom/fanart.jpg'))
youporn_icon        = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/youporn/icon.png'))
youporn_fanart      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/youporn/fanart.jpg'))
pornfun_icon        = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/pornfun/icon.png'))
pornfun_fanart      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/pornfun/fanart.jpg'))
motherless_icon     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/motherless/icon.png'))
motherless_fanart   = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/motherless/fanart.jpg'))
spankbang_icon      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/spankbang/icon.png'))
spankbang_fanart    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/spankbang/fanart.jpg'))
porn00_icon         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/porn00/icon.png'))
porn00_fanart       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/porn00/fanart.jpg'))
virtualpornstars_icon   = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/virtualpornstars/icon.png'))
virtualpornstars_fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/virtualpornstars/fanart.jpg'))
watchxxxfree_icon   = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/watchxxxfree/icon.png'))
watchxxxfree_fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/watchxxxfree/fanart.jpg'))
perfectgirls_icon   = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/perfectgirls/icon.png'))
perfectgirls_fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/perfectgirls/fanart.jpg'))
justporno_icon      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/justporno/icon.png'))
justporno_fanart    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/justporno/fanart.jpg'))
eporner_icon        = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/eporner/icon.png'))
eporner_fanart      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/eporner/fanart.jpg'))
pornxs_icon         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/pornxs/icon.png'))
pornxs_fanart       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/pornxs/fanart.jpg'))
xvideos_icon        = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/xvideos/icon.png'))
xvideos_fanart      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/xvideos/fanart.jpg'))
nxgx_icon           = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/nxgx/icon.png'))
nxgx_fanart         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/nxgx/fanart.jpg'))

def SEARCH():

	common.addDir("[COLOR white]SEARCH ALL WESBITES[/COLOR]","null",99,icon,fanart)
	common.addLink("[COLOR darkgray]#################################[/COLOR]","url",999,icon,fanart)
	common.addDir("[COLOR white]Search Eporner[/COLOR]",'null',244,eporner_icon,eporner_fanart)
	common.addDir("[COLOR white]Search Just Porno TV[/COLOR]","null",234,justporno_icon,justporno_fanart)
	common.addDir("[COLOR white]Search Motherless[/COLOR]","null",97,motherless_icon,motherless_fanart)
	common.addDir("[COLOR white]Search NXGX[/COLOR]","null",274,nxgx_icon,nxgx_fanart)
	common.addDir("[COLOR white]Search Perfect Girls[/COLOR]","null",314,perfectgirls_icon,perfectgirls_fanart)
	common.addDir("[COLOR white]Search Porn.com[/COLOR]","null",64,porncom_icon,porncom_fanart)
	common.addDir("[COLOR white]Search Porn00[/COLOR]","null",214,porn00_icon,porn00_fanart)
	common.addDir("[COLOR white]Search PornFun[/COLOR]","null",84,pornfun_icon,pornfun_fanart)
	common.addDir("[COLOR white]Search PornHD[/COLOR]","null",54,pornhd_icon,pornhd_fanart)
	common.addDir("[COLOR white]Search PornXS[/COLOR]",'null',254,pornxs_icon,pornxs_fanart)
	common.addDir("[COLOR white]Search RedTube[/COLOR]","null",45,redtube_icon,redtube_fanart)
	common.addDir("[COLOR white]Search Spankbang[/COLOR]","null",205,spankbang_icon,spankbang_fanart)
	common.addDir("[COLOR white]Search Virtual Porn Stars[/COLOR]","null",224,virtualpornstars_icon,virtualpornstars_fanart)
	common.addDir("[COLOR white]Search Watch XXX Free[/COLOR]","null",304,watchxxxfree_icon,watchxxxfree_fanart)
	common.addDir("[COLOR white]Search Xhamster[/COLOR]","null",14,xhamster_icon,xhamster_fanart)
	common.addDir("[COLOR white]Search XNXX[/COLOR]","null",29,xnxx_icon,xnxx_fanart)
	common.addDir("[COLOR white]Search Xvideos[/COLOR]",'null',264,xvideos_icon,xvideos_fanart)
	common.addDir("[COLOR white]Search YouPorn[/COLOR]","null",74,youporn_icon,youporn_fanart)

	kodi_name = common.GET_KODI_VERSION()

	if kodi_name == "Jarvis":
		xbmc.executebuiltin('Container.SetViewMode(50)')
	elif kodi_name == "Krypton":
		xbmc.executebuiltin('Container.SetViewMode(55)')
	else: xbmc.executebuiltin('Container.SetViewMode(50)')
	
def VIDEOS():

	common.addDir("[COLOR white]Eporner.com[/COLOR]",'url',240,eporner_icon,eporner_fanart)
	common.addDir("[COLOR white]JustPorno.TV[/COLOR]",'url',230,justporno_icon,justporno_fanart)
	common.addDir("[COLOR white]Motherless.com[/COLOR]",'url',93,motherless_icon,motherless_fanart)
	common.addDir("[COLOR white]NXGX.com[/COLOR]",'url',270,nxgx_icon,nxgx_fanart)
	common.addDir("[COLOR white]Perfectgirls.net[/COLOR]",'url',310,perfectgirls_icon,perfectgirls_fanart)
	common.addDir("[COLOR white]Porn00.org[/COLOR]",'url',210,porn00_icon,porn00_fanart)
	common.addDir("[COLOR white]Porn.com[/COLOR]",'url',60,porncom_icon,porncom_fanart)
	common.addDir("[COLOR white]PornFun.com[/COLOR]",'url',80,pornfun_icon,pornfun_fanart)
	common.addDir("[COLOR white]PornHD.com[/COLOR]",'url',50,pornhd_icon,pornhd_fanart)
	common.addDir("[COLOR white]PornXS.com[/COLOR]",'url',250,pornxs_icon,pornxs_fanart)
	common.addDir("[COLOR white]RedTube.com[/COLOR]",'url',41,redtube_icon,redtube_fanart)
	common.addDir("[COLOR white]Spankbang.com[/COLOR]",'url',200,spankbang_icon,spankbang_fanart)
	common.addDir("[COLOR white]Virtualpornstars.com[/COLOR]",'url',220,virtualpornstars_icon,virtualpornstars_fanart)
	common.addDir("[COLOR white]Watchxxxfree.com[/COLOR]",'url',300,watchxxxfree_icon,watchxxxfree_fanart)
	common.addDir("[COLOR white]Xhamster.com[/COLOR]",'url',10,xhamster_icon,xhamster_fanart)
	common.addDir("[COLOR white]XNXX.com[/COLOR]",'url',30,xnxx_icon,xnxx_fanart)
	common.addDir("[COLOR white]Xvideos.com[/COLOR]",'url',260,xvideos_icon,xvideos_fanart)
	common.addDir("[COLOR white]YouPorn.com[/COLOR]",'url',70,youporn_icon,youporn_fanart)

	kodi_name = common.GET_KODI_VERSION()

	if kodi_name == "Jarvis":
		xbmc.executebuiltin('Container.SetViewMode(50)')
	elif kodi_name == "Krypton":
		xbmc.executebuiltin('Container.SetViewMode(55)')
	else: xbmc.executebuiltin('Container.SetViewMode(50)')
	
def LIVE():

	common.addDir("[COLOR white]Chaturbate.com[/COLOR]",'url',20,chaturbate_icon,chaturbate_fanart)
	common.addDir("[COLOR white]Live Channels[/COLOR]",'http://echocoder.com/m3u/xxxodus.xml',995,icon,fanart)

	kodi_name = common.GET_KODI_VERSION()

	if kodi_name == "Jarvis":
		xbmc.executebuiltin('Container.SetViewMode(50)')
	elif kodi_name == "Krypton":
		xbmc.executebuiltin('Container.SetViewMode(55)')
	else: xbmc.executebuiltin('Container.SetViewMode(50)')
	
def PICTURES():

	common.addDir("[COLOR white]Motherless Pictures[/COLOR]","url",90,motherless_icon,motherless_fanart)
	common.addDir("[COLOR white]XNXX Pictures[/COLOR]","url",34,xnxx_icon,xnxx_fanart)
	
	kodi_name = common.GET_KODI_VERSION()

	if kodi_name == "Jarvis":
		xbmc.executebuiltin('Container.SetViewMode(50)')
	elif kodi_name == "Krypton":
		xbmc.executebuiltin('Container.SetViewMode(55)')
	else: xbmc.executebuiltin('Container.SetViewMode(50)')
	
def STORIES():

	common.addDir("[COLOR white]XNXX Stories[/COLOR]","url",38,xnxx_icon,xnxx_fanart)

	kodi_name = common.GET_KODI_VERSION()

	if kodi_name == "Jarvis":
		xbmc.executebuiltin('Container.SetViewMode(50)')
	elif kodi_name == "Krypton":
		xbmc.executebuiltin('Container.SetViewMode(55)')
	else: xbmc.executebuiltin('Container.SetViewMode(50)')