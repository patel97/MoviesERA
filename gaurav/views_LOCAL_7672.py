from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import logout as auth_logout
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.models import SocialToken

# from email.MIMEMultipart import MIMEMultipart
# from studyaccountsapp.safe import usermail,upassword
# from email.MIMEText import MIMEText

from django.contrib.auth import authenticate

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

import requests


from .API_ERA import popular
from .API_ERA import Classes
from .API_ERA import Genres
from .API_ERA import Search

import json
from random import shuffle

from .models import genre
from .models import User
from .models import UserProfile
# from .models import customUser
# Create your views here.

from django.views.decorators.cache import cache_page
from django.core.cache import cache

from tmdb3 import Movie
from tmdb3 import Series
from tmdb3 import set_key
key  = '79f8797f2c2e527e4e396dfe9816a3cd'
set_key(key)

def slide():
    movies_tv = popular.getPopular()
    shuffle(movies_tv)

    first_movie = movies_tv[0]
    movies_tv = movies_tv[1:]

    return first_movie, movies_tv


def popularMovies(GenreMovieList):
    popMovies = []
    for genre in GenreMovieList:
        x = GenreMovieList[genre][0]
        popMovies.append(x)

    return popMovies


def popularTV(GenreTVList):
    popTV = []
    for genre in GenreTVList:
        x = GenreTVList[genre][0]
        popTV.append(x)

    return popTV

def gen_vardict():
    var_dict = {}
    first_movie, movies_tv = slide()
    var_dict['First'] = first_movie
    print(len(first_movie.genreName),"\t",first_movie.title)
    for c in movies_tv:
        print(len(c.genreName),"\t",c.title)
    var_dict['MoviesTV'] = movies_tv

    genresMovie = ['Crime','Thriller', 'Fantasy', 'Science Fiction']
    genresTV = ['Comedy', 'Drama', 'Mystery', 'Reality']
    GenreMovieList, GenreTVList = Genres.getGenreList(genresMovie, genresTV)
    popMovies = popularMovies(GenreMovieList)
    popTV = popularTV(GenreTVList)
    var_dict['popMovies'] = popMovies
    var_dict['popTV'] = popTV

    genresMovie = ['Romance', 'Comedy', 'Drama']
    genresTV = []
    GenreMovieList, _ = Genres.getGenreList(genresMovie, genresTV)

    for genre in GenreMovieList:
        key = genre + 'Movie'
        var_dict[key] = GenreMovieList[genre][0:4]
    return var_dict

#@cache_page(60*1440)
def khatam(request):
    if request.user.is_authenticated():

    # var_dict = gen_vardict()
    # cache.set('var_dict',var_dict,60*1440)
    # var_dict = cache.get('var_dict')
        return render(request,'moviestar/index.html' )
    else:
        return redirect('/login/')

def movie(request, movieid):
    m = Movie(movieid)
    mx = Classes.Movies()
    mx.set(movie=m)
    mdict = {}
    mdict['movie'] = mx
    return render(request, 'moviestar/movie.html', mdict)

def tv(request, tvid):
    t = Series(tvid)
    tx = Classes.TV()
    tx.set(tv=t)
    tdict = {}
    tdict['tv'] = tx
    return render(request, 'moviestar/tv.html', tdict)

def dashboard(request):
    # u = customUser()
    u.setAttr(obj=request)      
    return render(request,'moviestar/single-movie.html')




def register(request):
    if request.method == 'POST':
        usermail = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

       
        user = User.objects.create(username=usermail,password=password)
        user.save()

        return render(request,'rocku/login.html')

    else:
        return render(request,'rocku/register.html')



# def registration(request,p):
    # if request.method=='POST':
    #     print (p)
    #     fname = request.POST.get('fname')
    #     lname = request.POST.get('lname')

    #     profile_pic = request.FILES['profile_pic']

    #     day = request.POST.get('day')
    #     month = request.POST.get('month')
    #     year = request.POST.get('year')

    #     gender = request.POST.get('gender')

    #     city = request.POST.get('city')
    #     country = request.POST.get('country')

    #     upass = request.POST.get('upass')
    #     upass1 = request.POST.get('upass1')

    #     print (fname)
    #     print(lname)
    #     print(day)
    #     print(month)
    #     print(year)
    #     print(gender)
    #     print(city)
    #     print(country)

    #     if upass == upass1:
    #         up = User.objects.get(password=p)
    #         print (up)

    #         userprofile = UserProfile.objects.create(user=up,first_name=fname,last_name=lname,
    #             profile_pic=profile_pic,day=day,month=month,year=year,gender=gender,
    #             city=city,country=country)
    #         userprofile.save()   

    #         up.set_password(upass)
    #         up.save()

    #         user = authenticate(username=up.username, password=upass)

    #         if user.is_active:
    #             auth_login(request, user)

    #             return redirect('/profile/')


    #         else:
    #             return HttpResponse("Unexpected Error! Please Try Again.")

    #     else:
    #         return HttpResponse('Enter password correctly')

    # else:
    #     up=User.objects.get(password=p)
    #     print (up)
    #     return render(request,'pages/details.html',{ 'p':p, 'day':range(31),
    #     'year':range(1980,2017) })




