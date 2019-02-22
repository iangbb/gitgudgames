from django.conf.urls import url
from reviews import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
