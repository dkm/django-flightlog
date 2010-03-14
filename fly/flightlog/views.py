from django.http import HttpResponse
from fly.flightlog.models import Flight, Wing, Location
from django.shortcuts import render_to_response, get_object_or_404

def index(request):
    latest_flights_list = Flight.objects.all().order_by('-date')[:5]
    return render_to_response('flightlog/index.html', {'latest_flights_list': latest_flights_list})

def detail(request, flight_id):
    f = get_object_or_404(Flight, pk=flight_id)

    return render_to_response('flightlog/detail.html', {'flight': f})

