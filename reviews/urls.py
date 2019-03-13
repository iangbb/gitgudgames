from django.conf.urls import url
from reviews import views

urlpatterns = [
    # Site URLs
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    # Game urls
    url(r'^games/', views.games, name='games'),
    url(r'^game/(?P<game_slug>[\w\-]+)/$', views.game, name='game'),
    url(r'^game/(?P<game_slug>[\w\-]+)/add_review/$', views.add_review, name='add_review'),
    # User urls
    url(r'^profile/(?P<user>[\w\-]+)$', views.profile, name='profile'),
    url(r'^profile/(?P<user>[\w\-]+)/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^restricted/$', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name='logout'),
]
