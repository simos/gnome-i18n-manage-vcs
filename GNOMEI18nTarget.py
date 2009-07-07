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

PROGNAME='gnome-i18n-manage-vcs'

PACKAGE_NAME    = 'GNOME I18n Manage VCS'
PACKAGE_VERSION = '0.9'
PACKAGE_AUTHORS = ['Simos Xenitellis <simos@gnome.org>', 'Og Maciel <ogmaciel@gnome.org>']
PACKAGE_COPYRIGHT = 'Copyright 2009 Simos Xenitellis'

class GNOMEI18nTarget:
    def __init__(self):
        self.message_states = ['translated', 'untranslated', 'fuzzy', 'docfuzzy', 'docuntranslated', 'doctranslated']
        self.flags = []

        self.stats_release = None
        self.stats_language = None

        self.category_id = None

        self.module_id = None
        self.module_branch = None       

        self.domain = None
        self.document = None

        self.pofile = None
        self.vcspath = None

        self.resources = []
        self.module = {}
        self.category = {}
        self.stats = {}

    def start(self, tag, attrib):
        if tag not in self.message_states:
            if tag == 'domain':
                self.domain = attrib['id']
            elif tag == 'document':
                self.document = attrib['id']
            elif tag == 'module':
                self.module_id = attrib['id']
                self.module_branch = attrib['branch']
            elif tag == 'category':
                self.category_id = attrib['id']
            elif tag == 'stats':
                self.stats_release = attrib['release']
                self.stats_language = attrib['language']
            elif tag not in ['pofile', 'svnpath']:
                # Should not be reached
                #print self.tabs[:self.level], ('start %s %s' % (tag, attrib))
                pass
            self.push_flag(tag)

    def end(self, tag):
        if tag not in self.message_states:
            if tag == 'domain':
                self.resources.append({'id': tag, 'type': self.domain, 
                    'pofile': self.pofile, 'vcspath' : self.vcspath }) 
                self.domain = self.pofile = self.vcspath = None
            elif tag == 'document':
                self.resources.append({'id': tag, 'type': self.document, 
                    'pofile': self.pofile, 'vcspath' : self.vcspath }) 
                self.document = self.pofile = self.vcspath = None
            elif tag == 'module':
                self.module[self.module_id] = { 'branch': self.module_branch, 'resource': self.resources }
                self.module_id = self.module_branch = None
                self.resources = []
            elif tag == 'category':
                self.category[self.category_id] = self.module
                self.module = {}
                self.category_id = None
            elif tag == 'stats':
                self.stats = { 'language': self.stats_language, 'release': self.stats_release, 
                        'categories': self.category } 
                self.category = {}
                self.stats_release = self.stats_language = None
            elif tag not in ['pofile', 'svnpath']:
                # Should not be reached
                        #print self.tabs[:self.level], ('end %s' % tag)
                pass
            self.pop_flag(tag)

    def data(self, data):
        if not data.isspace() and not data.isdigit():
            if self.flags[-1] == 'pofile':
                self.pofile = data
            elif self.flags[-1] == 'svnpath':
                self.vcspath = data
            else:
                # Should not be reached
                        #print self.tabs[:self.level], ('data %r' % data)
                pass

    def comment(self, text):
        pass

    def close(self):
        return True

    def push_flag(self, tag):
        self.flags.append(tag)

    def pop_flag(self, tag):
        if self.flags.pop() != tag:
            print 'ERROR, did not pop', tag

    def get_stats(self):
        return self.stats
