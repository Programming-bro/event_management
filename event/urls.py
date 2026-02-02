from django.urls import path
from event.views import mew, test, home, event_details, create_event, org_dash, update_event, delete_event

urlpatterns = [
    path('mew/',mew),
    path('test/',test),
    path('home/',home,name="home"),
    path('event_details/<int:id>/',event_details, name="event_details"),
    path('create_event/',create_event,name="create_event"),
    path('organizer_dashboard/',org_dash,name="organizer_dashboard"),
    path('update_event/<int:id>/',update_event, name="update_event"),
    path('delete_event/<int:id>/',delete_event, name="delete_event"),
]