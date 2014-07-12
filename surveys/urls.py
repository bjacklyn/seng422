from django.conf.urls import patterns, url

from surveys import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
	url(r'/create$', views.create, name='create'),
	url(r'/delete$', views.delete, name='delete'),
	url(r'/display$', views.display, name='display'),
	url(r'/cancel$', views.cancel, name='cancel')
)
