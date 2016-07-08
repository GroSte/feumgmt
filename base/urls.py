from django.conf.urls import url
from django.contrib.auth.views import login, logout_then_login
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
import views

urlpatterns = [
    url(r'^login/$', login, {'template_name': 'base/login.html'}, name='login'),
    url(r'^logout/$', logout_then_login, {'login_url': reverse_lazy('login')}, name='logout'),

    url(_(r'^dashboard/$'), views.Dashboard.as_view(), name='dashboard'),
    url(_(r'^user/password/?$'), views.UserChangePassword.as_view(), name='user_change_password'),
    url(_(r'^user-import/$'), views.UserImport.as_view(), name='user_import'),
    url(_(r'^message/?$'), views.MessageList.as_view(), name='message_list'),
    url(_(r'^message/new$'), views.MessageCreate.as_view(), name='message_new'),
    url(_(r'^message/(?P<pk>\d+)?/?$'), views.MessageUpdate.as_view(), name='message_edit'),
    url(_(r'^message/delete/(?P<pk>\d+)?/?$'), views.MessageDelete.as_view(), name='message_delete'),
    url(_(r'^gallery/?$'), views.GalleryList.as_view(), name='gallery'),
]
