from django.db import models


from authentication.models import User

# Create your models here.


class EventBooking(models.Model):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=50, null=False, blank=False)
    event_date = models.DateField(null=False, blank=False)
    event_time = models.TimeField(null=False, blank=False)
    event_location = models.CharField(max_length=50, null=False, blank=False)
    event_description = models.TextField(null=False, blank=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_bookings",
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.event_name}"

    class Meta:
        ordering = ["-created_at"]


class Event(models.Model):
    BIRTHDAY = "birthday"
    WEDDING = "wedding"
    CONCERT = "concert"
    CONFERENCE = "conference"

    EVENT_TYPE_CHOICES = [
        (BIRTHDAY, "Birthday"),
        (WEDDING, "Wedding"),
        (CONCERT, "Concert"),
        (CONFERENCE, "Conference"),
    ]

    event_name = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.event_name


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_booking = models.OneToOneField(EventBooking, on_delete=models.CASCADE)
    rating = models.IntegerField(
        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")], default=5
    )
    comment = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.rating} stars"

    class Meta:
        ordering = ["-created_at"]
