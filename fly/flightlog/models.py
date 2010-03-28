##from django.db import models
from django.contrib.gis.db import models
# Create your models here.

class Wing(models.Model):
    name = models.CharField(max_length=200)
    purchase_date = models.DateTimeField('date of purchase')

    def __unicode__(self):
        return u"%s" % self.name

    def get_absolute_url(self):
        return "/wing/view/%i/" % self.id

class Location(models.Model):
    name = models.CharField(max_length=200)
    TYPE_CHOICES = (
        ('T', 'Take-Off'),
        ('L', 'Landing'),
        ('B', 'Take-off & Landing'),
    )
    ltype = models.CharField(max_length=1, choices=TYPE_CHOICES)
    coord = models.PointField()
    objects = models.GeoManager()

    def __unicode__(self):
        return u"%s (%s)" %(self.name, self.ltype)

    def get_absolute_url(self):
        return "/location/view/%i/" % self.id

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
        return "/flight/view/%i/" % self.id
