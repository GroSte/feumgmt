from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
import views

urlpatterns = [
    url(_(r'^missions/?$'), views.MissionList.as_view(), name='mission_list'),
    url(_(r'^mission/new$'), views.MissionCreate.as_view(), name='mission_new'),
    url(_(r'^mission/(?P<pk>\d+)?/?$'), views.MissionUpdate.as_view(), name='mission_edit'),
    url(_(r'^mission/delete/(?P<pk>\d+)?/?$'), views.MissionDelete.as_view(), name='mission_delete'),
    url(_(r'^mission-alarm/(?P<pk>\d+)?/?$'), views.MissionAlarm.as_view(), name='mission_alarm'),
    url(_(r'^bp-trainings/?$'), views.BPTrainingList.as_view(), name='bptraining_list'),
    url(_(r'^bp-training/new$'), views.BPTrainingCreate.as_view(), name='bptraining_new'),
    url(_(r'^bp-training/(?P<pk>\d+)?/?$'), views.BPTrainingUpdate.as_view(), name='bptraining_edit'),
    url(_(r'^bp-training/delete/(?P<pk>\d+)?/?$'), views.BPTrainingDelete.as_view(),
        name='bptraining_delete'),
    url(_(r'^trainings/?$'), views.TrainingList.as_view(), name='training_list'),
    url(_(r'^training/new$'), views.TrainingCreate.as_view(), name='training_new'),
    url(_(r'^training/(?P<pk>\d+)?/?$'), views.TrainingUpdate.as_view(), name='training_edit'),
    url(_(r'^training/delete/(?P<pk>\d+)?/?$'), views.TrainingDelete.as_view(),
        name='training_delete'),
    url(_(r'^training-import/$'), views.TrainingImport.as_view(), name='training_import'),
    url(_(r'^bp-carriers/?$'), views.BPCarrierList.as_view(), name='bpcarrier_list'),
    url(_(r'^bp-carrier/(?P<pk>\d+)?/?$'), views.BPCarrierUpdate.as_view(), name='bpcarrier_edit'),
]
