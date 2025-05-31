from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Car, Booking, Payment

admin.site.unregister(User)
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display  = ("username", "email", "is_active", "is_staff", "is_superuser")
    list_filter   = ("is_active", "is_staff", "is_superuser")
    actions       = ["approve_users"]

    @admin.action(description="Approve selected users")
    def approve_users(self, request, queryset):
        queryset.update(is_active=True)
        
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "car",
        "customer",
        "start_date",
        "end_date",
        "status",
    )
    list_filter = ("status",)
    actions = ["confirm_and_invoice"]

    @admin.action(description="Confirm selected bookings & create invoice")
    def confirm_and_invoice(self, request, queryset):
        pending = queryset.filter(status=Booking.PENDING)
        for bk in pending:
            bk.status = Booking.CONFIRMED
            bk.save()
            Payment.objects.get_or_create(
                booking=bk,
                defaults={"amount": bk.total_price}
            )

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "booking",
        "amount",
        "status",
        "paid_at",
    )
    list_filter = ("status",)

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display    = ("make", "model", "year", "price_per_day")
    search_fields   = ("make", "model")
    list_filter     = ("year",)
