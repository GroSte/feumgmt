from django.conf.urls import url
from django.contrib.auth.views import login, logout_then_login
from django.core.urlresolvers import reverse_lazy
import views

urlpatterns = [
    url(r'^login/$', login, {'template_name': 'base/login.html'}, name='login'),
    url(r'^logout/$', logout_then_login, {'login_url': reverse_lazy('login')}, name='logout'),

    url(r'^dashboard/$', views.Dashboard.as_view(), name='dashboard'),
    url(r'^missions/?$', views.MissionList.as_view(), name='mission_list'),
    url(r'^mission/(?P<pk>\d+)?/?$', views.MissionUpdate.as_view(), name='mission_edit'),
    url(r'^mission-alarm/?$', views.MissionAlarm.as_view(), name='mission_alarm'),
    url(r'^bp-trainings/?$', views.BPTrainingList.as_view(), name='bptraining_list'),
    url(r'^bp-training/new$', views.BPTrainingCreate.as_view(), name='bptraining_new'),
    url(r'^bp-training/(?P<pk>\d+)?/?$', views.BPTrainingUpdate.as_view(), name='bptraining_edit'),
    url(r'^gallery/?$', views.GalleryList.as_view(), name='gallery'),
]
