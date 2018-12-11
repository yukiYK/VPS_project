import json
import time
from common.response import render
from django.http import HttpResponse
from django.http import JsonResponse
import onetimepass as otp
from .forms import CaptchaTestForm
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.contrib.auth.decorators import login_required


# Create your views here.
# ------------------------------------pages----------------------------------
@login_required
def authenticator_page(request):
    return render(request, 'authenticator/authenticator.html')


def captcha_page(request):
    if request.POST:
        form = CaptchaTestForm(request.POST)
        if form.is_valid():
            human = True
    else:
        form = CaptchaTestForm()
    # return render_to_response('captcha.html', locals())
    return render(request, 'authenticator/captcha.html', {"form": form})


# ---------------------------------------------------------------------------
def google(request):
    if "secret_key" not in request.POST:
        return JsonResponse({"code": 400, "message": "secret_key lack"})
    secret_key = request.POST.get("secret_key")
    time1 = time.time() - 30
    time2 = time.time() + 30
    arr = list()
    try:
        otp.get_totp(secret_key)
    except:
        return JsonResponse({"code": 401, "message": "invalid secret_key"})
    arr.append(fix_value(otp.get_totp(secret_key)))
    arr.append(fix_value(otp.get_totp(secret_key, clock=time1)))
    arr.append(fix_value(otp.get_totp(secret_key, clock=time2)))
    return JsonResponse({"code": 200, "data": arr})


def fix_value(value):
    value_str = str(value)
    while len(value_str) < 6:
        value_str = '0' + value_str
    return value_str


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
