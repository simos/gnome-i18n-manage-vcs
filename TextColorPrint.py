#!/usr/bin/python

# Thanks to Marginal Structure,
# http://blog.quaternio.net/2009/05/18/colourizing-python-print-statements/

import re

class TextColorPrint:
    colors = {
        # regular (darker) colors
        'dark_gray':          '\033[0;30m',
        'dark_red':           '\033[0;31m',
        'dark_green':         '\033[0;32m',
        'dark_yellow':        '\033[0;33m',
        'dark_blue':          '\033[0;34m',
        'dark_magenta':       '\033[0;35m',
        'dark_cyan':          '\033[0;36m',
        'dark_gray':          '\033[0;37m',
        'dark_crimson':       '\033[0;38m',

        # brighter (bolded) colors
        'gray':               '\033[1;30m',
        'red':                '\033[1;31m',
        'green':              '\033[1;32m',
        'yellow':             '\033[1;33m',
        'blue':               '\033[1;34m',
        'magenta':            '\033[1;35m',
        'cyan':               '\033[1;36m',
        'white':              '\033[1;37m',
        'crimson':            '\033[1;38m',

        # text on colored background
        'red_highlight':      '\033[1;41m',
        'green_highlight':    '\033[1;42m',
        'yellow_highlight':   '\033[1;43m',
        'blue_highlight':     '\033[1;44m',
        'magenta_highlight':  '\033[1;45m',
        'cyan_highlight':     '\033[1;46m',
        'gray_highlight':     '\033[1;47m',
        'crimson_highlight':  '\033[1;48m',

        # miscellaneous other
        'underscore':         '\033[0;04m',
        'inverse':            '\033[0;07m',
        'concealed':          '\033[0;08m', 

        # remove color formatting
        'clear':              '\033[0m',
    }

    def show_colors(self):
        ''' show all available color options'''
        for key in self.colors:
            print self.cprint(key, key)

    def cprint(self, string, color='red'):
        ''' print string in the color specified.'''
        if not self.colors.has_key(color):
            raise KeyError, 'Invalid color. use show_colors() to see all options.' 
        return self.colors[color] + string + self.colors['clear']

    def hprint(self, string, regex, color='red'):
        ''' find and highlight all occurences of regex in string and print
        those characters in the color specified '''
        if not self.colors.has_key(color):
            raise KeyError, 'Invalid color. use show_colors() to see all options.'        
        formatted = re.sub('(?P<x>' + regex+')', self.colors[color] + '\g<x>' + self.colors['clear'], string)
        return formatted

if __name__ == '__main__':
    a = TextColorPrint()
    a.show_colors()
    a.hprint("This is a test, one of many. Test.", "[Tt]est")

