from django.http import HttpResponse, HttpResponseRedirect
from fly.flightlog.models import Flight, Wing, Location
from django.shortcuts import render_to_response, get_object_or_404
from django.forms import ModelForm
from django import forms
from django.template import RequestContext

from django.views.generic import list_detail,create_update

from olwidget.widgets import MapDisplay,EditableMap

OL_LAYERS = ['osm.mapnik', 
             'osm.osmarender', 
             'google.streets', 
             'google.physical', 
             'google.satellite', 
             'google.hybrid', 
             've.road', 
             've.shaded', 
             've.aerial', 
             've.hybrid', 
             'wms.map', 
             ##            'wms.nasa', 
             'yahoo.map']

## Grenoble
DEFAULT_LAT=45.194619097664
DEFAULT_LON=5.7650756833635

OL_OPTIONS = {    
    'hide_textarea': True,
    'default_zoom': 10,
    'layers' : OL_LAYERS,
    'default_lat': DEFAULT_LAT,
    'default_lon': DEFAULT_LON
    }

class LocationForm(ModelForm):
    coord = forms.CharField(widget=EditableMap(options = OL_OPTIONS))
    class Meta:
        model = Location

 
class FlightForm(forms.ModelForm):
    track = forms.CharField(widget=EditableMap(options={
        'geometry': 'linestring',
        'hide_textarea': False,
    }))

    class Meta:
        model = Flight

def wing_detail(request, wing_id):
    flights = Flight.objects.filter(wing__exact=wing_id)[:5]
    return list_detail.object_detail(
        request,
        queryset = Wing.objects.all(),
        object_id = wing_id,
        template_object_name = "wing",
        template_name = "flightlog/wing_detail.html",
        extra_context = {"flights" : flights}
    )

def create_location(request):
    return create_update.create_object(
        request,
        form_class=LocationForm,
        )



def location_update(request, location_id=None):
    Form = LocationForm

    if location_id:
        instance = Form.Meta.model.objects.get(pk=location_id)
    else:
        instance = Form.Meta.model()
 
    if request.method == 'POST':
        form = Form(request.POST, instance=instance)
        try:
            model = form.save()
            return HttpResponseRedirect(model.get_absolute_url())
        except ValueError:
            pass
    else:
        form = Form(instance=instance)
 
    return render_to_response("flightlog/location_form.html",
            {'form': form},
            RequestContext(request))

def flight_detail(request, flight_id):
    takeoff = Flight.objects.filter(takeoff__exact=location_id)[:5]
    landing = Flight.objects.filter(landing__exact=location_id)[:5]

    the_map = MapDisplay(fields=[Location.objects.get(pk=location_id).coord],options={
            'hide_textarea': True,
            } )

    # Use the object_list view for the heavy lifting.
    return list_detail.object_detail(
        request,
        queryset = Location.objects.all(),
        object_id = location_id,
        template_object_name = "flight",
        template_name = "flightlog/flight_detail.html",
        extra_context = {"takeoff" : takeoff,
                         "landing" : landing,
                         "map": the_map}
    )


def location_detail(request, location_id):
    takeoff = Flight.objects.filter(takeoff__exact=location_id)[:5]
    landing = Flight.objects.filter(landing__exact=location_id)[:5]

    the_map = MapDisplay(fields=[Location.objects.get(pk=location_id).coord],options={
            'hide_textarea': True,
            } )

    # Use the object_list view for the heavy lifting.
    return list_detail.object_detail(
        request,
        queryset = Location.objects.all(),
        object_id = location_id,
        template_object_name = "location",
        template_name = "flightlog/location_detail.html",
        extra_context = {"takeoff" : takeoff,
                         "landing" : landing,
                         "map": the_map}
    )


def create_flight(request):
    return create_update.create_object(
        request,
        form_class=FlightForm,
        )



def flight_update(request, flight_id=None):
    Form = FlightForm

    if flight_id:
        instance = Form.Meta.model.objects.get(pk=flight_id)
    else:
        instance = Form.Meta.model()
 
    if request.method == 'POST':
        form = Form(request.POST, instance=instance)
        try:
            model = form.save()
            return HttpResponseRedirect(model.get_absolute_url())
        except ValueError:
            pass
    else:
        form = Form(instance=instance)
 
    return render_to_response("flightlog/flight_form.html",
            {'form': form},
            RequestContext(request))


def flight_detail(request, flight_id):

    the_map = MapDisplay(fields=[Flight.objects.get(pk=flight_id).track],options={
            'hide_textarea': True,
            } )

    # Use the object_list view for the heavy lifting.
    return list_detail.object_detail(
        request,
        queryset = Flight.objects.all(),
        object_id = flight_id,
        template_object_name = "flight",
        template_name = "flightlog/flight_detail.html",
        extra_context = {"map": the_map}
    )


def newflight(request):
    if request.method == 'POST':
        form = FlightForm(request.POST)
        if form.is_valid():
            # w = Wing(name=form.cleaned_data['name'],
            #          purchase_date=form.cleaned_data['purchase_date'])
            # w.save()
            return HttpResponseRedirect('/')
    else:
        form = FlightForm() # An unbound form

    return render_to_response('flightlog/newflight.html', {
            'form': form,
            })



def flightstats(request, year=None):
    all = Flight.objects.all()

    if year != None:
        queryset = Flight.objects.filter(date__year=year)
    else:
        queryset = all

    years = {}
    for x in all:
        years[x.date.year] = True

    l = len(queryset)

    dist = 0

    for f in queryset:
        dist += f.distance

    if l == 0:
        avg_dist_per_flight = None
    else:
        avg_dist_per_flight = dist/len(queryset)
        
    return render_to_response('flightlog/flightstats.html', {"flight_list": queryset,
                                                             'total_distance' : dist,
                                                             'total_flights' : len(queryset),
                                                             'avg_dist_per_flight' : avg_dist_per_flight,
                                                             'year': year,
                                                             'years': years})

