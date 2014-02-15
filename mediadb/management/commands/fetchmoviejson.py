from django.core.management.base import BaseCommand, CommandError
from app.models import Movie
import time

class Command(BaseCommand):
	help = 'Loads all json from TMDB'

	def handle(self, *args, **options):
		for movie in Movie.objects.all():
			movie.pull_tmdb_info()
			time.sleep(0.4)
