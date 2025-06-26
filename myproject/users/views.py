from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny

from .models import Payment, User
from .permissions import IsUser
from .serializers import PaymentSerializer, UserBaseSerializer, UserSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """Контроллер для настройки фильтрации для
    эндпоинта  списка платежей:менять порядок сортировки по
    дате   оплаты,  фильтровать  по   курсу   или
    уроку,  фильтровать   по   способу   оплаты"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = (
        "paid_course",
        "paid_lesson",
        "type",
    )
    ordering_fields = ("payment_date",)


class UserCreateAPIView(CreateAPIView):
    """Класс, позволяет любому пользователю зарегистрироваться."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserUpdateAPIView(UpdateAPIView):
    """Класс, позволяет редактировать пользователя """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUser,)


class UserRetrieveAPIView(RetrieveAPIView):
    """Контроллер, позволяет получать детализацию о пользователе """
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.kwargs.get("pk") == self.request.user.pk:
            return UserSerializer
        return UserBaseSerializer


class UserListAPIView(ListAPIView):
    """Контроллер, позволяет получать список пользователей """
    queryset = User.objects.all()
    serializer_class = UserBaseSerializer


class UserDestroyAPIView(DestroyAPIView):
    """Контроллер, позволяет удалять пользователя """
    queryset = User.objects.all()
    permission_classes = (IsUser,)
