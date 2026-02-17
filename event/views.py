from django.shortcuts import render, redirect
from django.http import HttpResponse
from event.models import Event, Category
from event.forms import EventModelForm
from django.db.models import Count, Q
from datetime import date
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from django.contrib import messages
from users.views import is_admin

# Create your views here.

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()


def is_participant(user):
    return user.groups.filter(name='User').exists()

def events(request):
    search = request.GET.get('search','all')
    loc = request.GET.get('location','all')
    base_query = Event.objects.select_related('category').prefetch_related('participant')
    events = base_query.all()
    cats = Category.objects.all()
    category = Category.objects.filter(name=type).first()
    group = request.user.groups.first().name
    if(search != 'all' and loc != 'all'):
        events = base_query.filter(Q(name__icontains=search) | Q(location = loc))
    elif(search != 'all'):
        events = base_query.filter(name__icontains=search)
    elif(loc != 'all'):
        events = base_query.filter(location = loc)
    context = {
        "events":events,
        "cats":cats,
        "group":group
    }
    return render(request,"events.html",context)

def event_details(request,id):
    event = Event.objects.prefetch_related('participant').get(id=id)
    participants = event.participant.all()
    context = {
        "participants":participants,
        "event":event
    }
    return render(request,"event_details.html",context)

def org_dash(request):
    type = request.GET.get('type','todays') 
    # tasks = Task.objects.select_related('details').prefetch_related('assigned_to').all()
    counts = Event.objects.aggregate(
        total = Count('id'),
        upcoming = Count('id',filter=Q(event_date__gt= date.today())),
        todays = Count('id',filter=Q(event_date = date.today())),
        past = Count('id',filter=Q(event_date__lt=date.today()))
    )
    participant = Event.objects.aggregate(total = Count('participant',distinct=True))
    base_query = Event.objects.select_related('category').prefetch_related('participant')
    
    if type == 'todays':
        events = base_query.filter(event_date = date.today())
    elif type == 'upcoming':
        events = base_query.filter(event_date__gt= date.today())
    elif type == 'past':
        events = base_query.filter(event_date__lt= date.today())
    elif type == 'my':
        events = request.user.revp_event.all()
    elif type == 'all':
        events = base_query.all()
    print(type)
    my_count = request.user.revp_event.count()

    group = request.user.groups.first().name
    context = {
        'events':events,
        'todays':base_query.filter(event_date = date.today()),
        'counts':counts,
        'my_cnt':my_count,
        'type':type,
        'participants':participant,
        'group': group
    }
    return render(request,"organizer_dashboard.html",context)

def user_dash(request):
    return render(request,"organizer_dashboard.html")


@login_required
@permission_required("event.view_event", login_url='no-permission')
def book_event(request, id):
    if request.method == 'POST':
        event = Event.objects.get(id = id)
        user = request.user
        if user in event.participant.all():
            messages.warning(request, 'You have already booked this event.')
        else:
            event.participant.add(user)
            messages.success(request,"Successfully Booked the event")
        return redirect("dashboard")
        
    return HttpResponse("Invalid request method", status=400)

@login_required
@permission_required("event.add_event", login_url='no-permission')
def create_event(request):
    form = EventModelForm()
    if(request.method == 'POST'):
        form = EventModelForm(request.POST, request.FILES)
        if form.is_valid():
            """For ModelForm data"""
            form.save()
            messages.success(request, "Task Created Successfully")
            return redirect('create_event')
    
    context = {"form":form}

    return render(request,"create_event.html",context)

@login_required
@permission_required("event.change_event", login_url='no-permission')
def update_event(request,id):
    event = Event.objects.get(id=id)
    # participants = Event.participant.objects.all()
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

@login_required
@permission_required("event.delete_event", login_url='no-permission')
def delete_event(request,id):
    if(request.method == 'POST'):
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request,"Event Deleted successfully")
        return redirect("organizer_dashboard")
    else:
        messages.error(request,"Something went wrong")
        return redirect("organizer_dashboard")


@login_required
def dashboard(request):
    if is_organizer(request.user):
        return redirect('organizer_dashboard')
    elif is_participant(request.user):
        return redirect('user_dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')

    return redirect('no-permission')