from django.conf.urls import url
import views

urlpatterns = [
    # url(r'^login/$', login, {'template_name': 'base/login.html'}, name='login'),
    # url(r'^logout/$', logout_then_login, {'login_url': reverse_lazy('login')}, name='logout'),

    url(r'^dashboard/$', views.Dashboard.as_view(), name='dashboard'),
    url(r'^missions/?$', views.MissionList.as_view(), name='mission_list'),
    url(r'^mission/(?P<pk>\d+)?/?$', views.MissionUpdate.as_view(), name='mission_edit'),
]
