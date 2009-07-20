#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

# Author  : Simos Xenitellis <simos@gnome.org>, 2009
# Version : 0.9

import ConfigParser             # ConfigParser()
import GNOMEI18nTarget

try:
    from lxml import etree      # etree.XMLParser(), etree.XML()
except ImportError, err:
    print 'Import error:', err
    print 'This script requires to have the "python-lxml" package installed'
    print 'Please install the package python-lxml and try again.\nExiting...'
    sys.exit(-10)

PROGNAME='gnome-i18n-manage-vcs'

PACKAGE_NAME    = 'GNOME I18n Manage VCS'
PACKAGE_VERSION = '0.9'
PACKAGE_AUTHORS = ['Simos Xenitellis <simos@gnome.org>', 'Og Maciel <ogmaciel@gnome.org>']
PACKAGE_COPYRIGHT = 'Copyright 2009 Simos Xenitellis'

class ModuleIterator:
    def __init__(self, language, release, category, module, transtype):
        self.language = language
        self.release = release
        self.category = category
        self.module = module
        self.transtype = transtype
        self.gnome_release_data = ''

        self.selected_modules = []
        
        if self.release:
            self.gnome_release_data = self.generate_gnome_release_data()
            
            for cat in self.gnome_release_data['categories'].keys():
                if self.category != '' and cat != self.category:
                    continue
                for mod in self.gnome_release_data['categories'][cat]:
                    if self.module != '' and mod != self.module:
                        continue
                    for resource in self.gnome_release_data['categories'][cat][mod]['resource']:
                        if self.transtype:
                            if resource['id'] not in self.transtype:
                                continue
                            else:
                                self.selected_modules.append([mod, resource])
                        else:
                            self.selected_modules.append([mod, resource])

    def next(self):
        return self.selected_modules.pop()

    def __iter__(self):
        return self

    def generate_gnome_release_data(self):
        """ Assumes that there exist an XML with release RSS feed """
        filename = 'managevcs-%s-%s.xml' % (self.language, self.release)

        try:
            xmlfile = open(filename, 'r')
            xmlfile.close
        except OSError:
            print 'Could not open file ', filename, '. Aborting...'
            sys.exit(-1)
    
        contents = ''.join(xmlfile.readlines())
        
        mytarget = GNOMEI18nTarget.GNOMEI18nTarget()
        parser = etree.XMLParser(target = mytarget)
        result = etree.XML(contents, parser)
    
        return mytarget.get_stats()

if __name__ == '__main__':
    a = iter(ModuleIterator('el', 'gnome-2-28', '', 'gnome-games', ''))

    try:
        for module_set in a:
            print module_set[0], module_set[1]
    except:
        pass

