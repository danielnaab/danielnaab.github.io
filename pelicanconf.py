#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os


AUTHOR = 'Daniel Naab'
SITENAME = 'Crushing Pennies'
SITETAGLINE = "Daniel Naab is Crushing Pennies and is writing code."
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/Chicago'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
#LINKS = (('Pelican', 'http://getpelican.com/'),
#         ('Python.org', 'http://python.org/'),
#         ('Jinja2', 'http://jinja.pocoo.org/'),
#         ('You can modify those links in your config file', '#'),)
#SOCIAL = (('Github', 'https://github.com/danielnaab'),
#          ('LinkedIn', 'https://www.linkedin.com/in/danielnaab'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# Enable some typographic improvements in generated HTML.
TYPOGRIFY = True

_this_dir = os.path.dirname(__file__)
THEME = os.path.join(_this_dir, 'theme')

PLUGIN_PATHS = [os.path.join(_this_dir, 'pelican-plugins')]
PLUGINS = [
    'assets',
    'minify',
]
