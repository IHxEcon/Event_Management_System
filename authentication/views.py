from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from authentication.models import User
from dashboard.models import EventBooking, Review


def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        if email is None or password is None:
            return redirect("login")

        user = authenticate(email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("home")
    return render(request, "authentication/login.html")


def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone_number = request.POST.get("phone_number")

        if User.objects.filter(email=email).exists():
            return redirect("register")

        if (
            email is None
            or password is None
            or first_name is None
            or last_name is None
            or phone_number is None
        ):
            return redirect("register")
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )
        user.save()
        return redirect("login")
    return render(request, "authentication/register.html")


@login_required
def profile(request):
    # Check if user is superuser and redirect to admin dashboard
    if request.user.is_superuser:
        return redirect("admin_dashboard")

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "update_profile":
            # Handle profile updates
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            phone_number = request.POST.get("phone_number")

            user = request.user
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if phone_number:
                user.phone_number = phone_number

            user.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")

        elif action == "update_event":
            # Handle event booking updates
            booking_id = request.POST.get("booking_id")
            booking = get_object_or_404(EventBooking, id=booking_id, user=request.user)

            booking.event_name = request.POST.get("event_name")
            booking.event_date = request.POST.get("event_date")
            booking.event_time = request.POST.get("event_time")
            booking.event_location = request.POST.get("event_location")
            booking.event_description = request.POST.get("event_description")

            booking.save()
            messages.success(request, "Event updated successfully!")
            return redirect("profile")

        elif action == "delete_event":
            # Handle event booking deletion
            booking_id = request.POST.get("booking_id")
            booking = get_object_or_404(EventBooking, id=booking_id, user=request.user)
            booking.delete()
            messages.success(request, "Event booking deleted successfully!")
            return redirect("profile")

    # Get user's event bookings
    user_bookings = EventBooking.objects.filter(user=request.user).order_by(
        "-event_date"
    )

    # Get bookings that can be reviewed (approved events without reviews)
    reviewable_bookings = []
    user_reviews = {}

    for booking in user_bookings:
        if booking.status == EventBooking.APPROVED:
            try:
                review = Review.objects.get(event_booking=booking)
                user_reviews[booking.id] = review
            except Review.DoesNotExist:
                reviewable_bookings.append(booking)

    context = {
        "user": request.user,
        "bookings": user_bookings,
        "total_bookings": user_bookings.count(),
        "reviewable_bookings": reviewable_bookings,
        "user_reviews": user_reviews,
    }

    return render(request, "authentication/profile.html", context)


def sign_out(request):
    logout(request)
    return redirect("login")


@login_required
def admin_dashboard(request):
    # Check if user is superuser
    if not request.user.is_superuser:
        messages.error(request, "Access denied. You need superuser privileges.")
        return redirect("home")

    if request.method == "POST":
        action = request.POST.get("action")
        booking_id = request.POST.get("booking_id")

        if action in ["approve", "reject"]:
            booking = get_object_or_404(EventBooking, id=booking_id)

            if action == "approve":
                booking.status = EventBooking.APPROVED
                booking.approved_by = request.user
                messages.success(
                    request,
                    f"Event booking for {booking.user.first_name} {booking.user.last_name} has been approved.",
                )
            elif action == "reject":
                booking.status = EventBooking.REJECTED
                booking.approved_by = request.user
                messages.success(
                    request,
                    f"Event booking for {booking.user.first_name} {booking.user.last_name} has been rejected.",
                )

            booking.save()
            return redirect("admin_dashboard")

    # Get all bookings with filters
    status_filter = request.GET.get("status", "all")
    search_query = request.GET.get("search", "")

    bookings = EventBooking.objects.select_related("user", "approved_by").all()

    if status_filter != "all":
        bookings = bookings.filter(status=status_filter)

    if search_query:
        bookings = bookings.filter(
            Q(user__first_name__icontains=search_query)
            | Q(user__last_name__icontains=search_query)
            | Q(user__email__icontains=search_query)
            | Q(event_name__icontains=search_query)
            | Q(event_location__icontains=search_query)
        )

    # Statistics
    total_bookings = EventBooking.objects.count()
    pending_bookings = EventBooking.objects.filter(status=EventBooking.PENDING).count()
    approved_bookings = EventBooking.objects.filter(
        status=EventBooking.APPROVED
    ).count()
    rejected_bookings = EventBooking.objects.filter(
        status=EventBooking.REJECTED
    ).count()

    context = {
        "bookings": bookings,
        "total_bookings": total_bookings,
        "pending_bookings": pending_bookings,
        "approved_bookings": approved_bookings,
        "rejected_bookings": rejected_bookings,
        "status_filter": status_filter,
        "search_query": search_query,
        "status_choices": EventBooking.STATUS_CHOICES,
    }

    return render(request, "authentication/admin_dashboard.html", context)
