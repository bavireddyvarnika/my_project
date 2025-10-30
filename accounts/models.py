# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


def default_expiry():
    # OTP expiry window; adjust as needed
    return timezone.now() + timedelta(minutes=10)




class User(models.Model):
    email = models.EmailField(unique=True)
    password=models.CharField()

    def __str__(self):
        return self.email


# class OTPCode(models.Model):
#     # Use AUTH_USER_MODEL so migrations stay stable
#     user = models.ForeignKey(
#         'User',                 # refer directly to your User model
#         on_delete=models.CASCADE,
#         related_name='otp_codes'
#     )    
#     created_at = models.DateTimeField(auto_now_add=True)
#     expires_at = models.DateTimeField(default=default_expiry)

#     class Meta:
#         indexes = [
#             models.Index(fields=["user", "code"]),
#             models.Index(fields=["expires_at"]),
#         ]

#     def __str__(self):
#         return f"{self.user.email} - {self.code}"
