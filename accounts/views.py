import random
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import User, OTPCode
import json

def parse_json(request):
    return json.loads(request.body.decode())

def request_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

@csrf_exempt
def registeration(request):
    if request.method != "POST":
        return JsonResponse({"description": "Method not allowed"}, status=405)

    data = parse_json(request)
    email = (data.get("email") or "").strip().lower()
    password = data.get("password")

    if not email or not password:
        return JsonResponse({"description": "Missing Fields"}, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({"description": "Already exists"}, status=400)

    return {}

    
    # return JsonResponse({"description": "OTP sent", "otp": otp}, status=200)

# @csrf_exempt
# def verify_otp(request):
#     if request.method != "POST":
#         return JsonResponse({"description": "Method not allowed"}, status=405)

#     data = parse_json(request)
#     email = (data.get("email") or "").strip().lower()
#     otp = data.get("otp")

#     try:
#         user = User.objects.get(email=email)
#     except User.DoesNotExist:
#         return JsonResponse({"description": "User not found"}, status=404)

#     otp_entry = OTPCode.objects.filter(user=user, code=otp).first()
#     if not otp_entry:
#         return JsonResponse({"description": "Invalid OTP"}, status=400)

#     user.is_verified = True
#     user.save()
#     otp_entry.delete()  # remove used OTP

#     return JsonResponse({"description": "User verified successfully"}, status=200)