from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
import time
from django.http import JsonResponse
import onetimepass as otp
from .forms import CaptchaTestForm
from django.views.generic.edit import CreateView
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
import json
from django.views.decorators.csrf import csrf_exempt


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


def validation_captcha(request):
    if request.POST:
        form = CaptchaTestForm(request.POST)
        if form.is_valid():
            human = True
    else:
        form = CaptchaTestForm()
    # return render_to_response('captcha.html', locals())
    return render(request, 'captcha.html', {"form": form})


def get_new_captcha(request):
    if request.GET.get('newsn') == '1':
        csn = CaptchaStore.generate_key()
        cimageurl = captcha_image_url(csn)
        return HttpResponse(cimageurl)


def submit_form(request):
    # if request.POST:
    #     form = CaptchaTestForm(request.POST)
    #     if form.is_valid():
    #         human = True
    #         print('Successfull')
    #     else:
    #         print('Failed')

    hash_key = request.POST.get('captcha_0', '')
    result = request.POST.get('captcha_1', '')
    captcha = CaptchaStore.objects.get(hashkey=hash_key)
    if captcha.response == result:
        print('Success')
        return JsonResponse({"code": 200})
    else:
        print('Failed')
        return JsonResponse({"code": 400})


# class AjaxExampleForm(CreateView):
#     template_name = ''
#     form_class = AjaxForm
#
#     def form_invalid(self, form):
#         if self.request.is_ajax():
#             to_json_response = dict()
#             to_json_response['status'] = 0
#             to_json_response['form_errors'] = form.errors
#             to_json_response['status'] = CaptchaStore.generate_key()
#             to_json_response['status'] = captcha_image_url(to_json_response['new_captcha_key'])
#
#             return HttpResponse(json.dumps(to_json_response), content_type='application/json')
#
#     def form_valid(self, form):
#         form.save()
#         if self.request.is_ajax():
#             to_json_response = dict()
#             to_json_response['status'] = 1
#             to_json_response['new_captcha_key'] = CaptchaStore.generate_key()
#             to_json_response['new_captcha_image'] = captcha_image_url(to_json_response['new_captcha_key'])
#
#             return HttpResponse(json.dumps(to_json_response), content_type='application/json')
