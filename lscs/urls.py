from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lscs.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^lscs/', include('surveys.urls')),
    url(r'^login/$', 'django.contrib.auth.views.login', {
        'template_name': 'lscs/login.html', 'extra_context': {'next': '/lscs/'}}),
    url(r'^admin/$', include(admin.site.urls)),
)
