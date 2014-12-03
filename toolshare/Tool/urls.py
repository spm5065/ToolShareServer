__author__ = 'Sergio'

from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from Tool import views
from Tool.models import Tool
from django.views.generic import UpdateView
from Tool.forms import UpdateToolForm


urlpatterns = patterns('',
                       url(r'^$', views.index, name='tool_list'),
                       url(r'^detail/(?P<pk>\d+)/$', views.tool_detail, name='detail'),
                       url(r'^edit/(?P<pk>\d+)/$', views.UpdateToolView.as_view(), name='edit'),
                       url(r'^register/$', views.CreateToolView.as_view(), name='register'),
                       url(r'^delete/(?P<pk>\d+)/$', views.DeleteToolView.as_view(), name = 'delete'),
                       url(r'^display/(?P<pk>\d+)/$', views.DisplayToolView.as_view(), name = 'display'),
                       url(r'^pickup/$', views.pickups, name='pickups'),
                       url(r'^requested/$', views.requests, name='requests'),
                       url(r'^borrowed/$', views.borrowed, name='borrowed'),
                       url(r'^return/(?P<pk>\d+)/$', views.return_tool, name='return_tool'),
                       url(r'^approve/(?P<pk>\d+)/$', views.approve_request, name='approve_request'),
                       url(r'^pickup_tool/(?P<pk>\d+)/$', views.pickup_tool, name='pickup_tool'),
                       url(r'^return_check/(?P<pk>\d+)/$', views.return_check, name='return_check'),
                       url(r'^returned/$', views.returns, name='returned'),
                       url(r'^damaged/$', views.damaged, name='damaged'),
                       url(r'^fix/(?P<pk>\d+)/$', views.fix, name='fix'),
                       url(r'^stats/(?P<pk>\d+)/$', views.tool_stats, name='stats'),


)