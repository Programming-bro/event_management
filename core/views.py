from django.shortcuts import render

# Create your views here.
def home(request):
    group =  request.user.groups.first().name
    return render(request, 'home.html', {"group":group})

def no_permission(request):
    return render(request, 'no_permission.html')