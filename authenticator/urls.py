from django.conf.urls import url
from . import views

app_name = 'authenticator'

urlpatterns = [
    url(r'^$', views.authenticator_page, name='authenticator')
]
