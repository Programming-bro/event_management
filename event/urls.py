from django.urls import path
from event.views import events, event_details, create_event, org_dash, update_event, delete_event, book_event, user_dash, dashboard

urlpatterns = [
    path('events/',events,name="events"),
    path('dashboard', dashboard, name='dashboard'),
    path('event_details/<int:id>/',event_details, name="event_details"),
    path('create_event/',create_event,name="create_event"),
    path('organizer_dashboard/',org_dash,name="organizer_dashboard"),
    path('user_dashboard/',user_dash,name="user_dashboard"),
    path('update_event/<int:id>/',update_event, name="update_event"),
    path('delete_event/<int:id>/',delete_event, name="delete_event"),
    path('book_event/<int:id>/',book_event,name="book_event")
]