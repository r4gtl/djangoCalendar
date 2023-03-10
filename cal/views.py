from django.views.generic import View
from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic.list import MultipleObjectMixin
import calendar
import numpy as np

from .models import *
from .utils import Calendar
from .forms import EventForm, OrderForm

def index(request):
    return HttpResponse('hello')

class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        print("d dall class based: " + str(d))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

class DashboardView(View):
    #login_url = "accounts:signin"
    template_name = "cal/dashboard.html"

    def get(self, request, *args, **kwargs):
        # events = Event.objects.get_all_events(user=request.user)
        # running_events = Event.objects.get_running_events(user=request.user)
        # latest_events = Event.objects.filter(user=request.user).order_by("-id")[:10]
        events = Event.objects.get_all_events()
        running_events = Event.objects.get_running_events()
        latest_events = Event.objects.filter().order_by("-id")[:10]
        context = {
            "total_event": events.count(),
            "running_events": running_events,
            "latest_events": latest_events,
        }
        return render(request, self.template_name, context)

def calendarView(request) :

    # The dictionary for data initialization with field names as the keys
    context ={}
    d = get_date(request.GET.get('month', None))
    print("D: " + str(d))
    cal = Calendar(d.year, d.month)
    html_cal = cal.formatmonth(withyear=True)
    # It has to be added to the dictionary during field initialization
    context["eventi"] = Event.objects.all()  
    context["ordini"] = tblOrdini.objects.all()
    context['calendar'] = mark_safe(html_cal)
    context['prev_month'] = prev_month(d)
    context['next_month'] = next_month(d)
    return render(request, "cal/calendar.html", context)

def calendarWeekView(request) :

    # The dictionary for data initialization with field names as the keys
    context ={}
    d = get_date(request.GET.get('month', None))
    print("D: " + str(d))
    cal = Calendar(d.year, d.month)
    
    dateToday = datetime.now()
    week=get_week_of_month(d.year, d.month, d.day)
    print("Settimana ottenuta: " + str(week))
    html_cal = cal.formatmonthWeek(week, withyear=True)
    # It has to be added to the dictionary during field initialization
    context["eventi"] = Event.objects.all()  
    context["ordini"] = tblOrdini.objects.all()
    context['calendar'] = mark_safe(html_cal)
    context['prev_month'] = prev_month(d)
    context['next_month'] = next_month(d)
    return render(request, "cal/calendar.html", context)

def get_week_of_month(year, month, day):
		x = np.array(calendar.monthcalendar(year, month))
		week_of_month = np.where(x==day)[0][0] + 1
		return(week_of_month)

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'cal/event.html', {'form': form})

def order(request, order_id=None):
    instance = tblOrdini()
    if order_id:
        instance = get_object_or_404(tblOrdini, pk=order_id)
    else:
        instance = tblOrdini()

    form = OrderForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'cal/order.html', {'form': form})