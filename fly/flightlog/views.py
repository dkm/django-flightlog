from django.http import HttpResponse, HttpResponseRedirect
from fly.flightlog.models import Flight, Wing, Location
from django.shortcuts import render_to_response, get_object_or_404
from django.forms import ModelForm

class WingForm(ModelForm):
    class Meta:
        model = Wing

class FlightForm(ModelForm):
    class Meta:
        model = Flight



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
    if year != None:
        queryset = Flight.objects.filter(date__year=year)
    else:
        queryset = Flight.objects.all()

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
                                                             'year': year})

