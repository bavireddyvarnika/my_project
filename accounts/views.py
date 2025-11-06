import random
import jwt
from datetime import datetime, timedelta, timezone
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from .models import AppUser
import json

def parse_json(request):
    return json.loads(request.body.decode())

def request_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

@csrf_exempt
def registeration(request):
    try:
        if request.method != "POST":
            return JsonResponse({"description": "Method not allowed"}, status=405)

        data = parse_json(request)
        email = (data.get("email") or "").strip().lower()
        password = data.get("password")

        if not email or not password:
            return JsonResponse({"description": "Missing Fields"}, status=400)

        if AppUser.objects.filter(email=email).exists():
            return JsonResponse({"description": "Already exists"}, status=400)

        otp = request_otp()
        hashed_password = make_password(password)
        AppUser.objects.create(email=email, password=hashed_password, otp=otp)
        
        return JsonResponse({"description": "User created and OTP sent for verification", "otp": otp}, status=201)
    except Exception as e:
        return JsonResponse(
            {"description": "Internal server error", "error": str(e)}, status=500
        )

@csrf_exempt
def verify_otp(request):
    try:
        if request.method != "POST":
            return JsonResponse({"description": "Method not allowed"}, status=405)

        data = parse_json(request)
        email = (data.get("email") or "").strip().lower()
        otp = data.get("otp")

        if not email or not otp:
            return JsonResponse({"description": "Missing Fields"}, status=400)

        user = AppUser.objects.get(email=email, otp=otp)
        if user:
            user.is_verified = True
            user.save()
            return JsonResponse({"description": "User verified and registered successfully"}, status=200)
        else:
            return JsonResponse({"description": "User Not Found"}, status=400)
    
    except Exception as e:
        return JsonResponse(
            {"description": "Internal server error", "error": str(e)}, status=500
        )
@csrf_exempt
def signin(request):
    if request.method != "POST":
        return JsonResponse({"description": "Method not allowed"}, status=405)

    data = parse_json(request)
    email = (data.get("email") or "").strip().lower()
    password = data.get("password")

    if not email or not password:
        return JsonResponse({"description": "Missing Fields"}, status=400)

    try:
        user = AppUser.objects.get(email=email)
    except AppUser.DoesNotExist:
        return JsonResponse({"description": "Invalid credentials"}, status=400)

    if not user.is_verified:
        return JsonResponse({"description": "User not verified"}, status=400)

    if not check_password(password, user.password):
        return JsonResponse({"description": "Invalid credentials"}, status=400)

    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.now(timezone.utc) + timedelta(days=7)
    }
    
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    
    return JsonResponse({"description": "Login successful", "token": token}, status=200)