from django import template
import mediadb.library
import tmdb3

register = template.Library()

def tmdbResURL(sizes, size, ident):
	return tmdb3.Configuration.images['base_url'] + mediadb.library.find_best_size(sizes, size) + str(ident)

@register.simple_tag()
def tmdbBgURL(size, ident):
	return tmdbResURL(tmdb3.Configuration.images['backdrop_sizes'], size, ident)

@register.simple_tag()
def tmdbPosterURL(size, ident):
	return tmdbResURL(tmdb3.Configuration.images['poster_sizes'], size, ident)
