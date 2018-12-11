from django.conf.urls import url
from . import views

app_name = 'authenticator'

urlpatterns = [
    url(r'^$', views.authenticator_page, name='authenticator_page'),
    url(r'^api/google$', views.google, name='google'),
    url(r'^captcha$', views.captcha_page, name='captcha_page'),
    url(r'^api/get_new_captcha$', views.get_new_captcha),
    url(r'^api/submit_form$', views.submit_form),
]
