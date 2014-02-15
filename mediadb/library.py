import tmdb3
from django.conf import settings

tmdb3.set_locale()
tmdb3.set_key(settings.TMDB_KEY)

tmdb_url = 'http://api.themoviedb.org/3/'

def list_to_2d(lst, row_length=4):
	outList = []
	i=0
	for itm in lst:
		if i%row_length == 0:
			clist = []
			outList.append(clist)
		clist.append(itm)
		i += 1
	return outList

def find_best_size(sizes, trg):
        for sz in sizes:
                if sz[0] == 'w':
                        if int(sz[1:])>=trg: return sz

        return sizes[-1]

