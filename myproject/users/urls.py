from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserCreateAPIView, PaymentViewSet


app_name = "users"


router = DefaultRouter()
router.register(r'payments', PaymentViewSet)

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserCreateAPIView, PaymentViewSet
from . import views

app_name = "users"


router = DefaultRouter()
router.register(r'payments', PaymentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserCreateAPIView.as_view(), name= 'register'),

]
urlpatterns += router.urls

