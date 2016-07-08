from django.conf.urls import url
import views

urlpatterns = [
    url(r'^missions/?$', views.MissionList.as_view(), name='mission_list'),
    url(r'^mission/new$', views.MissionCreate.as_view(), name='mission_new'),
    url(r'^mission/(?P<pk>\d+)?/?$', views.MissionUpdate.as_view(), name='mission_edit'),
    url(r'^mission/delete/(?P<pk>\d+)?/?$', views.MissionDelete.as_view(), name='mission_delete'),
    url(r'^mission-alarm/(?P<pk>\d+)?/?$', views.MissionAlarm.as_view(), name='mission_alarm'),
    url(r'^bp-trainings/?$', views.BPTrainingList.as_view(), name='bptraining_list'),
    url(r'^bp-training/new$', views.BPTrainingCreate.as_view(), name='bptraining_new'),
    url(r'^bp-training/(?P<pk>\d+)?/?$', views.BPTrainingUpdate.as_view(), name='bptraining_edit'),
    url(r'^bp-training/delete/(?P<pk>\d+)?/?$', views.BPTrainingDelete.as_view(),
        name='bptraining_delete'),
    url(r'^trainings/?$', views.TrainingList.as_view(), name='training_list'),
    url(r'^training/new$', views.TrainingCreate.as_view(), name='training_new'),
    url(r'^training/(?P<pk>\d+)?/?$', views.TrainingUpdate.as_view(), name='training_edit'),
    url(r'^training/delete/(?P<pk>\d+)?/?$', views.TrainingDelete.as_view(),
        name='training_delete'),
    url(r'^training-import/$', views.TrainingImport.as_view(), name='training_import'),
    url(r'^bp-carriers/?$', views.BPCarrierList.as_view(), name='bpcarrier_list'),
    url(r'^bp-carrier/(?P<pk>\d+)?/?$', views.BPCarrierUpdate.as_view(), name='bpcarrier_edit'),
]
