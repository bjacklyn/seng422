from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import password_reset_confirm
from lscs.forms import ValidatingSetPasswordForm

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'lscs.views.main_page', name='login'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
		password_reset_confirm, {'post_reset_redirect': '/reset_complete', 'template_name': 'lscs/set_password.html', 'set_password_form': ValidatingSetPasswordForm}, 
		name='password_reset_confirm'),
    url(r'^reset_complete$', 'lscs.views.reset_complete'),
    url(r'^admin', include(admin.site.urls)),
    url(r'^surveys', include('surveys.urls')),
	url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'})
	
)
