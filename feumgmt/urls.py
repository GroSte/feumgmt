from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.views.i18n import javascript_catalog

admin.autodiscover()

js_info_dict = {
    'packages': ('base', ),
}

urlpatterns = [
    url(r'^jsi18n/$', javascript_catalog, js_info_dict, name='js_i18n'),
    url(r'^$', RedirectView.as_view(pattern_name='dashboard', permanent=True)),
    url(r'^base/', include('base.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
