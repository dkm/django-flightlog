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

def index(request):
    latest_flights_list = Flight.objects.all().order_by('-date')[:5]
    return render_to_response('flightlog/index.html', {'latest_flights_list': latest_flights_list})



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


def newwing(request):
    if request.method == 'POST':
        form = WingForm(request.POST)
        if form.is_valid():
            w = Wing(name=form.cleaned_data['name'],
                     purchase_date=form.cleaned_data['purchase_date'])
            w.save()
            return HttpResponseRedirect('/')
    else:
        form = WingForm() # An unbound form

    return render_to_response('flightlog/newwing.html', {
            'form': form,
            })


def detail(request, flight_id):
    f = get_object_or_404(Flight, pk=flight_id)

    return render_to_response('flightlog/detail.html', {'flight': f})

