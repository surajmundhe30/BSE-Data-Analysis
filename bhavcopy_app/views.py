from django.shortcuts import render
from .models import *
import csv
import io
from django.conf import settings
from django.contrib import messages
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache

CACHE_TTL = getattr(settings ,'CACHE_TTL' , DEFAULT_TIMEOUT)

def get_bhavdata(filter_bhavdata = None):
    if filter_bhavdata: 
        bhavdata = Bhavdata.objects.filter(name__contains = filter_bhavdata)   # Fetching Data from Database
    else:
        bhavdata = Bhavdata.objects.all()
    return bhavdata

def home(request):
    
    filter_bhavdata = request.GET.get('bhavdata')
    if cache.get(filter_bhavdata):
        bhavdata = cache.get(filter_bhavdata)  # Fetching data from cache
    else:
        if filter_bhavdata:
            bhavdata = get_bhavdata(filter_bhavdata)
            cache.set(filter_bhavdata, bhavdata)
        else:
            bhavdata = get_bhavdata()
        
    context = {'bhavdata': bhavdata}
    return render(request, 'home.html' , context)

@csrf_exempt
def upload(request):   
    prompt={
        'order':'order should correct'
    }
    
    if request.method == "GET":
        return render(request, 'upload.html' , prompt)
    
    csv_file=request.FILES['file']
    
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'File format is not correct!')
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    print("Deleting Previous Data from table!")
    Bhavdata.objects.all().delete()
    print("Adding New data into the table!")
    for column in csv.reader(io_string,delimiter=',',quotechar="|"):
        _, created = Bhavdata.objects.update_or_create(
            code=column[0],
            name=column[1],
            open=column[4],
            high=column[5],
            low=column[6],
            close=column[7],
        )
                   
        context = {}
    print('Successfully Updated New Data!')
    return render(request, 'upload.html' , context)