from django.http import HttpResponse, HttpResponseRedirect
from fly.flightlog.models import Flight, Wing, Location
from django.shortcuts import render_to_response, get_object_or_404
from django.forms import ModelForm

from django.views.generic import list_detail

class WingForm(ModelForm):
    class Meta:
        model = Wing

class FlightForm(ModelForm):
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

def location_detail(request, location_id):
    takeoff = Flight.objects.filter(takeoff__exact=location_id)[:5]
    landing = Flight.objects.filter(landing__exact=location_id)[:5]

    # Use the object_list view for the heavy lifting.
    return list_detail.object_detail(
        request,
        queryset = Location.objects.all(),
        object_id = location_id,
        template_object_name = "location",
        template_name = "flightlog/location_detail.html",
        extra_context = {"takeoff" : takeoff,
                         "landing" : landing}
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

