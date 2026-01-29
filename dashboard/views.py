from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event, EventBooking, Review

# Create your views here.


def dashboard(request):
    """Handle custom event booking form submission"""

    if request.method == "POST":
        # Check if user is authenticated
        if not request.user.is_authenticated:
            messages.error(request, "Please log in to book an event.")
            return redirect("login")

        # Get form data
        event_name = request.POST.get("event_name", "").strip()
        event_date = request.POST.get("event_date")
        event_time = request.POST.get("event_time")
        event_location = request.POST.get("event_location", "").strip()
        event_description = request.POST.get("event_description", "").strip()

        # Validate required fields
        if not all(
            [event_name, event_date, event_time, event_location, event_description]
        ):
            messages.error(
                request, "All fields are required. Please fill in all details."
            )
            return render(request, "index/home.html")

        try:
            # Create EventBooking
            event_booking = EventBooking(
                user=request.user,
                event_name=event_name,
                event_date=event_date,
                event_time=event_time,
                event_location=event_location,
                event_description=event_description,
            )
            event_booking.save()

            messages.success(
                request,
                f"Event '{event_name}' booking submitted successfully! "
                f"You can track its status in your dashboard.",
            )

        except Exception as e:
            messages.error(
                request,
                "Sorry, there was an error submitting your booking. Please try again.",
            )

        return redirect("home")

    # Get reviews to display on home page
    reviews = Review.objects.select_related("user", "event_booking").order_by(
        "-created_at"
    )[:10]

    context = {"reviews": reviews}

    return render(request, "index/home.html", context)


@login_required
def event_booking(request, boom):
    """Handle quick event booking from service cards"""

    # Check if user is authenticated
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to book an event.")
        return redirect("login")

    # Map boom parameter to event types
    event_types = {
        1: {"name": "Birthday Party", "type": Event.BIRTHDAY},
        2: {"name": "Wedding Ceremony", "type": Event.WEDDING},
        3: {"name": "Concert Event", "type": Event.CONCERT},
        4: {"name": "Conference Meeting", "type": Event.CONFERENCE},
    }

    # Get event type or default to conference
    event_info = event_types.get(boom, event_types[4])

    try:
        # Create a basic EventBooking record for tracking
        # User can later edit these details in their dashboard
        event_booking = EventBooking(
            user=request.user,
            event_name=event_info["name"],
            event_date="2025-01-01",  # Placeholder date - user will update
            event_time="12:00:00",  # Placeholder time - user will update
            event_location="TBD",  # To be determined - user will update
            event_description=f"Quick booking for {event_info['name']} - Please update details in your dashboard",
        )
        event_booking.save()

        # Show success message with instructions
        messages.success(
            request,
            f"'{event_info['name']}' booking created successfully! "
            f"Please visit your dashboard to complete the booking details.",
        )

    except Exception as e:
        messages.error(
            request,
            "Sorry, there was an error processing your request. Please try again.",
        )

    return redirect("home")


@login_required
def submit_review(request, booking_id):
    """Handle review submission for approved events"""
    booking = get_object_or_404(EventBooking, id=booking_id, user=request.user)

    # Check if event is approved
    if booking.status != EventBooking.APPROVED:
        messages.error(request, "You can only review approved events.")
        return redirect("profile")

    # Check if review already exists
    if Review.objects.filter(event_booking=booking).exists():
        messages.error(request, "You have already reviewed this event.")
        return redirect("profile")

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment", "").strip()

        # Validate input
        if not rating or not comment:
            messages.error(request, "Please provide both rating and comment.")
            return redirect("profile")

        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                messages.error(request, "Rating must be between 1 and 5.")
                return redirect("profile")

            # Create review
            review = Review(
                user=request.user, event_booking=booking, rating=rating, comment=comment
            )
            review.save()

            messages.success(request, "Thank you for your review!")

        except ValueError:
            messages.error(request, "Invalid rating value.")
        except Exception as e:
            messages.error(
                request,
                "Sorry, there was an error submitting your review. Please try again.",
            )

    return redirect("profile")
