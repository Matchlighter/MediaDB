from django.db import models
from django.forms import ModelForm
from django.conf import settings
from django.forms.models import modelform_factory

import tmdb3
import library
import os.path
import json
import requests

type_choices = (
	('PRM', 'Primary'),
	('BONUS', 'Bonus')
)

class Location(models.Model):
	name = models.CharField(max_length=200)
	short_name = models.CharField(max_length=3)
	
	def get_next_index(self):
		movs = self.mediaobject_set.order_by('index')
		ind = 1
		for mv in movs:
			if mv.index>ind:
				return ind
			ind += 1
			
		return ind
	
	def __str__(self):
		return self.name
	
class MFormat(models.Model):
	name = models.CharField(max_length=10)
	
	def __str__(self):
		return self.name

class MediaBase(models.Model):
	title = models.CharField("Title", max_length=200)
	tmdb_id = models.IntegerField(blank=True, null=True, unique=True)
	
	class Meta:
		abstract = True
		
	def get_poster_path(self):
		return ''
		
class LinkedMedia(models.Model):
	pass
	
	class Meta:
		abstract = True
		
class Movie(MediaBase):
	mediums = models.ManyToManyField('MediaObject', blank=True, through='MovieMedia', related_name='movies')
	
	def _get_index(self): #This is a very heavy op
		ret = ""
		for media in self.mediums.all():
			if media.type == "PRM":
				if ret is not "":
					ret += ", "
				ret += "%s%s" % (media.location.short_name, media.index)
		return ret
		
	def get_index(self):
		if not hasattr(self, '_locindex'):
			self._locindex = self._get_index()
		return self._locindex
		
	def primaryMO(self):
		for media in self.mediums.all():
			if media.type == "PRM":
				return media

	def get_tmdb_movie(self):
		if self.tmdb_id != None:
			return tmdb3.Movie(self.tmdb_id)

	def get_json_path(self):
		return os.path.join(settings.TMDB_JSON_STORE, 'Movie%s.json'%self.tmdb_id)

	cached_json = None
	@property
	def json(self, allow_pull=True):
		if self.tmdb_id and self.cached_json is None:
			jsonPath = self.get_json_path()
			if not os.path.exists(jsonPath):
				if allow_pull:
					self.pull_tmdb_info()
				else:
					return None
			
			with open(jsonPath, 'r') as f:
				self.cached_json = json.load(f)

		return self.cached_json
		
	def get_poster_url(self):
		if self.json:
			return self.json.get("poster_path")
		
	def get_backdrop_url(self):
		pass
	
	def get_ripped(self):
		from django.db import connections
		cursor = connections['xbmc_movies'].cursor()
		cursor.execute("SELECT COUNT(*) FROM movie WHERE c00 = %s;", [self.title])
		return cursor.fetchone()[0] > 0

	def pull_tmdb_info(self):
		with open(self.get_json_path(), 'wb') as f:
			resp = requests.get(library.tmdb_url + 'movie/%s'%self.tmdb_id, params={'api_key': settings.TMDB_KEY})
			json.dump(resp.json(), f)
			
	def __str__(self):
		return self.title
			
class MediaObject(models.Model):
	index = models.IntegerField("Index", null=True)
	format = models.ForeignKey(MFormat)
	ripped = models.BooleanField(default=False)
	type = models.CharField(max_length=15, choices=type_choices, default=0)
	
	location = models.ForeignKey(Location)
	
	class Meta:
		unique_together = (('location', 'index'))
	
	def __str__(self):
		return "%s - %s" % (self.location.name, self.index)
	
class MovieMedia(models.Model):
	movie = models.ForeignKey(Movie)
	medium = models.ForeignKey(MediaObject)
	
	def __str__(self):
		return "%s : %s" % (self.movie, self.medium)
		
	def delete(self):
		super(MovieMedia, self).delete()
		if self.medium.movies.count() == 0:
			self.medium.delete()
			
class TVSeries(MediaBase):
	
	#Generate seasons from tmdb
	def import_tmdb(self):
		pass
	
class TVSeason(LinkedMedia):
	series = models.ForeignKey(TVSeries)
	number = models.IntegerField()
	
	mediums = models.ManyToManyField('MediaObject', blank=True, through='TVSeasonMedia', related_name='tv_seasons')
	
	class Meta:
		ordering = ['number']
	
	#Generate episodes from tmdb
	def import_tmdb(self):
		pass
	
class TVEpisode(models.Model):
	title = models.CharField(max_length=200)
	season = models.ForeignKey(TVSeason)
	number = models.IntegerField()
	
	class Meta:
		ordering = ['number']
	
class TVSeasonMedia(models.Model):
	tvseason = models.ForeignKey(TVSeason)
	medium = models.ForeignKey(MediaObject)
	
	order = models.PositiveIntegerField()

	class Meta:
		ordering = ('order',)
