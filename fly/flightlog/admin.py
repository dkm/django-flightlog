from fly.flightlog.models import Flight,Wing,Location
##from django.contrib import admin
from django.contrib.gis import admin

admin.site.register(Flight)
admin.site.register(Wing)
##admin.site.register(Location)
 
admin.site.register(Location, admin.GeoModelAdmin)
