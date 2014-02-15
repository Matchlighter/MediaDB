from django.conf.urls import patterns, url, include
import views
import ajax

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^(?P<v>grid|list|plainlist)/$', views.index, name='index'),
	url(r'^gridBody/$', views.gridBody, name='gridBody'),
	
	url(r'^movie/', include(patterns('',
		url(r'^(?P<pk>\d+)/$', views.show, name='show'),
		url(r'^(?P<pk>\d+)/edit/$', views.edit, name='edit'),
		url(r'^(?P<pk>\d+)/delete/$', views.delete, name='delete'),
		url(r'^new/$', views.edit, name='new'),
	), namespace='movie')),
	
	url(r'^series/', include(patterns('',
		url(r'^(?P<pk>\d+)/$', views.tv_show, name='show'),
		url(r'^(?P<pk>\d+)/edit/$', views.tv_edit, name='edit'),
		url(r'^(?P<pk>\d+)/delete/$', views.delete, name='delete'),
		url(r'^new/$', views.tv_edit, name='new'),
	), namespace='series')),
	
	url(r'^ajax/', include(patterns('',
		url(r'^tmdb/(?P<resource>.+)/$', ajax.tmdb),
		url(r'^tmdbSearch/$', ajax.getMovieList, name='tmdbSearch'),
		
		url(r'^movie/', include(patterns('',
			url(r'^gridList/$', ajax.movie_list_json, name='gridList'),
			
			url(r'^(?P<pk>[\sA-Za-z0-9]+)/', include(patterns('',
				url(r'^$', ajax.movie_details, name='details'),
			))),
		), namespace='movie')),
		
		url(r'^location/(?P<loc_id>[\sA-Za-z0-9]+)/', include(patterns('',
			url(r'^nextIndex/$', None, name='nextIndex'),
		), namespace='location')),
	), namespace='ajax')),
)
