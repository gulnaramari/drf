from django.contrib import admin

from .models import Payment, User, Subscription


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "payment_date",
        "paid_course",
        "paid_lesson",
        "amount",
        "payment_type"

    )

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
         "course",
         "created_at",
    )
