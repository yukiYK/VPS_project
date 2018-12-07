from django.shortcuts import render as origin_render


def render(request, template_name, context=None):

    if not context:
        context = {}
    context["is_login"] = 1
    return origin_render(request, template_name, context)

