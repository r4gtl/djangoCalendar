#from django.conf.urls import url
from django.urls import re_path as url
from . import views

app_name = 'cal'
urlpatterns = [
    #url("", views.DashboardView.as_view(), name="dashboard"),
    url(r'^index/$', views.DashboardView.as_view(), name='dashboard'),
    #url(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
    #url(r'^calendar/$', views.calendarView, name='calendar'),
    url(r'^calendar/$', views.calendarWeekView, name='calendar'),
    url(r'^event/new/$', views.event, name='event_new'),
    url(r'^order/new/$', views.order, name='order_new'),
	url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
    url(r'^order/edit/(?P<order_id>\d+)/$', views.order, name='order_edit'),
]
