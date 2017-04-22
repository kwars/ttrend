from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Index, name='index'),
    url(r'^post/$', views.Post, name='post'),
    #url(r'^snsEP/$', views.snsEP, name='snsEP'),
    #url(r'^polling/$', views.snsEP, name='polling')

]
