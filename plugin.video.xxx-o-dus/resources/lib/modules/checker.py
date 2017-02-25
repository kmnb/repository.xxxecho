"""
    Copyright (C) 2016 ECHO Wizard

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
import os
from resources.lib.modules  import common

def check(url):

	REPO_FOLDER,INFO = url.split('|SPLIT|')
	
	if not os.path.exists(REPO_FOLDER):
		f = open(INFO,mode='r'); msg = f.read(); f.close()
		common.TextBoxes("%s" % msg)
		quit()
	else: return
