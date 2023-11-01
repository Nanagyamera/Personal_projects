from django.urls import path
from .views import EventListView, EventDetailView, EventCreateView, EventUpdateView, EventDeleteView
from . import views

urlpatterns = [
    path('', views.landingpage, name='eventHub-landingpage'),
    path('home/', EventListView.as_view(), name='eventHub-home'),
    path('about/', views.about, name='eventHub-about'),
    path('contact/', views.contact, name='eventHub-contact'),
    path('successPage/', views.successPage, name='success-page'),
    path('signIn/', views.signIn, name='eventHub-signin'),
    path('signUp/', views.signUp, name='eventHub-signup'),
    path('signOut/', views.signOut, name='eventHub-signout'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('event/new/', EventCreateView.as_view(), name='event-create'),
    path('event/<int:pk>/update/', EventUpdateView.as_view(), name='event-update'),
    path('event/<int:pk>/delete/', EventDeleteView.as_view(), name='event-delete'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.search_events, name='search'),
    path('register_event/<int:event_id>/', views.register_event, name='register_event'),
    path('event/<int:event_id>/registered_attendees/', views.registered_attendees, name='registered_attendees'),
]