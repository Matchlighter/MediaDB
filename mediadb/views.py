# Create your views here.
from django.shortcuts import get_object_or_404, render, redirect
from mediadb.models import *
from mediadb.forms import *
from django.views import generic
from django.http import HttpResponse
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import add_to_builtins
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers

from django.forms.models import inlineformset_factory, modelformset_factory, modelform_factory

import library
import re
import json
import tmdb3

def index(req, v=None):
	search = req.GET.get('q', '')
	
	vmode = req.session.get('viewmode', 'grid') if v == None else v.lower()
	req.session['viewmode'] = vmode
	
	context = {
		'page_title': 'Movies',
		'term': search,
		'ajax_loading': False, # Toggle the use of AJAX. Makes the grid load faster initially.
	}
	
	if not vmode == 'grid' or not context.get('ajax_load'):
		movs = Movie.objects.filter(title__icontains=search).order_by('title')
		# for mov in movs:
			# mov['trimmedTitle'] = re.sub(r'^(The|A) (.*)', r'\2, \1', 'The Big Game'), mov.title)
	
		if vmode == 'list':
			pager = Paginator(movs, 20)
			page = req.GET.get('p')
	
			try:
				movs = pager.page(page)
			except PageNotAnInteger:
				movs = pager.page(1)
			except EmptyPage:
				movs = pager.page(pager.num_pages)

		context['movies'] = movs
		
	if vmode == 'grid':
		if req.GET.get('poster_width'):
			req.session['grid_poster_width'] = req.GET.get('poster_width')
		context['poster_width'] = req.session.get('grid_poster_width', 190)
		context['genres_list'] = []
		#context['ajax_load'] = True
		
	return render(req, 'mediadb/movies/%s.html'%vmode, context)

def gridBody(req):
	movs = Movie.objects.order_by('title')
	return render(req, 'mediadb/movies/partials/grid_body.html', {
		'movies': movs,
		'poster_width': req.session.get('grid_poster_width', 190),
		'genres_list': [],
	})

def _movie_context(movie):
	mjson = movie.json
	context = {}
	
	if mjson != None:
		import tmdb3
		url = tmdb3.Configuration.images['base_url'].rstrip('/')
		context['mjson'] = mjson
		if mjson.get("poster_path") != None:
			context['poster'] = url+'/{0}/{1}'.format('original', mjson.get("poster_path"))
		if mjson.get("backdrop_path") != None:
			context['bg'] = url+'/{0}/{1}'.format('original', mjson.get("backdrop_path"))
	return context
	
def show(req, pk):
	mov = get_object_or_404(Movie, pk=pk)
	#tmdbMovie = mov.get_tmdb_movie()
	context = {
		'movie': mov,
		'page_title': 'Movie:'
	}
	
	context.update(_movie_context(mov))
	return render(req, 'mediadb/movies/show.html', context)

def edit(req, pk=None):
	if pk:
		mov = get_object_or_404(Movie, pk=pk)
		pg_title = 'Edit \'%s\'' % mov.title
		btn_txt = 'Save changes'
		extra_itms = 0
	else:
		mov = Movie()
		pg_title = 'Add Movie...'
		btn_txt = 'Add'
		extra_itms = 1

	MediaFormSet = inlineformset_factory(Movie, MovieMedia, formset=TemplatedFormSet, form=MediaInlineForm, exclude=('movie',), extra=extra_itms)
	if req.method=='POST':
		frm = MovieForm(req.POST, instance=mov)
		mediaSet = MediaFormSet(req.POST, req.FILES, instance=mov)
		if mediaSet.is_valid() and frm.is_valid():
			mov = frm.save()
			mediaSet.save()
			mov.pull_tmdb_info()
			return redirect(reverse('mediadb:movie:show', args=[mov.id]))
				
	else:
		frm = MovieForm(instance=mov)
		mediaSet = MediaFormSet(instance=mov)

	context = {'movie': mov, 'form': frm, 'request': req, 'page_title': pg_title, 'button': btn_txt, 'media': mediaSet}
	context.update(_movie_context(mov))
	return render(req, 'mediadb/movies/edit.html', context)

def delete(req, pk):
	mov = Movie(pk)
	try:
		Movie.objects.get(pk=pk).delete()
	except Movie.DoesNotExist:
		pass
		
	return redirect(reverse('mediadb:movie:index'))

def tv_show(req, pk):
	pass

def tv_edit(req, pk=None):
	if pk:
		series = get_object_or_404(TVSeries, pk=pk)
		pg_title = 'Edit \'%s\'' % series.title
		btn_txt = 'Save changes'
		extra_itms = 0
	else:
		series = TVSeries()
		pg_title = 'Add TV Series...'
		btn_txt = 'Add'
		extra_itms = 1

	SeriesForm = modelform_factory(TVSeries)
	SeasonFormSet = inlineformset_factory(TVSeries, TVSeason, formset=TemplatedFormSet, exclude=('mediums',), extra=extra_itms)
	MediaFormSet = inlineformset_factory(TVSeason, TVSeasonMedia, formset=TemplatedFormSet, form=MediaInlineForm, exclude=('movie',), extra=extra_itms)
	EpisodeFormSet = inlineformset_factory(TVSeason, TVEpisode, formset=TemplatedFormSet, exclude=('mediums',), extra=extra_itms)
	if req.method=='POST':
		frm = SeriesForm(req.POST, instance=series)
		seasonSet = SeasonFormSet(req.POST, req.FILES, instance=series)
		all_valid = True
		for seasonForm in seasonSet:
			seasonForm.episodeSet = EpisodeFormSet(req.POST, req.FILES, instance=seasonForm.instance, prefix=seasonForm.prefix+'-episode')
			seasonForm.mediaSet = MediaFormSet(req.POST, req.FILES, instance=seasonForm.instance, prefix=seasonForm.prefix+'-media')
			all_valid = all_valid and seasonForm.episodeSet.is_valid() and seasonForm.mediaSet.is_valid()
			
		if all_valid and seasonSet.is_valid() and frm.is_valid():
			series = frm.save()
			seasonSet.save()
			for seasonForm in seasonSet:
				seasonForm.episodeSet.save()
				seasonForm.mediaSet.save()
			#series.pull_tmdb_info()
			return redirect(reverse('mediadb:series:show', args=[series.id]))
		
	else:
		frm = SeriesForm(instance=series)
		seasonSet = SeasonFormSet(instance=series)
		for seasonForm in seasonSet:
			seasonForm.episodeSet = EpisodeFormSet(instance=seasonForm.instance, prefix=seasonForm.prefix+'-episode')
			seasonForm.mediaSet = MediaFormSet(instance=seasonForm.instance, prefix=seasonForm.prefix+'-media')

	context = {
		'series': series,
		'form': frm,
		'request': req,
		'page_title': pg_title,
		'button': btn_txt,
		'SeasonFormSet': seasonSet,
	} #, 'media': mediaSet
	#context.update(_movie_context(series))
	return render(req, 'mediadb/tvseries/edit.html', context)