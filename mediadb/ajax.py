from django.shortcuts import get_object_or_404, render, redirect
from models import *
from forms import *
from django.http import HttpResponse
from django.conf import settings
from django.core.urlresolvers import reverse

import library
import re
import json
import tmdb3

def getMovieList(req):
	tmdbResp = tmdb3.request.Request('search/movie', query=req.GET['q'], search_type='ngram').read()
	ljson = json.loads(tmdbResp)
	return HttpResponse(json.dumps(ljson['results']), content_type='application/json')

def movie_list_json(req):
	movs = Movie.objects.order_by('title')
	
	out_data = {
		'options': {
			'baseImageUrl': tmdb3.Configuration.images['base_url'],
			'poster_sizes': tmdb3.Configuration.images['poster_sizes'],
		},
		'media': [
			{
				'id': movie.pk,
				'title': movie.title,
				'ripped': movie.get_ripped(),
				'url': reverse('mediadb:movie:show', args=[movie.id]),
				'indices': [{'type': medium.type,
					'index': medium.index,
					'full_location': medium.location.name,
					'short_location': medium.location.short_name} for medium in movie.mediums.all()],
				'poster_path': movie.get_poster_url(),
			} for movie in movs
		],
		
	}
	return HttpResponse(json.dumps(out_data), content_type='text/json')
	
def movie_details(req, pk):
	movie = get_object_or_404(Movie, pk=pk)
	return HttpResponse(json.dumps(movie.json), content_type='text/json')
	
def tmdb(req, resource):
	from tmdb3.request import Request
	req2 = Request(resource)
	req2.add_header('X-Forwarded-For', req.META['REMOTE_ADDR'])
	return HttpResponse(req2.read(), content_type='text/json')