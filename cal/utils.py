from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event, tblOrdini
from django.urls import reverse
import numpy as np


#class Calendar(HTMLCalendar):
class originalCalendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	#def formatday(self, day, events, orders):
	def formatday(self, day, events):
		events_per_day = events.filter(start_time__day=day)
		
		d = ''
		for event in events_per_day:
			d += f'<li> {event.get_html_url} </li>'
		
		
		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
			
		return f'<tr> {week} </tr>'

	
	
 
 
	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)
		#orders = tblOrdini.objects.filter(datacons__year=self.year, datacons__month=self.month)
		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
			
		return cal



################Nuovo


class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		
		super(Calendar, self).__init__()
		print("Anno: " + str(self.year))
		print("Mese: " + str(self.month))
		
  
	# formats a day as a td
	# filter events by day
	#def formatday(self, day, events, orders):
	# def formatday(self, day, events):
	# 	print("Eventi: " + str(events))
	# 	events_per_day = events.filter(start_time__day=day)
		
	# 	d = ''
	# 	for event in events_per_day:
	# 		d += f'<li> {event.get_html_url} </li>'
		
		
	# 	if day != 0:
	# 		return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
	# 	return '<td></td>'
 
	def formatday(self, day, events):
		
		
		events_per_day = events.filter(start_time__day=day)
		
		d = ''
		for event in events_per_day:
			if event.origin == "order":
				order_id=event.external_id
				url = reverse('cal:order_edit', args=(order_id,))
				ordine=tblOrdini.objects.get(idordine=order_id)
				d += f'<li class="order"><a style="color:black;" href="{url}"> { ordine.datacons } </a> </li>'
			else:
				d += f'<li> {event.get_html_url} </li>'
		
		
		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

 
	# formats a week as a tr
	def formatweek(self, theweek, events):
		week = ''
		print("Theweek: " + str(theweek))
		for d, weekday in theweek:
			week += self.formatday(d,events)
			
		return f'<tr> {week} </tr>'

	# def formatweekOnly(self, theweek, events):
	# 	events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)
	# 	#orders = tblOrdini.objects.filter(datacons__year=self.year, datacons__month=self.month)
	# 	cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
	# 	cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
	# 	cal += f'{self.formatweekheader()}\n'
	# 	#for week in self.monthdays2calendar(self.year, self.month):
	# 	cal += f'{self.formatweek(week, events)}\n'
			
	# 	return cal

	def formatweekOnly(self, theweek, weekNum, events):
		week = ''
		theweek=theweek[:int(weekNum)]
		print("Theweek: " + str(theweek))
		for d, weekday in theweek:
			week += self.formatday(d,events)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)
		orders = tblOrdini.objects.filter(datacons__year=self.year, datacons__month=self.month)
		
	
		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			print("Settimana da formatmonth: " + str(week))
			cal += f'{self.formatweek(week, events)}\n' 
   			
			
		return cal
	
	def formatmonthWeek(self, week, withyear=True):
		#Appunto per me. Devo capire qual è il numero della settimana nella
		#tupla che esce dalla funzione week.
		events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)
	
		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		count=0
		for theweek in self.monthdays2calendar(self.year, self.month):
			if count==week-1:
				cal += f'{self.formatweek(theweek, events)}\n' 		
			count+=1

  		# count=0
  		
		# for week in self.monthdays2calendar(self.year, self.month):
		# 	count+=1
		# 	print("Inizio Week:" + str(week))
		# 	print("Inizio Exact_Week:" + str(exact_week))
		# 	if count == exact_week:
		# 		print("Week:" + str(week))
		# 		print("Exact_Week:" + str(exact_week))
		# 		print("Trovato")
		# 		cal += f'{self.formatweek(week, events)}\n' 
   			
			
		return cal

	


##################### Modificabile
class cancellaCalendar(HTMLCalendar):
#class provaCalendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	#def formatday(self, day, events, orders):
	def formatday(self, day, events,orders):
		print("Orders formatday: " + str(orders))
		print("Events formatday: " + str(events))
		events_per_day = events.filter(start_time__day=day)
		orders_per_day = orders.filter(datacons=day)
		d = ''
		for event in events_per_day:
			d += f'<li> {event.get_html_url} </li>'
		
		for order in orders_per_day:
			d += f'<li> {order.get_html_url} </li>'

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr
	def formatweek(self, theweek, events, orders):
		print("Orders formatweek: " + str(orders))
		print("Events formatweek: " + str(events))
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events, orders)
			#week += self.formatday(d, orders)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		#print("Orders formatmonth: " + str(orders))
		events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)
		orders = tblOrdini.objects.filter(datacons__year=self.year, datacons__month=self.month)
		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events, orders)}\n'
			#cal += f'{self.formatweek(week, orders)}\n'
		return cal
###################Prove precedenti