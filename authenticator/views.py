from django.shortcuts import render
import time
from django.http import JsonResponse
import onetimepass as otp


# Create your views here.
def authenticator_page(request):
    if "secret_key" not in request.GET:
        return JsonResponse({"code": 400, "message": "secret_key lack"})
    secret_key = request.GET.get("secret_key")
    time1 = time.time() - 30
    time2 = time.time() + 30
    arr = list()
    try:
        otp.get_totp(secret_key)
    except Exception:
        return JsonResponse({"code": 401, "message": "invalid secret_key"})
    arr.append(fix_value(otp.get_totp(secret_key)))
    arr.append(fix_value(otp.get_totp(secret_key, clock=time1)))
    arr.append(fix_value(otp.get_totp(secret_key, clock=time2)))
    context = {"list": arr}
    return render(request, 'authenticator.html', context)


def fix_value(value):
    value_str = str(value)
    while len(value_str) < 6:
        value_str = '0' + value_str
    return value_str
