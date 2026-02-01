from django.shortcuts import render, redirect
from django.http import HttpResponse
from event.models import Event, Participant, Category
from event.forms import EventModelForm
from django.db.models import Count, Q
from datetime import date
from django.contrib import messages

# Create your views here.

def mew(request):
    return render(request,"mew.html")

def test(request):
    return render(request,"test.html")

def home(request):
    events = Event.objects.all().select_related('category').prefetch_related('attended')
    context = {
        "events":events
    }
    return render(request,"home.html",context)

def org_dash(request):
    type = request.GET.get('type','all') 
    # tasks = Task.objects.select_related('details').prefetch_related('assigned_to').all()
    counts = Event.objects.aggregate(
        total = Count('id'),
        upcoming = Count('id',filter=Q(event_date__gt= date.today())),
        todays = Count('id',filter=Q(event_date = date.today())),
        past = Count('id',filter=Q(event_date__lt=date.today()))
    )
    participant = Event.objects.aggregate(total = Count('attended',distinct=True))
    base_query = Event.objects.select_related('category').prefetch_related('attended')
    
    if type == 'todays':
        events = base_query.filter(event_date = date.today())
    elif type == 'upcoming':
        events = base_query.filter(event_date__gt= date.today())
    elif type == 'past':
        events = base_query.filter(event_date__lt=date.today())
    elif type == 'all':
        events = base_query.all()
    print(type)

    context = {
        'events':events,
        'todays':base_query.filter(event_date = date.today()),
        'counts':counts,
        'type':type,
        'participants':participant
    }
    return render(request,"organizer_dashboard.html",context)

def create_event(request):
    participants = Participant.objects.all()
    form = EventModelForm()
    if(request.method == 'POST'):
        form = EventModelForm(request.POST)
        if form.is_valid():
            """For ModelForm data"""
            form.save()
            messages.success(request, "Task Created Successfully")
            return redirect('create_event')
    
    context = {"form":form}

    return render(request,"create_event.html",context)

def update_event(request,id):
    event = Event.objects.get(id=id)
    participants = Participant.objects.all()
    form = EventModelForm(instance=event)

    if(request.method == 'POST'):
        form = EventModelForm(request.POST,instance=event)
        if form.is_valid():
            """For ModelForm data"""
            form.save()
            messages.success(request, "Task Updated Successfully")
            return redirect('update_event',id)
    
    context = {"form":form}

    return render(request,"create_event.html",context)