from django.conf.urls import url,include
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^$', views.khatam),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^dashboard/',views.dashboard),
    url(r'^login/',views.login),
    url(r'^logout/',views.logout),
    url(r'^register/',views.register),
    url(r'^fblogin/',views.fblogin),
    # url(r'^completeregister/',views.completeregister),
    url(r'^movie/(?P<movieid>\d+)/$', views.movie),
    url(r'^tv/(?P<tvid>\d+)/$', views.tv),
    url(r'^temp/',views.temp),
    url(r'^search/',views.search),
]