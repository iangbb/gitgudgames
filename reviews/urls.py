from django.conf.urls import url
from reviews import views

urlpatterns = [
    # Development URL to fill in for pages yet to be created
    url(r'^$', views.index, name='#'),
    # URLs
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^games/$', views.games, name='games'),
    url(r'^game/$', views.game, name='game'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^restricted/$', views.restricted, name='restricted'),
    url(r'^review/$', views.review, name='review'),

]
