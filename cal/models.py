from django.db import models
from django.urls import reverse

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    origin = models.CharField(max_length=50, blank=True, null=True)
    external_id = models.IntegerField(null=True, blank=True)

    @property
    def get_html_url(self):
        url = reverse('cal:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
    
class tblOrdini(models.Model):
    idordine = models.AutoField(primary_key=True)
    origineordine=models.IntegerField(null=True, blank=True)
    nordine=models.IntegerField(null=True, blank=True)
    dataordine=models.DateField(blank=True, null=True)
    idcliente=models.ForeignKey('tblClienti', on_delete=models.CASCADE)
    datacons=models.DateTimeField(blank=True, null=True)
    datacomunicata=models.DateField(blank=True, null=True)
    riford=models.CharField(max_length=200, null=True, blank=True)
    evaso=models.BooleanField(blank=True, null=True)
    note=models.CharField(max_length=500, null=True, blank=True)
    note_calendario=models.CharField(max_length=500, null=True, blank=True)

    @property
    def get_html_url(self, order_id):
        url = reverse('cal:order_edit', args=(order_id))
        return f'<a href="{url}"> {self.nordine} </a>'

class tblClienti(models.Model):
    idcliente=models.AutoField(primary_key=True)
    cliente=models.CharField(max_length=50, blank=True, null=True)
    codicecliente=models.CharField(max_length=50, blank=True, null=True)
    rappresentante=models.CharField(max_length=50, blank=True, null=True)
    note=models.CharField(max_length=200, blank=True, null=True)
    indirizzo=models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.cliente
    
class tbldettordini(models.Model):
    iddettordine=models.AutoField(primary_key=True)
    idordine=models.ForeignKey('tblOrdini', on_delete=models.CASCADE)
    idgruppo=models.ForeignKey('Gruppi', on_delete=models.CASCADE)
    idcolore=models.ForeignKey('Colori', on_delete=models.CASCADE)
    quantity=models.FloatField(blank=True, null=True)
    prezzo=models.FloatField(blank=True, null=True)

class Gruppi(models.Model)    :
    idgruppo=models.AutoField(primary_key=True)
    descrizionegruppo=models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.descrizionegruppo
    
class Colori(models.Model):
    idcolore=models.AutoField(primary_key=True)
    descrizionecolori=models.CharField(max_length=50, null=False, blank=False)
    
    def __str__(self):
        return self.descrizionecolori
    