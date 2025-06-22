from django.contrib import admin
from .models import User, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("owner_id", "payment_date", "paid_course", "paid_lesson", "amount", "type")
