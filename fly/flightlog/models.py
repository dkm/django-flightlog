from django.db import models

# Create your models here.

class Wing(models.Model):
    name = models.CharField(max_length=200)
    purchase_date = models.DateTimeField('date of purchase')

    def __unicode__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name

class Flight(models.Model):
    date = models.DateTimeField()
    duration = models.PositiveIntegerField()
    takeoff = models.ForeignKey(Location, related_name="takeoff")
    landing = models.ForeignKey(Location, related_name="landing")
    wing = models.ForeignKey(Wing)
    distance = models.PositiveIntegerField()
    
    def __unicode__(self):
        return "%s -> %s" %(self.takeoff, self.landing)

    def get_absolute_url(self):
        return "/flights/%i/" % self.id
