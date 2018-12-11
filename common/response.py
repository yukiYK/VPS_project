from django.shortcuts import render as origin_render
from django.http import JsonResponse as origin_JsonResponse


def render(request, template_name, context=None):

    if not context:
        context = {}
    context["is_login"] = False
    if request.user and request.user.id:
        context["is_login"] = True
    return origin_render(request, template_name, context)


def JsonResponse(code, msg, data=None):
    if not data:
        data = {}
    return origin_JsonResponse({"code": code, "msg": msg, "data": data})
