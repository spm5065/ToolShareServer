__author__ = 'Noah'

from django.conf.urls import patterns, url
from borrow import views

urlpatterns = patterns('',
                       url(r'^request/(?P<pk>\d+)/$', views.request, name='request'),
                       # url(r'^detail/(?P<pk>\d+)/$', views.tool_detail, name='detail'),
                       # url(r'^edit/(?P<pk>\d+)/$', views.UpdateToolView.as_view(), name='edit'),
                       # url(r'^register/$', views.CreateToolView.as_view(), name='register'),
                       # url(r'^delete/(?P<pk>\d+)/$', views.DeleteToolView.as_view(), name = 'delete'),
                       # url(r'^display/(?P<pk>\d+)/$', views.DisplayToolView.as_view(), name = 'display'),

)