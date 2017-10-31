from tmdb3 import set_key
from tmdb3 import searchMovie, searchPerson
key  = '79f8797f2c2e527e4e396dfe9816a3cd'
set_key(key)

query = 'Ja'

x = searchMovie(query)

print(x[0].title)