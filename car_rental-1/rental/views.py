from __future__ import annotations

import stripe
from datetime import datetime
from django.contrib import messages 

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

from .forms import (BookingForm, CarFilterForm, MockPaymentForm, SignUpForm)
from .models import Booking, Car, Payment
from .forms import ProfileForm
from .models import Profile

def home(request):
    return render(request, "rental/home.html")

def car_list(request):
    qs = Car.objects.filter(available=True)
    form = CarFilterForm(request.GET or None)
    if form.is_valid():
        qs = form.filter_queryset(qs)

    return render(request, "rental/car_list.html", {"cars": qs, "form": form})

def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk, available=True)
    return render(request, "rental/car_detail.html", {"car": car})

def rental_search(request):
    cars = []
    start_raw = request.GET.get("start_date")
    end_raw = request.GET.get("end_date")

    if start_raw and end_raw:
        start = datetime.strptime(start_raw, "%Y-%m-%d").date()
        end = datetime.strptime(end_raw, "%Y-%m-%d").date()

        cars = (
            Car.objects.filter(available=True)
               .exclude(
                   bookings__status__in=[Booking.PENDING, Booking.CONFIRMED],
                   bookings__start_date__lt=end,
                   bookings__end_date__gt=start,
               )
               .distinct()
        )

    return render(request, "rental/rental_search.html", {
        "cars": cars, "start_date": start_raw, "end_date": end_raw
    })

def contact_us(request):
    return render(request, "rental/contact_us.html")

def signup(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(
            request,
            "Thanks for signing up! Your account is pending approval by an administrator."
        )
        return redirect("login")
    return render(request, "rental/signup.html", {"form": form})

@login_required
def customer_dashboard(request):
    bookings = (Booking.objects
        .filter(customer=request.user)
        .select_related("car")
        .prefetch_related("payment")
        .order_by("-created_at")
    )
    return render(request, "rental/customer_dashboard.html",
                  {"bookings": bookings})

@login_required
def create_booking(request, car_id):
    car = get_object_or_404(Car, pk=car_id, available=True)
    form = BookingForm(request.POST or None, car=car)

    if request.method == "POST" and form.is_valid():
        booking = form.save(commit=False)
        booking.customer = request.user
        booking.save()
        return redirect("my_bookings")

    return render(request, "rental/create_booking.html", {
        "car": car,
        "form": form,
    })

@login_required
def my_bookings(request):
    qs = (
        Booking.objects
               .filter(customer=request.user)
               .select_related("car", "payment")
               .order_by("-created_at")
    )
    return render(
        request,
        "rental/my_bookings.html",
        {"bookings": qs},
    )

@login_required
def view_bookings(request):
    qs = Booking.objects.filter(customer=request.user).select_related("car")
    return render(request, "rental/my_bookings.html", {
        "bookings": qs
    })

@login_required
def pay_booking(request, booking_id: int):
    booking = get_object_or_404(
        Booking.objects.select_related("payment", "car"),
        pk=booking_id, customer=request.user, status=Booking.CONFIRMED
    )

    payment, _ = Payment.objects.get_or_create(
        booking=booking, defaults={"amount": booking.total_price}
    )

    if payment.status == Payment.PAID:
        return redirect("payment_receipt", pk=payment.pk)

    form = MockPaymentForm(request.POST or None, instance=payment)
    if request.method == "POST" and form.is_valid():
        payment.status = Payment.PAID
        payment.paid_at = timezone.now()
        payment.save()
        return redirect("payment_receipt", pk=payment.pk)

    return render(request, "rental/payment_form.html",
                  {"booking": booking, "payment": payment, "form": form})

@login_required
def payment_receipt(request, pk: int):
    payment = get_object_or_404(
        Payment.objects.select_related("booking__car"),
        pk=pk, booking__customer=request.user
    )
    return render(request, "rental/payment_receipt.html", {"payment": payment})

@login_required
def stripe_checkout(request, booking_id: int):
    booking = get_object_or_404(
        Booking,
        pk=booking_id,
        customer=request.user,
        status=Booking.CONFIRMED,
    )

    payment, _ = Payment.objects.get_or_create(
        booking=booking, defaults={"amount": booking.total_price}
    )

    if payment.status == Payment.PAID:
        return redirect("payment_success", payment_id=payment.pk)

    days = (booking.end_date - booking.start_date).days or 1
    amount = int(days * booking.car.price_per_day * 100)

    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": str(booking.car),
                    "description": f"{booking.start_date} → {booking.end_date}",
                },
                "unit_amount": amount,
            },
            "quantity": 1,
        }],
        metadata={"payment_id": payment.pk},
        success_url=(
            request.build_absolute_uri(
                reverse("payment_success")
                + f"?payment_id={payment.pk}"
            )
        ),
        cancel_url=(
            request.build_absolute_uri(
                reverse("payment_cancel")
                + f"?payment_id={payment.pk}"
            )
        ),
    )

    payment.stripe_session_id = session.id
    payment.save()

    return redirect(session.url, code=303)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig = request.headers.get("stripe-signature", "")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        sess = event["data"]["object"]
        pid = sess["metadata"].get("payment_id")
        try:
            payment = Payment.objects.get(pk=pid)
        except Payment.DoesNotExist:
            pass
        else:
            payment.status = Payment.PAID
            payment.paid_at = timezone.now()
            payment.save()

    return HttpResponse(status=200)

@login_required
def payment_success(request):
    pid = request.GET.get("payment_id")
    payment = get_object_or_404(
        Payment, pk=pid, booking__customer=request.user
    )
    return render(request, "rental/payment_success.html", {"payment": payment})

@login_required
def payment_cancel(request):
    pid = request.GET.get("payment_id")
    payment = get_object_or_404(
        Payment, pk=pid, booking__customer=request.user
    )
    return render(request, "rental/payment_cancel.html", {"payment": payment})

@staff_member_required
def manage_bookings(request):
    qs = (Booking.objects.select_related("car", "customer")
                           .order_by("-created_at"))

    status = request.GET.get("status")
    if status in dict(Booking.STATUS_CHOICES):
        qs = qs.filter(status=status)

    return render(request, "rental/manage_bookings.html",
                  {"bookings": qs, "status_choices": Booking.STATUS_CHOICES})

@staff_member_required
def update_booking_status(request, booking_id: int, new_status: str):
    booking = get_object_or_404(Booking, pk=booking_id)
    if new_status in dict(Booking.STATUS_CHOICES):
        booking.status = new_status
        booking.save()
    return redirect("manage_bookings")

@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile_obj)

    return render(request, "rental/profile.html", {
        "profile": profile_obj,
        "form": form,
    })