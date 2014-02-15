from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def mult(value, arg):
    "Multiplies the arg and the value"
    return float(value) * float(arg)

@register.filter
def sub(value, arg):
    "Subtracts the arg from the value"
    return float(value) - float(arg)
	
@register.filter
def div(value, arg):
    "Divides the value by the arg"
    return float(value) / float(arg)

@register.filter
def get_range( value ):
	"""
	Filter - returns a list containing range made from given value
	Usage (in template):

	<ul>{% for i in 3|get_range %}
	<li>{{ i }}. Do something</li>
	{% endfor %}</ul>

	Results with the HTML:
	<ul>
	<li>0. Do something</li>
	<li>1. Do something</li>
	<li>2. Do something</li>
	</ul>

	Instead of 3 one may use the variable set in the views
	"""
	return range( value )

@register.filter(name='fa', needs_autoescape=True)
@stringfilter
def fontawesome(value, autoescape=None):
	if autoescape:
		esc = conditional_escape
	else:
		esc = lambda x: x

	return mark_safe('<i class="fa fa-%s"></i>' % esc(value))
	
class GenreNode(template.Node):
	def __init__(self, movie):
		self.movie = movie
		
	def render(self, context):
		if self not in context.render_context:
			context.render_context[self] = (
                template.Variable(self.movie),
            )
	
		if 'genres_list' not in context:
			context['genres_list'] = []
		
		movie = context.render_context[self][0].resolve(context)
		genreList = ""
		if movie.json is not None:
			for genre in movie.json['genres']:
				if genre['name'] not in context['genres_list']:
					context['genres_list'].append(genre['name'])
				genreList += genre['name'] + ','
		
		context['genres_list'].sort()
		
		return genreList
		
@register.tag
def collect_movie_genres(parser, token):
	args = token.split_contents()
	return GenreNode(args[1])
	
