from django.urls import path
from event.views import mew, test, home, create_event, org_dash, update_event

urlpatterns = [
    path('mew/',mew),
    path('test/',test),
    path('home/',home,name="home"),
    path('create_event/',create_event,name="create_event"),
    path('organizer_dashboard/',org_dash,name="organizer_dashboard"),
    path('update_event/<int:id>/',update_event, name="update_event")
]