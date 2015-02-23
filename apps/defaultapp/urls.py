from django.conf.urls import patterns, include, url
from django.contrib import admin
from apps.porsuk.views import ComponentsView, PackageView, PackageListView

from .views import IndexView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<repo>[\w\.-]+)/packages/$', PackageListView.as_view(), name='packages'),
    url(r'^(?P<repo>[\w\.-]+)/packages/(?P<component>[\w\.-]+)/$', PackageListView.as_view(), name='packages'),



    url(r'^(?P<repo>[\w\.-]+)/components/$', ComponentsView.as_view(), name='components'),
    url(r'^(?P<repo>[\w\.-]+)/components/(?P<component_name>[\w\.-]+)/$', ComponentsView.as_view(), name='component'),
    url(r'^(?P<repo>[\w\.-]+)/package/(?P<slug>[\w\.-]+)/$', PackageView.as_view(), name='package'),
    url(r'^admin/', include(admin.site.urls)),
)



