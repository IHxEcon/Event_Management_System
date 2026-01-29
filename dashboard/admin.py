from django.contrib import admin

from dashboard.models import Event, EventBooking, Review

# Register your models here.


@admin.register(EventBooking)
class EventBookingAdmin(admin.ModelAdmin):
    list_display = [
        "user__first_name",
        "event_name",
        "event_date",
        "event_time",
        "event_location",
    ]
    search_fields = ["event_name", "event_location"]
    list_filter = ["event_date", "event_time"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["event_name", "user__first_name"]
    search_fields = ["event_name"]
    list_filter = ["event_name"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "event_booking", "rating", "created_at"]
    search_fields = ["user__first_name", "user__last_name", "comment"]
    list_filter = ["rating", "created_at"]
    readonly_fields = ["created_at", "updated_at"]
