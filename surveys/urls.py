from django.conf.urls import patterns, url

from surveys import views

urlpatterns = patterns('',
    url(r'^$', views.list_surveys, name='list_surveys'),
	url(r'/create$', views.create_survey, name='create_survey'),
	url(r'/delete$', views.delete_surveys, name='delete_surveys'),
	url(r'/display/(?P<survey_id>\d+)$', views.display_survey, name='display_survey'),
	url(r'/display/edit/(?P<survey_id>\d+)$', views.edit_survey, name='edit_survey'),
	url(r'/cancel$', views.cancel_create_survey, name='cancel_create_survey')
)
