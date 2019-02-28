from django.conf.urls import url
from reviews import views

urlpatterns = [
    # Development URL to fill in for pages yet to be created
    url(r'^$', views.index, name='#'),
    # URLs
    url(r'^$', views.index, name='index'),
]
