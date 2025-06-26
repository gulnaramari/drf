from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    """Создание сериализатора для модели платежа"""
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """Создание сериализатора для модели пользователя с вложенным сериализатором платежей"""
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "password",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "city",
            "avatar",
            "payments",
        )


class UserBaseSerializer(serializers.ModelSerializer):
    """Создание сериализатора для модели пользователя с уменьшенным количеством полей"""
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "phone_number",
            "city",
            "avatar",
        )
