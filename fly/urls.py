from django.conf.urls.defaults import *
from fly.flightlog.models import Flight, Wing, Location
from django.views.generic import list_detail,create_update

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

wing_info = {
    "queryset" : Wing.objects.all(),
    "paginate_by" : 10,
}

flight_info = {
    "queryset" : Flight.objects.all(),
}

urlpatterns = patterns('',
    (r'^wing/$', list_detail.object_list, wing_info),
    (r'^flights/$', list_detail.object_list, flight_info),

    # (r'^fly/', include('fly.foo.urls')),
    (r'^flights/$', 'fly.flightlog.views.index'),
    (r'^flights/new$', create_update.create_object, {'model': Flight}),
    (r'^flights/(?P<flight_id>\d+)/$', 'fly.flightlog.views.detail'),
    (r'^wing/new/$', 'fly.flightlog.views.newwing'),
    (r'^flight/new/$', 'fly.flightlog.views.newflight'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
