from django.conf.urls import url
from . import views

app_name = 'authenticator'

urlpatterns = [
    url(r'^$', views.authenticator_page, name='authenticator'),
    url(r'^captcha$', views.validation_captcha, name='captcha'),
    url(r'^get_new_captcha$', views.get_new_captcha),
    url(r'^submit_form$', views.submit_form),
]
