from django.contrib import admin

from .models import Payment, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "payment_date",
        "paid_course",
        "paid_lesson",
        "amount",
        "payment_type"

    )
