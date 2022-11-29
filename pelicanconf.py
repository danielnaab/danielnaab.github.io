import os

AUTHOR = 'Daniel Naab'
SITENAME = 'Crushing Pennies'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/Chicago'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
# LINKS = (('Pelican', 'https://getpelican.com/'),
#          ('Python.org', 'https://www.python.org/'),
#          ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
#          ('You can modify those links in your config file', '#'),)

# Social widget
# SOCIAL = (('You can add links in your config file', '#'),
#           ('Another social link', '#'),)

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
    'css-html-js-minify',
]
