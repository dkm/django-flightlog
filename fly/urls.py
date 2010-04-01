from django.conf.urls.defaults import *
from fly.flightlog.models import Flight, Wing, Location
from django.views.generic import list_detail,create_update
from django.forms import ModelForm
from olwidget.widgets import EditableMap
from django.contrib import databrowse

import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

wing_info = {
    "queryset" : Wing.objects.all(),
    "template_object_name" : "wing",
}

flight_info = {
    "queryset" : Flight.objects.all(),
    "template_object_name" : "flight",
}

location_info = {
    "queryset" : Location.objects.all(),
    "template_object_name" : "location",
}
        
urlpatterns = patterns('',


    (r'^flight/$', list_detail.object_list, flight_info),
    (r'^flight/stats/$', "fly.flightlog.views.flightstats"),
    (r'^flight/stats/(?P<year>\d+)/$', "fly.flightlog.views.flightstats"),
    (r'^flight/new$', create_update.create_object, {'model': Flight}),
    (r'^flight/view/(?P<object_id>\d+)/$', list_detail.object_detail, flight_info),
    (r'^flight/edit/(?P<object_id>\d+)/$', create_update.update_object, {'model': Flight}),
    (r'^flight/del/(?P<object_id>\d+)/$', create_update.delete_object, {'model': Flight,
                                                                        'post_delete_redirect': '/flight',
                                                                        'template_object_name' : 'flight'}),

    (r'^wing/$', list_detail.object_list, wing_info),
    (r'^wing/new/$', create_update.create_object, {'model': Wing}),
    (r'^wing/view/(?P<wing_id>\d+)/$', "fly.flightlog.views.wing_detail"),
    (r'^wing/edit/(?P<object_id>\d+)/$', create_update.update_object, {'model': Wing}),
    (r'^wing/del/(?P<object_id>\d+)/$', create_update.delete_object, {'model': Wing,
                                                                      'post_delete_redirect': '/wing',
                                                                      'template_object_name' : 'wing'}),
    (r'^databrowse/(.*)', databrowse.site.root),
    (r'^location/$', list_detail.object_list, location_info),
    (r'^location/new$', "fly.flightlog.views.create_location"),
#    (r'^location/view/(?P<object_id>\d+)/$', list_detail.object_detail, location_info),
    (r'^location/view/(?P<location_id>\d+)/$', "fly.flightlog.views.location_detail"),
    (r'^location/edit/(?P<location_id>\d+)/$', "fly.flightlog.views.location_update"),
    (r'^location/del/(?P<object_id>\d+)/$', create_update.delete_object, {'model': Location,
                                                                          'post_delete_redirect': '/location',
                                                                          'template_object_name' : 'location'}),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^umedia/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
)
