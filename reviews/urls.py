from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from reviews import views

urlpatterns = [
    # Site URLs
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^restricted/$', views.restricted, name='restricted'),
    # Game urls
    url(r'^games/$', views.games, name='games'),
    url(r'^games/(?P<game_slug>[\w\-]+)/$', views.game, name='game'),
    url(r'^games/(?P<game_slug>[\w\-]+)/add_review/$', views.add_review, name='add_review'),
    # User urls
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    # Profile urls
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
    url(r'^profile/(?P<username>[\w\-]+)/edit/$', views.edit_profile, name='edit_profile'),
    # AJAX URLs
    url(r'^ajax/get_comments/$', views.ajax_get_comments, name='ajax_get_comments'),
    url(r'^ajax/get_reviews/$', views.ajax_get_reviews, name='ajax_get_reviews'),
    url(r'^ajax/add_comment/$', views.ajax_add_comment, name='ajax_add_comment'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
