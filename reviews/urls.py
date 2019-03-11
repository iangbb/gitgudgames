from django.conf.urls import url
from reviews import views

urlpatterns = [
    # Development URL to fill in for pages yet to be created
    url(r'^$', views.index, name='#'),
    # URLs
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^games/', views.games, name='games'),
    url(r'^games/(?P<game_slug>[\w\-]+)/$', views.game, name='game'),
    url(r'^games/(?P<game_slug>[\w\-]+)/add_review/$', views.add_review, name='add_review'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^restricted/$', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name='logout'),
]
