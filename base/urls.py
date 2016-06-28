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
    url(r'^bp-carriers/?$', views.BPCarrierList.as_view(), name='bpcarrier_list'),
    url(r'^bp-carrier/(?P<pk>\d+)?/?$', views.BPCarrierUpdate.as_view(), name='bpcarrier_edit'),
    url(r'^message/?$', views.MessageList.as_view(), name='message_list'),
    url(r'^message/new$', views.MessageCreate.as_view(), name='message_new'),
    url(r'^message/(?P<pk>\d+)?/?$', views.MessageUpdate.as_view(), name='message_edit'),
    url(r'^user-import/$', views.UserImport.as_view(), name='user_import'),
    url(r'^training-import/$', views.TrainingImport.as_view(), name='training_import'),
    url(r'^gallery/?$', views.GalleryList.as_view(), name='gallery'),
]
