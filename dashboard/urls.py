from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="home"),
    path("event_booking/<int:boom>", views.event_booking, name="event_booking"),
    path("submit_review/<int:booking_id>", views.submit_review, name="submit_review"),
]
