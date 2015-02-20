from django.conf.urls import patterns, include, url
from django.contrib import admin
from apps.porsuk.views import ComponentsView, PackageView

from .views import IndexView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<repo>[\w\.-]+)/components/$', ComponentsView.as_view(), name='components'),
    url(r'^(?P<repo>[\w\.-]+)/components/(?P<component_or_package>[\w\.-]+)/$', ComponentsView.as_view(), name='component'),
    url(r'^(?P<repo>[\w\.-]+)/packages/(?P<slug>[\w\.-]+)/$', PackageView.as_view(), name='component'),
    url(r'^admin/', include(admin.site.urls)),
)



