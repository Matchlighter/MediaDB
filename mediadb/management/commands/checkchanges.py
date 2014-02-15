from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from app.models import Movie
from app import library

import requests
import json
import time

class Command(BaseCommand):
        help = 'Checks for changed movies and pulls new JSON'
	
	def getPage(self, pg):
		return requests.get(library.tmdb_url + 'movie/changes', params={'api_key': settings.TMDB_KEY, 'page': pg}).json()

	def processPage(self, pg):
		for mov in pg['results']:
			qs = Movie.objects.filter(tmdb_id=mov['id'])
			if qs.exists():
				self.stdout.write("Refreshing info for id %s: '%s'"%(mov['id'], qs[0].title))
				qs[0].pull_tmdb_info()
				time.sleep(0.4)

	def handle(self, *args, **params):
		fpg = self.getPage(1)
		self.processPage(fpg)
		for i in range(2, fpg['total_pages']):
			self.processPage(self.getPage(i))
