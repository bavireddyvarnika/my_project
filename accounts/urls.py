from django.urls import path
from .views import registeration #verify_otp

urlpatterns = [
    path("auth/register", registeration),
    # path("auth/verify-otp", verify_otp),
]
