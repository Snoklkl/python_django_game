from django.shortcuts import render
from .models import stocks_info, player_info, player_targets, time_trackers

# Create your views here.

def index(request):
    return render(request, 'stocks/index.html')