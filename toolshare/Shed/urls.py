__author__ = 'Sergio'

from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from Shed import views


urlpatterns = patterns('',
                       url(r'^(?P<page_id>\d+)/$', views.ShedList, name='shed_list'), #TemplateView.as_view(template_name='Shed/shed_list.html')
                       url(r'^detail/(?P<pk>\d+)/$', views.DisplayShedView.as_view(template_name='Shed/display.html'), name='detail'),
                       url(r'^register/$', views.CreateShedView.as_view(), name='register'),
                       url(r'^register_user/(?P<shed_id>\d+)/$', views.register_user_with_shed, name='register_user'),
                       url(r'^deregister_user/(?P<shed_id>\d+)/$', views.deregister_user_with_shed, name='deregister_user'),
                       url(r'^stats/(?P<pk>\d+)/$', views.shed_stats, name='stats'),
                       url(r'^update/(?P<pk>\d+)/$', views.UpdateShedView.as_view(), name = 'update'),
)