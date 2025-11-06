from django.urls import path
from .views import registeration, verify_otp, signin

urlpatterns = [
    path("auth/register", registeration),
    path("auth/verify-otp", verify_otp),
    path("auth/signin", signin),

]
