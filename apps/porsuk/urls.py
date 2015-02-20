from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'apps.porsuk.views.index', name='components'),
    url(r'^(?P<component_or_package>[\w\.-]+)/$', 'apps.porsuk.views.index', name='packages'),
    url(r'^(?P<component>[\w\.-]+)/source/(?P<source>[\w\.-]+)/$', 'apps.porsuk.views.source_detail', name='source_detail'),
    url(r'^(?P<component>[\w\.-]+)/(?P<package>[\w\.-]+)/$', 'apps.porsuk.views.package_detail', name='package_detail'),
    #(r'^(?P<url>.*)$', 'apps.defaultapp.views.index'),
)
