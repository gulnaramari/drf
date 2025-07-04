from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Payment, User
from .permissions import IsUser
from .serializers import PaymentSerializer, UserBaseSerializer, UserSerializer


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = (
        "course",
        "lesson",
        "payment_type",
    )
    ordering_fields = ("payment_date",)


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        if request.data.get("payment_type") != "cash":
            amount = request.data.get("amount")
            price = create_price(amount)
            payment_link = get_payment_link(price)
            return Response(
                {
                    "user": request.user.pk,
                    "course": request.data.get("course"),
                    "lesson": request.data.get("lesson"),
                    "amount": request.data.get("payment_amount"),
                    "payment_type": request.data.get("payment_method"),
                    "payment_link": payment_link,
                }
            )

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        payment.save()


class UserCreateAPIView(generics.CreateAPIView):
    """Класс, позволяет любому пользователю зарегистрироваться."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserUpdateAPIView(generics.UpdateAPIView):
    """Класс, позволяет редактировать пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUser,)


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер, позволяет получать детализацию о пользователе"""

    queryset = User.objects.all()

    def get_serializer_class(self):
        """Метод, позволяет получать детализацию полную для пользователя,
        и частичную не для этого пользователя"""
        if self.kwargs.get("pk") == self.request.user.pk:
            return UserSerializer
        return UserBaseSerializer


class UserListAPIView(generics.ListAPIView):
    """Контроллер, позволяет получать список пользователей"""

    queryset = User.objects.all()
    serializer_class = UserBaseSerializer


class UserDestroyAPIView(generics.DestroyAPIView):
    """Контроллер, позволяет удалять пользователя"""

    queryset = User.objects.all()
    permission_classes = (IsUser,)
