from datetime import date, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Car(models.Model):
    make          = models.CharField(max_length=60)
    model         = models.CharField(max_length=60)
    year          = models.PositiveSmallIntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    image         = models.ImageField(upload_to="cars/", blank=True)
    available     = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

    def next_available_date(self):
        """
        Returns the next date this car is available by looking at confirmed/pending bookings.
        If the latest booked end_date is in the future (>= today), return (latest_end + 1 day).
        Otherwise, return today.
        """
        latest_end = self.bookings.aggregate(latest=Max("end_date"))["latest"]
        today = date.today()
        if latest_end and latest_end >= today:
            return latest_end + timedelta(days=1)
        return today


class Booking(models.Model):
    PENDING   = "pending"
    CONFIRMED = "confirmed"
    CANCELED  = "canceled"
    PAID     = "paid"

    STATUS_CHOICES = [
        (PENDING,   "Pending"),
        (CONFIRMED, "Confirmed"),
        (CANCELED,  "Canceled"),
        (PAID,      "Paid"),
        
    ]

    car        = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    customer   = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    start_date = models.DateField()
    end_date   = models.DateField()
    status     = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDING
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.car} • {self.start_date} → {self.end_date}"

    @property
    def total_price(self):
        """
        Compute total price as (number of days) * price_per_day.
        If start_date == end_date, treat it as 1 day.
        """
        days = (self.end_date - self.start_date).days or 1
        return days * self.car.price_per_day


class Payment(models.Model):
    PENDING = "pending"
    PAID    = "paid"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (PAID,    "Paid"),
    ]

    booking           = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="payment"
    )
    amount            = models.DecimalField(max_digits=10, decimal_places=2)
    status            = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDING
    )
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)
    paid_at           = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.booking} → {self.get_status_display()}"


def user_directory_path(instance, filename):
    """
    Generate upload path for user profile photos:
    MEDIA_ROOT/profiles/user_<id>/<filename>
    """
    return f"profiles/user_{instance.user.id}/{filename}"


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    photo = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
        null=True
    )
    # You can add more fields here (e.g. bio, phone number, etc.)

    def __str__(self):
        return f"Profile of {self.user.username}"


    @property
    def photo_url(self):
        if self.photo and hasattr(self.photo, "url"):
            return self.photo.url
        return "/static/rental/img/default_profile.png"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    1) If this is a brand‐new User (created=True), make a new Profile for them.
    2) Otherwise (existing User), get_or_create so that if a Profile is missing,
       Django will build one now—then save it.
    """
    if created:
        # New user → create a Profile row right away
        Profile.objects.create(user=instance)
    else:
        # Existing user → ensure a Profile exists (get_or_create) then save it
        profile_obj, _ = Profile.objects.get_or_create(user=instance)
        profile_obj.save()
