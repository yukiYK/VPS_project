from common.response import render, JsonResponse
from common.check import is_phone
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from user.models import User
from common.redis import get_redis
from django.contrib.auth.decorators import login_required
# Create your views here.


# ---------------------------------page request--------------------------------
def login_page(request):
    return render(request, "user/login.html")


def register_page(request):
    return render(request, "user/register.html")


@login_required
def user_page(request):
    return render(request, "user/userCenter.html")


@login_required
def setting_page(request):
    return render(request, "user/setting.html")


# ---------------------------------API request---------------------------------
def sign_in(request):
    phone = request.POST.get("phone", "")
    password = request.POST.get("password", "")
    user = User.get_by_phone(phone)
    if not user:
        return JsonResponse(4001, "用户不存在")
    if not user.check_password(password):
        return JsonResponse(4002, "账户或密码错误")
    login(request, user)
    # save sessionid
    r_db1 = get_redis(**{'db': 1})
    session_key = request.session._get_session_key()
    r_db1.set('SESSION::%s' % user.id, session_key)
    return JsonResponse(200, "登录成功")


def sign_up(request):
    phone = request.POST.get("phone", "")
    password = request.POST.get("password", "")
    if not is_phone(phone):
        return JsonResponse(4001, "请输入正确的手机号")
    user = User.get_by_phone(phone)
    if user:
        return JsonResponse(4002, "手机号已被注册")
    try:
        User.create(phone, password)
    except:
        return JsonResponse(4003, "注册失败，请稍后再试")
    return JsonResponse(200, "注册成功")


def sign_out(request):
    logout(request)
    return redirect("/")

