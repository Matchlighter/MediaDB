# Django settings for movies_db project.

import os
from base_settings import *
APP_ROOT = os.path.dirname(__file__)

TMDB_KEY = ''

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
		'NAME': 'moviesdb_dev',                      # Or path to database file if using sqlite3.
		# The following settings are not used with sqlite3:
		'USER': 'movies',
		'PASSWORD': 'movies',
		'HOST': '127.0.0.1',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
		'PORT': '',                      # Set to empty string for default.
	},
	'xbmc_movies': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'MyVideos75',
		'USER': 'xbmc',
		'PASSWORD': 'xbmc',
		'HOST': '127.0.0.1',
		'PORT': '',
	}
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Denver'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(APP_ROOT, 'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

TMDB_JSON_STORE = os.path.join(MEDIA_ROOT, 'MovieStore/')

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(APP_ROOT, 'static/')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'