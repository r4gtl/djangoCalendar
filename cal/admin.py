from django.contrib import admin
from cal.models import Event, tblOrdini, tblClienti, Gruppi, Colori, tbldettordini

# Register your models here.
admin.site.register(Event)
admin.site.register(tblOrdini)
admin.site.register(tblClienti)
admin.site.register(Gruppi)
admin.site.register(Colori)
admin.site.register(tbldettordini)