def login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('/')

            else:
                context['error'] = 'Non active user'
        else:
            context['error'] = 'Wrong username or password'
    else:
        context['error'] = ''

    # populateContext(request, context)

    return render(request, 'rocku/login.html', context)



def logout(request):
    context = {}
    if request.user.is_authenticated():
        auth_logout(request)
        # context['error'] = 'Some error occured.'

    #   populateContext(request, context)
    return render(request, 'rocku/login.html', context)



# def populateContext(request, context):
#     context['authenticated'] = request.user.is_authenticated()
#     if context['authenticated'] == True:
#         context['username'] = request.user.username
    
        # auth_logout(request)

# Create your views here.

    # def friend_list(request):
    #     context = {}
    #     fb_uid = SocialAccount.objects.filter(user_id=request.user.id, provider='facebook')
    #     print ('hi')
    #     print (fb_uid[0].uid)
    #     if fb_uid.exists():
    #         fb_uid = fb_uid[0].uid
    #         tolken = SocialToken.objects.filter(account__user=request.user, account__provider='facebook').first()
    #         #tolken='EAACEdEose0cBAPnFKDHpJpq7wvScCDma9dxd1V17NEejvVy2U0rVVbkOiX5aXHOjhapHyFaG5Ayo5dyAFCI0Ufv6aZA9wD0uNRRbxE0IOM4fRDWrWidJsGUuRNHm0RuIDEv5lhij5wKJZBJEOaEJKj7b6i5HlOdOhJPzLnA6TaP6H8CzK5gOWeLneoM6YZD'
    #         print(tolken)
            
    #         returned_json = requests.get("https://graph.facebook.com/v2.10/" + fb_uid + "/friends?access_token=" + 'EAACEdEose0cBAPnFKDHpJpq7wvScCDma9dxd1V17NEejvVy2U0rVVbkOiX5aXHOjhapHyFaG5Ayo5dyAFCI0Ufv6aZA9wD0uNRRbxE0IOM4fRDWrWidJsGUuRNHm0RuIDEv5lhij5wKJZBJEOaEJKj7b6i5HlOdOhJPzLnA6TaP6H8CzK5gOWeLneoM6YZD')

    #         targets = returned_json.json()['data']
    #         print(targets)
            
    #         # '''
    #         # id_list = [target['id'] for target in targets]
    #         # friends = SocialAccount.objects.filter(uid__in=id_list)
    #         # print(friends)
    #         # context['friends'] = friends
    #         # '''
    #     return render(request,'friendslist.html',)

def friend_list(request):
    context = {}
    fb_uid = SocialAccount.objects.filter(user_id=request.user.id, provider='facebook')
    print ('hi')
    print (fb_uid[0].uid)
    if fb_uid.exists():
        fb_uid = fb_uid[0].uid
        tolken = SocialToken.objects.filter(account__user=request.user, account__provider='facebook').first()
        # returned_json = requests.get("https://graph.facebook.com/v2.9/" + fb_uid + "/friends?access_token=" + str(tolken))
        print(tolken)
        returned_json = requests.get("https://graph.facebook.com/v2.10/" + fb_uid +"?fields=friends{name}&access_token=" + str(tolken))
        #   print(returned_json.json()['friends'])
        # targets = returned_json.json()['data']
        # id_list = [target['id'] for target in targets]
        # friends = SocialAccount.objects.filter(uid__in=id_list)
        # context['friends'] = friends
        print (context)
    return render(request,'friendslist.html',{'friends':context})


def fblogin(request):
    return render(request,'fblogin.html')


# def register(request):
#     if(request.method=='POST'):
#         some_var=request.POST.getlist('checks[]')
#         print (len(some_var))
#         print (some_var)
#         return HttpResponse('fuck you')
#     else:
#         genrelist=genre.objects.all()
#         print(genrelist)
#         return render(request,'register.html',{'genrelist':genrelist})


def search(request):
    if request.method=='POST':
        return HttpResponse('string aaya')
    else:
        return render(request,'search.html')


def searchresults(request):
    if(request.method=="POST"):
        movies_query=request.POST.get('movie')
        person_query=request.POST.get('person')
        if(movies_query==''):
            print('person search:')
            print(person_query)
            flag,res = Search.getTV(person_query) 
        else:
            print('movie search')
            print(movies_query)
            flag,res = Search.getMovie(movies_query)
        if(flag==0):
            r = 'Search Unsuccessful'
        else:
            r = ''
            for x in res:
                r += x.title + '\n'
        res = r
        return HttpResponse(res)